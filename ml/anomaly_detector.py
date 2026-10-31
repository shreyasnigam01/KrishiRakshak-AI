"""
ml/anomaly_detector.py
Multi-Tiered Agricultural Anomaly Detection Engine for KrishiRakshak
Detects:
1. Out-of-Distribution (OOD) Non-Crop Images (e.g., tools, vehicles, animals, skin, noise)
2. Novel / Unregistered Foliar Pathogens (diseases outside the 14 trained classes)
3. Severe Abiotic / Complex Physiological foliar anomalies (chemical burns, salinity, extreme deficiency)
"""

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from typing import Dict, Any

def detect_foliar_anomaly(
    image: Image.Image,
    logits: torch.Tensor,
    probabilities: torch.Tensor
) -> Dict[str, Any]:
    """
    Computes a multi-metric anomaly evaluation combining computer vision foliar validation,
    deep feature energy score, and logit Shannon entropy.
    """
    # 1. Computer Vision Foliar Validation
    # Analyze raw image for plant chromatic signatures
    work_img = image.convert("RGB").resize((256, 256), Image.Resampling.BILINEAR)
    arr = np.array(work_img, dtype=np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    sum_rgb = r + g + b + 1e-6
    
    rn = r / sum_rgb
    gn = g / sum_rgb
    bn = b / sum_rgb
    
    # Plant foliar signatures:
    # A. Active green chlorophyll tissue
    is_green = (gn > 0.34) & (g > r * 0.95) & (g > b * 1.05) & (sum_rgb > 50)
    # B. Chlorotic yellowing / yellow foliar tissue
    is_yellow_foliar = (rn > 0.32) & (gn > 0.32) & (bn < 0.32) & (g > b * 1.1)
    # C. Necrotic / Brown dry foliar tissue
    is_brown_foliar = (rn > 0.36) & (gn > 0.28) & (bn < 0.30) & (r > b * 1.15) & (sum_rgb < 450)
    
    foliar_pixels = np.sum(is_green | is_yellow_foliar | is_brown_foliar)
    total_pixels = 256 * 256
    foliar_ratio = float(foliar_pixels) / float(total_pixels)
    foliar_percentage = round(foliar_ratio * 100.0, 1)

    # 2. Deep Logit Metrics (Energy Score & Shannon Entropy)
    num_classes = logits.shape[1]
    max_p = torch.max(probabilities).item()
    
    # A. Free Energy Score: E(x) = -T * logsumexp(logits / T)
    T = 1.0
    energy = -float((T * torch.logsumexp(logits / T, dim=1)).item())
    
    # B. Normalized Shannon Entropy: H = -sum(p * log2(p)) / log2(K)
    entropy_raw = -float(torch.sum(probabilities * torch.log2(probabilities + 1e-12)).item())
    max_entropy = float(np.log2(num_classes))
    norm_entropy = float(np.clip(entropy_raw / max_entropy, 0.0, 1.0))
    
    # 3. Composite Anomaly Scoring (0 to 100)
    # Penalize low foliar content (Non-Plant OOD)
    if foliar_percentage < 8.0:
        foliar_anomaly_penalty = 60.0
    elif foliar_percentage < 18.0:
        foliar_anomaly_penalty = 30.0
    else:
        foliar_anomaly_penalty = 0.0

    # Penalize high entropy (dispersed, uncertain logits across classes)
    entropy_penalty = norm_entropy * 35.0
    
    # Penalize high energy (known samples typically have energy < -4.0)
    # e.g., energy = -2.5 is high uncertainty; energy = -5.5 is low uncertainty
    energy_penalty = float(np.clip((energy + 4.5) * 15.0, 0.0, 30.0))
    
    # Penalize low top-class confidence
    conf_penalty = float(np.clip((0.60 - max_p) * 40.0, 0.0, 30.0))
    
    raw_anomaly_score = foliar_anomaly_penalty + entropy_penalty + energy_penalty + conf_penalty
    anomaly_score = round(float(np.clip(raw_anomaly_score, 2.0, 99.0)), 1)

    # 4. Multi-Tier Classification
    if foliar_percentage < 8.0:
        anomaly_status = "OUT_OF_DISTRIBUTION"
        anomaly_type = "NON_PLANT_OOD"
        badge_label = "🔴 Non-Plant / Foreign Specimen"
        badge_color = "#dc3545"
        explanation = (
            f"The uploaded image contains only {foliar_percentage}% foliar plant signature. "
            "It does not appear to be an agricultural crop leaf (e.g. object, tool, animal, skin, or blank background)."
        )
        recommendation = (
            "Please upload a clear, focused photograph directly centered on an individual crop leaf (Cotton or Rice)."
        )
    elif anomaly_score > 60.0 or (norm_entropy > 0.70 and max_p < 0.35):
        anomaly_status = "OUT_OF_DISTRIBUTION"
        anomaly_type = "NOVEL_PATHOLOGY_UNREGISTERED"
        badge_label = "🔴 Novel / Unregistered Foliar Anomaly"
        badge_color = "#dc3545"
        explanation = (
            f"Foliar tissue detected ({foliar_percentage}%), but visual lesion pattern exhibits very high logit entropy "
            f"({round(norm_entropy * 100, 1)}%) and low energy activation ({round(energy, 2)}). "
            "The symptoms do not conform to any of the 14 standard trained pathogen classes."
        )
        recommendation = (
            "Suspected emerging pathogen, mutant disease strain, or exotic foliar condition. "
            "Isolate the affected plants and submit a physical fresh leaf sample to your nearest "
            "Krishi Vigyan Kendra (KVK) or State Agricultural University plant pathology laboratory for PCR diagnosis."
        )
    elif anomaly_score > 35.0 or (norm_entropy > 0.50):
        anomaly_status = "SUSPECTED_NOVEL_OR_ABIOTIC"
        anomaly_type = "COMPLEX_ABIOTIC_STRESS"
        badge_label = "🟡 Suspected Abiotic Stress / Secondary Complex"
        badge_color = "#fd7e14"
        explanation = (
            f"Specimen shows borderline atypical foliar characteristics (Entropy: {round(norm_entropy * 100, 1)}%). "
            "This often indicates non-pathogenic abiotic stress (such as chemical pesticide drift, nutrient imbalance like Zinc/Boron/Nitrogen deficiency, or soil salinity)."
        )
        recommendation = (
            "Cross-verify soil moisture and fertilizer history. Inspect leaf undersides with a 10x hand lens "
            "to rule out microscopic mite or thrips colonies. Test a balanced micronutrient foliar spray."
        )
    else:
        anomaly_status = "IN_DISTRIBUTION"
        anomaly_type = "NORMAL_CROP_FOLIAGE"
        badge_label = "🟢 Verified Crop Foliar Specimen"
        badge_color = "#28a745"
        explanation = (
            f"Specimen conforms to verified agricultural in-distribution patterns. "
            f"Foliar coverage: {foliar_percentage}%, Model Uncertainty Index: {round(norm_entropy * 100, 1)}%."
        )
        recommendation = (
            "Standard IPM diagnosis protocols apply. Follow the stage-specific chemical and biological prescriptions."
        )

    return {
        "anomaly_score": anomaly_score,
        "anomaly_status": anomaly_status,
        "anomaly_type": anomaly_type,
        "badge_label": badge_label,
        "badge_color": badge_color,
        "foliar_percentage": foliar_percentage,
        "energy_score": round(energy, 2),
        "entropy_index": round(norm_entropy * 100, 1),
        "confidence_level": round(max_p * 100, 1),
        "explanation": explanation,
        "recommendation": recommendation
    }
