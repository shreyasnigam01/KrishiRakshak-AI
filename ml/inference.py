import os
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image

from ml.stage_detector import analyze_leaf_lesions
from ml.stage_prescriptions import get_stage_prescription
from ml.anomaly_detector import detect_foliar_anomaly

# Determine best available device
DEVICE = torch.device(
    "mps" if torch.backends.mps.is_available() 
    else ("cuda" if torch.cuda.is_available() else "cpu")
)

# 1. Load class mapping (check both possible locations)
CLASS_MAPPING_PATHS = [
    "data/dataset/class_names.json",
    "data/class_names.json"
]

FALLBACK_14_CLASSES = [
    "bacterial_blight",
    "bollworm",
    "brown_planthopper",
    "curl_virus",
    "green_leafhopper",
    "healthy",
    "herbicide_growth_damage",
    "leaf_folder",
    "leaf_hopper_jassids",
    "leaf_redding",
    "leaf_variegation",
    "rice_bug",
    "stem_borer",
    "whorl_maggot"
]

CLASSES = None
for path in CLASS_MAPPING_PATHS:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                CLASSES = json.load(f)
                break
        except Exception:
            pass

if not CLASSES:
    CLASSES = FALLBACK_14_CLASSES

num_classes = len(CLASSES)

# 2. Built-in Plant-Pathogen Interaction (PPI) Knowledge Base
DEFAULT_KNOWLEDGE_BASE = {
    "bacterial_blight": {
        "crop": "Cotton",
        "pathogen_agent": "Xanthomonas citri pv. malvacearum",
        "trophic_type": "Hemibiotrophic",
        "entry_route": "Stomata and mechanical wind wounds",
        "key_r_genes": "B12, B4, B2 loci",
        "susceptible_stage": "Seedling emergence to active squaring",
        "biocontrol_ipm": [
            "Seed treatment with Pseudomonas fluorescens @ 10g/kg.",
            "Avoid excessive overhead sprinkler irrigation during high humidity.",
            "Spray Copper Oxychloride 50 WP (2.5 g/L) + Streptocycline (100 mg/L) if ETL exceeds."
        ],
        "resistant_cultivars": ["LHH-144", "Suraj", "PKV Rajat"]
    },
    "bollworm": {
        "crop": "Cotton",
        "pathogen_agent": "Helicoverpa armigera / Pectinophora gossypiella",
        "trophic_type": "Lepidopteran Internal Pod/Boll Feeder",
        "entry_route": "Oviposition on leaves, squares, and young bracts; surface scraping",
        "key_r_genes": "Stacked Cry1Ac + Cry2Ab (Bollgard II)",
        "susceptible_stage": "Squaring to boll formation (45 - 110 DAS)",
        "biocontrol_ipm": [
            "Install pheromone traps @ 5 traps/acre immediately for adult moth trapping.",
            "Release Trichogramma bactrae / chilonis egg parasitoid cards @ 60,000 eggs/acre.",
            "Apply Neem Seed Kernel Extract (NSKE 5%) or Azadirachtin 10,000 ppm @ 2.5 ml/L.",
            "Spray Chlorantraniliprole 18.5% SC @ 0.3 ml/L if flared squares exceed 10%."
        ],
        "resistant_cultivars": ["Non-Bt refuge line compliance", "Bt-II certified hybrids"]
    },
    "curl_virus": {
        "crop": "Cotton",
        "pathogen_agent": "Cotton Leaf Curl Multan Virus (CLCuMuV)",
        "trophic_type": "Biotrophic Geminivirus (Whitefly Transmitted)",
        "entry_route": "Stylet feeding via vector Bemisia tabaci into phloem",
        "key_r_genes": "Single dominant / complex modifier loci (e.g., C1-C6)",
        "susceptible_stage": "Early vegetative to peak canopy closure",
        "biocontrol_ipm": [
            "Install yellow sticky traps @ 10/acre to trap whiteflies.",
            "Spray Neem Seed Kernel Extract (NSKE 5%) or Azadirachtin 10,000 ppm @ 2 ml/L.",
            "Vector knockdown: Diafenthiuron 50% WP @ 1.2 g/L or Afidopyropen 50 g/L DC @ 2 ml/L."
        ],
        "resistant_cultivars": ["RS-2013", "FDK-124", "CICR-H1"]
    },
    "brown_planthopper": {
        "crop": "Paddy / Rice",
        "pathogen_agent": "Nilaparvata lugens (Brown Planthopper)",
        "trophic_type": "Phloem feeding homopteran (Stem-Base Colonization)",
        "entry_route": "Vascular bundle stylet probing at lower stem base near water level",
        "key_r_genes": "Bph3, Bph14, Bph18 loci",
        "susceptible_stage": "Tillering to milk/dough stage (40 - 90 DAT)",
        "biocontrol_ipm": [
            "Alternate Wetting and Drying (AWD): Drain standing water for 3-4 days to desiccate early nymphs.",
            "Conserve native wolf spiders (Lycosa pseudoannulata) and mirid bugs in bunds.",
            "Apply Neem Oil (Azadirachtin 10,000 ppm) @ 2.5 ml/L directed at stem base.",
            "Apply Pymetrozine 50% WDG @ 0.6 g/L or Triflumezopyrim 10% SC @ 0.5 ml/L if ETL breaches."
        ],
        "resistant_cultivars": ["IR-64 (tolerant)", "MTU-1010", "Swarna Sub-1"]
    },
    "leaf_folder": {
        "crop": "Paddy / Rice",
        "pathogen_agent": "Cnaphalocrocis medinalis (Rice Leaf Folder)",
        "trophic_type": "Lepidopteran Foliar Caterpillar",
        "entry_route": "Foliar epidermal feeding inside woven tubes",
        "key_r_genes": "Native polygenic resistance alleles",
        "susceptible_stage": "Active tillering to booting phase",
        "biocontrol_ipm": [
            "Release Trichogramma chilonis egg parasitoids @ 50,000/acre.",
            "Dislodge fold tubes using thorny branches before 10 AM.",
            "Apply Flubendiamide 39.35% SC @ 0.25 ml/L or Chlorantraniliprole 18.5% SC @ 0.3 ml/L."
        ],
        "resistant_cultivars": ["TKM-6", "IET-1444"]
    },
    "stem_borer": {
        "crop": "Paddy / Rice",
        "pathogen_agent": "Scirpophaga incertulas (Yellow Stem Borer)",
        "trophic_type": "Lepidopteran Internal Vascular Stem Tunneler",
        "entry_route": "Boring entry behind leaf sheath into central tiller",
        "key_r_genes": "Quantitative wild rice introgression lines",
        "susceptible_stage": "Tillering (Dead hearts) to Flowering (White ears)",
        "biocontrol_ipm": [
            "Clip seedling leaf tips before transplanting.",
            "Install yellow rubber septa pheromone traps @ 5 traps/acre.",
            "Apply Cartap Hydrochloride 4G granules @ 10 kg/acre or Chlorantraniliprole 0.4% GR."
        ],
        "resistant_cultivars": ["Ratna", "Vikas", "TKM-6"]
    },
    "healthy": {
        "crop": "Cotton / Paddy",
        "pathogen_agent": "None detected (Normal Physiological Tissue)",
        "trophic_type": "Intact Plant Cuticle & Photosynthetic Apparatus",
        "entry_route": "Not Applicable",
        "key_r_genes": "Intact native immune system",
        "susceptible_stage": "Maintain standard agronomic schedule",
        "biocontrol_ipm": [
            "Continue standard balanced N:P:K nutrient fertilization.",
            "Avoid prophylactic broad-spectrum insecticide sprays.",
            "Scout weekly for initial pest population threshold breaches."
        ],
        "resistant_cultivars": ["Current sown crop is in vigorous vegetative state"]
    }
}

# Merge external knowledge base if available
KNOWLEDGE_BASE = DEFAULT_KNOWLEDGE_BASE.copy()
KNOWLEDGE_BASE_PATH = "data/knowledge_base.json"
if os.path.exists(KNOWLEDGE_BASE_PATH):
    try:
        with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as f:
            external_kb = json.load(f)
            KNOWLEDGE_BASE.update(external_kb)
    except Exception:
        pass

# 3. Preprocessing Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 4. Initialize MobileNetV2 Architecture
model = models.mobilenet_v2(weights=None)
model.classifier = nn.Sequential(
    nn.Dropout(p=0.3),
    nn.Linear(model.last_channel, 256),
    nn.ReLU(inplace=True),
    nn.Dropout(p=0.2),
    nn.Linear(256, num_classes)
)

MODEL_PATH = "ml/model.pth"
if os.path.exists(MODEL_PATH):
    try:
        state_dict = torch.load(MODEL_PATH, map_location=DEVICE, weights_only=True)
        model.load_state_dict(state_dict)
    except Exception as err:
        print(f"Warning: Could not load exact weights from {MODEL_PATH}: {err}")

model.to(DEVICE)
model.eval()

# Calibrated confidence levels
CONFIDENCE_THRESHOLD = 0.30
EARLY_INCUBATION_THRESHOLD = 0.18

def run_inference(image: Image.Image, weather: dict = None):
    """
    Executes deep learning inference, quantitative computer vision lesion analysis,
    leaf damage stage detection, pest biological lifecycle determination,
    and stage-specific preventive measures & pesticide prescriptions.
    """
    # 1. Computer Vision Lesion & Foliar Stage Analysis
    cv_stage_data = analyze_leaf_lesions(image)
    leaf_stage_num = cv_stage_data["leaf_stage_num"]
    lesion_pct = cv_stage_data["lesion_percentage"]

    # 2. Deep Learning Pathogen Classification
    tensor = transform(image.convert("RGB")).unsqueeze(0).to(DEVICE)
    
    with torch.no_grad():
        outputs = model(tensor)
        probabilities = F.softmax(outputs, dim=1)[0]
        top_probs, top_indices = torch.topk(probabilities, k=min(3, len(CLASSES)))

    top_pred_idx = top_indices[0].item()
    max_prob = top_probs[0].item()
    confidence = round(max_prob * 100, 2)
    raw_class = CLASSES[top_pred_idx] if top_pred_idx < len(CLASSES) else f"class_{top_pred_idx}"

    # Build top 3 candidate predictions for explainability
    top3 = []
    for p, idx_val in zip(top_probs, top_indices):
        idx_i = idx_val.item()
        lbl = CLASSES[idx_i] if idx_i < len(CLASSES) else f"class_{idx_i}"
        top3.append({"label": lbl, "confidence": round(p.item() * 100, 1)})

    # 3. Multi-Tier Anomaly & Specimen Validity Check
    anomaly_data = detect_foliar_anomaly(image, outputs, probabilities.unsqueeze(0))

    if anomaly_data["anomaly_type"] == "NON_PLANT_OOD":
        status = "ANOMALY_NON_PLANT"
        disease_label = "Invalid Specimen (Non-Plant)"
        prescription = get_stage_prescription("unidentified", leaf_stage_num)
    elif anomaly_data["anomaly_type"] == "NOVEL_PATHOLOGY_UNREGISTERED":
        status = "ANOMALY_NOVEL_PATHOLOGY"
        disease_label = "Suspected Novel / Unregistered Pathology"
        prescription = get_stage_prescription("unidentified", leaf_stage_num)
    elif max_prob < EARLY_INCUBATION_THRESHOLD:
        status = "OUT_OF_SCOPE"
        disease_label = "Unidentified / Complex Anomaly"
        # Fallback stage prescription
        prescription = get_stage_prescription("unidentified", leaf_stage_num)
    elif max_prob < CONFIDENCE_THRESHOLD:
        # Subtle early micro-lesion or mild incubation symptom detected
        status = "EARLY_INCUBATION"
        disease_label = raw_class
        prescription = get_stage_prescription(raw_class, leaf_stage_num)
    else:
        status = "CONFIRMED"
        disease_label = raw_class
        prescription = get_stage_prescription(raw_class, leaf_stage_num)

    # 4. Integrate Plant-Pathogen Interaction (PPI) Profile
    details = KNOWLEDGE_BASE.get(raw_class, None)
    if not details:
        for k in KNOWLEDGE_BASE.keys():
            if k in raw_class or raw_class in k:
                details = KNOWLEDGE_BASE[k]
                break

    if not details:
        details = {
            "crop": "Cotton / Paddy Field Crop",
            "pathogen_agent": raw_class.replace("_", " ").title(),
            "trophic_type": "Parasitic Plant Colonizer",
            "entry_route": "Foliar Stomata or Epidermal Puncture",
            "key_r_genes": "Native Basal Immunity Loci",
            "susceptible_stage": "Vegetative to canopy development",
            "biocontrol_ipm": [
                "Deploy sticky/pheromone monitoring traps @ 8 traps/acre.",
                "Apply recommended biological bio-pesticides (Neem/Trichoderma).",
                "Maintain clean field borders to remove collateral weed hosts."
            ],
            "resistant_cultivars": ["ICAR/SAU recommended regional certified varieties"]
        }

    return {
        "status": status,
        "disease_label": disease_label,
        "raw_class": raw_class,
        "confidence": confidence,
        "top3": top3,
        # Foliar stage & lesion metrics from Computer Vision
        "leaf_stage": {
            "stage_num": leaf_stage_num,
            "title": cv_stage_data["leaf_stage_title"],
            "description": cv_stage_data["leaf_stage_desc"],
            "lesion_percentage": lesion_pct,
            "photosynthetic_health": cv_stage_data["photosynthetic_health"],
            "severity_color": cv_stage_data["severity_color"],
            "severity_label": cv_stage_data["severity_label"],
        },
        # Pest biological lifecycle stage
        "pest_stage": {
            "stage_name": prescription["pest_stage_name"],
            "biological_process": prescription["pest_biological_process"],
            "etl_status": prescription["etl_status"],
            "vulnerability_window": prescription["vulnerability_window"]
        },
        # Actionable treatments for this stage
        "preventive_measures": prescription["preventive_measures"],
        "chemical_options": prescription["chemical_options"],
        "bio_options": prescription["bio_options"],
        # Visual diagnostic segmentation heatmap
        "visual_overlay": cv_stage_data["visual_overlay"],
        # Specimen validity and anomaly detection
        "anomaly": anomaly_data,
        "details": details
    }