"""
ml/stage_detector.py
Advanced Foliar Lesion Segmentation & Thermal Gradient Heatmap Engine for KrishiRakshak
Uses multi-space color processing (ExG, HSV, normalized RGB) and continuous Gaussian
density diffusion to accurately identify necrotic lesions, chlorotic halos, and photosynthetic health.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import scipy.ndimage as ndi
from typing import Dict, Any, Tuple


def _rgb_to_hsv_fast(r: np.ndarray, g: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Vectorized RGB to HSV conversion normalized to [0, 1].
    r, g, b must be float arrays in [0, 255].
    """
    rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
    cmax = np.maximum(np.maximum(rf, gf), bf)
    cmin = np.minimum(np.minimum(rf, gf), bf)
    delta = cmax - cmin + 1e-7

    # Hue calculation
    hue = np.zeros_like(cmax)
    mask_r = (cmax == rf)
    mask_g = (cmax == gf)
    mask_b = (cmax == bf)

    hue[mask_r] = ((gf[mask_r] - bf[mask_r]) / delta[mask_r]) % 6.0
    hue[mask_g] = ((bf[mask_g] - rf[mask_g]) / delta[mask_g]) + 2.0
    hue[mask_b] = ((rf[mask_b] - gf[mask_b]) / delta[mask_b]) + 4.0
    hue = (hue / 6.0) % 1.0

    # Saturation
    saturation = np.zeros_like(cmax)
    cmax_gt_0 = cmax > 1e-5
    saturation[cmax_gt_0] = delta[cmax_gt_0] / cmax[cmax_gt_0]

    # Value
    value = cmax
    return hue, saturation, value


def _apply_thermal_colormap(val: np.ndarray) -> np.ndarray:
    """
    Maps normalized scalar field val in [0, 1] to smooth RGB thermal palette:
    0.0 -> Healthy Green (46, 139, 87)
    0.25 -> Mild Chlorotic Yellow-Green (154, 205, 50)
    0.50 -> Chlorotic Amber-Yellow (255, 204, 0)
    0.75 -> Active Lesion Orange (255, 102, 0)
    1.0 -> Severe Necrotic Crimson (220, 20, 60)
    """
    v = np.clip(val, 0.0, 1.0)
    rgb = np.zeros((v.shape[0], v.shape[1], 3), dtype=np.float32)

    # Segment 0: 0.0 to 0.3 (Green to Yellow-Green)
    m0 = (v <= 0.3)
    t0 = v[m0] / 0.3
    rgb[m0, 0] = 46.0 + t0 * (210.0 - 46.0)
    rgb[m0, 1] = 139.0 + t0 * (215.0 - 139.0)
    rgb[m0, 2] = 87.0 + t0 * (0.0 - 87.0)

    # Segment 1: 0.3 to 0.6 (Yellow-Green to Amber)
    m1 = (v > 0.3) & (v <= 0.6)
    t1 = (v[m1] - 0.3) / 0.3
    rgb[m1, 0] = 210.0 + t1 * (255.0 - 210.0)
    rgb[m1, 1] = 215.0 + t1 * (160.0 - 215.0)
    rgb[m1, 2] = 0.0

    # Segment 2: 0.6 to 1.0 (Amber to Crimson Red)
    m2 = (v > 0.6)
    t2 = (v[m2] - 0.6) / 0.4
    rgb[m2, 0] = 255.0 + t2 * (220.0 - 255.0)
    rgb[m2, 1] = 160.0 + t2 * (20.0 - 160.0)
    rgb[m2, 2] = 0.0 + t2 * (50.0 - 0.0)

    return np.clip(rgb, 0, 255).astype(np.uint8)


def analyze_leaf_lesions(image: Image.Image) -> Dict[str, Any]:
    """
    Performs high-precision computer vision color space segmentation on the leaf image:
    1. Robust Leaf Canopy extraction via HSV, ExG, and chromatic filtering
    2. Deep Lesion & Chlorotic Halo detection
    3. Gaussian Spatial Thermal Diffusion Heatmap with contour boundaries
    4. Quantitative Lesion % and Photosynthetic Health % calculation
    5. Leaf Stage Classification (Stage 1, 2, 3)
    """
    work_size = (400, 400)
    img_rgb = image.convert("RGB").resize(work_size, Image.Resampling.BILINEAR)
    arr = np.array(img_rgb, dtype=np.float32)

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    sum_rgb = r + g + b + 1e-6
    rn = r / sum_rgb
    gn = g / sum_rgb
    bn = b / sum_rgb

    # Excess Green Index: ExG = 2*G - R - B
    exg = 2.0 * g - r - b

    # Convert to HSV color space
    hue, sat, val = _rgb_to_hsv_fast(r, g, b)

    # 1. Precise Leaf Canopy Segmentation
    # Exclude stark white/gray backgrounds, dark shadows, hands/skin
    is_not_stark_white = ~((r > 235) & (g > 235) & (b > 235) & (sat < 0.15))
    is_not_shadow = (sum_rgb > 65)

    # Plant foliar signatures in HSV & chromatic space:
    # A. Active Green tissue: Hue ~ 0.16 to 0.46 (approx 60° to 165°), Sat > 0.15
    is_green_foliage = (hue >= 0.15) & (hue <= 0.48) & (sat >= 0.12) & (gn > 0.32)
    # B. Chlorotic Yellow foliar: Hue ~ 0.08 to 0.18, Sat > 0.20, ExG > -15
    is_yellow_foliage = (hue >= 0.08) & (hue < 0.18) & (sat >= 0.18) & (g > b * 1.05)
    # C. Necrotic Brown/Tan foliar: Hue in red/brown, moderate brightness, leaf texture
    is_brown_foliage = (
        ((hue < 0.10) | (hue > 0.90)) & (sat >= 0.16) & (rn > 0.36) & (gn > 0.26) & (r > b * 1.15) & (val < 0.85)
    )

    raw_leaf_mask = (is_green_foliage | is_yellow_foliage | is_brown_foliage) & is_not_stark_white & is_not_shadow

    # Morphological cleanup: close small holes, remove speckles
    struct = ndi.generate_binary_structure(2, 2)
    cleaned_leaf_mask = ndi.binary_closing(raw_leaf_mask, structure=struct, iterations=2)
    cleaned_leaf_mask = ndi.binary_fill_holes(cleaned_leaf_mask)

    total_leaf_pixels = int(np.sum(cleaned_leaf_mask))
    total_pixels = work_size[0] * work_size[1]

    # Fallback if leaf mask too small (e.g. extreme closeup or atypical lighting)
    if total_leaf_pixels < 0.04 * total_pixels:
        cleaned_leaf_mask = is_not_stark_white & is_not_shadow & (val > 0.15)
        total_leaf_pixels = max(1, int(np.sum(cleaned_leaf_mask)))

    # 2. Healthy Chlorophyll vs Lesion Differentiation
    # Healthy green: strong ExG, clear green hue, balanced illumination
    healthy_tissue = (
        cleaned_leaf_mask
        & (hue >= 0.18)
        & (hue <= 0.44)
        & (sat >= 0.20)
        & (exg > 15.0)
        & (gn > rn * 1.08)
        & (gn > bn * 1.15)
    )

    # A. Active Necrosis & Scorch (dead cell collapse, bacterial blight, brown hopper burns)
    necrosis_mask = cleaned_leaf_mask & ~healthy_tissue & (
        # Dark sunken brown/black lesions
        ((val < 0.35) & (cleaned_leaf_mask)) |
        # High red-to-green necrosis
        ((rn > 0.40) & (gn < 0.32) & (r > g * 1.2)) |
        # Tan/dry blight margin
        ((hue < 0.12) & (sat > 0.22) & (exg < -10.0) & (r > b * 1.25))
    )

    # B. Chlorotic Halos & Yellowing (early viral curl, sucking pest damage, nutrient halo)
    chlorosis_mask = cleaned_leaf_mask & ~healthy_tissue & ~necrosis_mask & (
        (hue >= 0.08) & (hue <= 0.18) & (sat >= 0.20) & (g > b * 1.10) & (val > 0.35)
    )

    # Total combined lesion footprint
    combined_lesion_mask = (necrosis_mask | chlorosis_mask) & cleaned_leaf_mask

    # Morphological filtering on lesions: remove single-pixel sensor noise
    combined_lesion_mask = ndi.binary_opening(combined_lesion_mask, structure=struct, iterations=1)
    necrosis_mask = necrosis_mask & combined_lesion_mask
    chlorosis_mask = chlorosis_mask & combined_lesion_mask

    lesion_pixels = int(np.sum(combined_lesion_mask))
    healthy_pixels = int(np.sum(healthy_tissue & ~combined_lesion_mask))

    # Quantitative area ratios
    raw_lesion_pct = (float(lesion_pixels) / max(1.0, float(total_leaf_pixels))) * 100.0
    lesion_percentage = round(float(np.clip(raw_lesion_pct, 0.4, 98.0)), 1)

    raw_health_pct = (float(healthy_pixels) / max(1.0, float(total_leaf_pixels))) * 100.0
    photosynthetic_health = round(float(np.clip(raw_health_pct, 2.0, 99.5)), 1)

    # 3. Leaf Stage Classification (Stage 1, Stage 2, Stage 3)
    if lesion_percentage < 10.0:
        leaf_stage_num = 1
        leaf_stage_title = "Stage 1: Initial / Incubation Phase"
        leaf_stage_desc = (
            "Mild localized chlorosis, pinprick water-soaked lesions, or faint early specks (<10% foliar area). "
            "Primary vascular leaf framework and photosynthetic capacity remain mostly intact."
        )
        severity_color = "#28a745"
        severity_label = "Low / Early"
    elif lesion_percentage <= 30.0:
        leaf_stage_num = 2
        leaf_stage_title = "Stage 2: Medium / Active Foliar Expansion"
        leaf_stage_desc = (
            "Active expanding necrotic lesions, distinct chlorotic halos, or coalescing patches (10% - 30% foliar area). "
            "Noticeable impairment of photosynthesis and early canopy stress."
        )
        severity_color = "#fd7e14"
        severity_label = "Moderate / Active"
    else:
        leaf_stage_num = 3
        leaf_stage_title = "Stage 3: Advanced / Severe Blight & Breakdown"
        leaf_stage_desc = (
            "Extensive coalescing necrosis, tissue collapse, scorched leaf margins, or skeletonization (>30% foliar area). "
            "High risk of premature defoliation and severe yield loss."
        )
        severity_color = "#dc3545"
        severity_label = "Severe / Critical"

    # 4. Generate High-Fidelity Continuous Thermal Heatmap
    # Build continuous scalar intensity field
    intensity_field = np.zeros(work_size, dtype=np.float32)
    # Healthy background = low intensity
    intensity_field[cleaned_leaf_mask] = 0.05
    # Chlorotic halos = medium intensity
    intensity_field[chlorosis_mask] = 0.45
    # Necrotic lesion cores = high intensity
    intensity_field[necrosis_mask] = 0.95

    # Smooth the intensity field with Gaussian diffusion filter for thermal dispersion
    smoothed_heat = ndi.gaussian_filter(intensity_field, sigma=3.2)
    smoothed_heat = np.clip(smoothed_heat, 0.0, 1.0)
    # Confine to leaf canopy mask
    smoothed_heat[~cleaned_leaf_mask] = 0.0

    # Colorize using thermal gradient
    thermal_rgb = _apply_thermal_colormap(smoothed_heat)

    # Edge detection for lesion boundary contour lines
    lesion_dilated = ndi.binary_dilation(combined_lesion_mask, structure=struct, iterations=1)
    lesion_contours = lesion_dilated & ~combined_lesion_mask & cleaned_leaf_mask

    # Alpha blending: 55% Original leaf texture + 45% Thermal Heatmap for optimal clarity
    orig_np = np.array(img_rgb, dtype=np.float32)
    blend_np = orig_np.copy()

    # Blend thermal heatmap over leaf tissue
    leaf_indices = cleaned_leaf_mask
    blend_np[leaf_indices] = (
        orig_np[leaf_indices] * 0.48 + thermal_rgb[leaf_indices] * 0.52
    )

    # Highlight contour outlines in high-visibility bright cyan/yellow
    blend_np[lesion_contours, 0] = 255.0
    blend_np[lesion_contours, 1] = 235.0
    blend_np[lesion_contours, 2] = 50.0

    # Dim background slightly to focus attention on leaf
    bg_indices = ~cleaned_leaf_mask
    blend_np[bg_indices] = orig_np[bg_indices] * 0.45

    overlay_img = Image.fromarray(np.clip(blend_np, 0, 255).astype(np.uint8))

    # 5. Composite HUD Header and Footer Banners
    banner_height = 44
    header_height = 28
    canvas_w = work_size[0]
    canvas_h = work_size[1] + banner_height + header_height
    canvas = Image.new("RGB", (canvas_w, canvas_h), color=(18, 24, 20))
    canvas.paste(overlay_img, (0, header_height))
    draw = ImageDraw.Draw(canvas)

    # Top HUD Bar: Real-time segmentation metrics
    draw.rectangle([0, 0, canvas_w, header_height], fill=(12, 16, 14))
    draw.text(
        (8, 6),
        f"🔬 CV SEGMENTATION: Lesion Area {lesion_percentage}% | Health {photosynthetic_health}%",
        fill=(220, 245, 230)
    )

    # Bottom Legend Banner
    bar_y = header_height + work_size[1]
    draw.rectangle([0, bar_y, canvas_w, canvas_h], fill=(22, 28, 24))

    # Legend elements:
    # Red: Necrotic Hotspot
    draw.rectangle([10, bar_y + 12, 22, bar_y + 24], fill=(220, 20, 60))
    draw.text((26, bar_y + 11), "Necrosis", fill=(240, 240, 240))

    # Yellow: Chlorotic Halo
    draw.rectangle([110, bar_y + 12, 122, bar_y + 24], fill=(255, 204, 0))
    draw.text((126, bar_y + 11), "Chlorosis", fill=(240, 240, 240))

    # Green: Healthy Tissue
    draw.rectangle([210, bar_y + 12, 222, bar_y + 24], fill=(46, 139, 87))
    draw.text((226, bar_y + 11), "Healthy Canopy", fill=(240, 240, 240))

    # Stage Badge Indicator
    badge_bg = (40, 167, 69) if leaf_stage_num == 1 else ((253, 126, 20) if leaf_stage_num == 2 else (220, 53, 69))
    draw.rectangle([canvas_w - 75, bar_y + 8, canvas_w - 8, bar_y + 28], fill=badge_bg)
    draw.text((canvas_w - 70, bar_y + 10), f"STAGE {leaf_stage_num}", fill=(255, 255, 255))

    return {
        "lesion_percentage": lesion_percentage,
        "photosynthetic_health": photosynthetic_health,
        "leaf_stage_num": leaf_stage_num,
        "leaf_stage_title": leaf_stage_title,
        "leaf_stage_desc": leaf_stage_desc,
        "severity_color": severity_color,
        "severity_label": severity_label,
        "visual_overlay": canvas
    }
