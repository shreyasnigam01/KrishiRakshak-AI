# safety/consumer_toxicology.py

CHEMICAL_TOXICOLOGY_REGISTRY = {
    "triflumezopyrim": {
        "class": "Mesoionic / Neonicotinoid-Related",
        "human_toxicity_level": "Moderate",
        "acute_symptoms": "Mild nausea, headache, dizziness, gastric discomfort.",
        "chronic_risks": "Low risk when PHI is maintained; prolonged high-dose exposure may induce liver metabolic stress.",
        "vulnerable_groups": "Pregnant women and nursing mothers should avoid unwashed produce.",
        "decontamination_method": "Wash thoroughly in running water; soak in 2% salt water for 10 minutes to remove surface residues."
    },
    "chlorantraniliprole": {
        "class": "Ryanoid / Anthranilic Diamide",
        "human_toxicity_level": "Very Low (High mammalian safety margin)",
        "acute_symptoms": "Low acute toxicity; potential mild eye or throat irritation upon direct contact.",
        "chronic_risks": "Minimal dietary risk; does not readily bioaccumulate in human adipose tissue.",
        "vulnerable_groups": "Standard hygienic washing recommended.",
        "decontamination_method": "Normal tap water washing removes systemic foliar residues."
    },
    "tricyclazole": {
        "class": "Triazole Fungicide",
        "human_toxicity_level": "Moderate (Strict Export Rejection Limits)",
        "acute_symptoms": "Nausea, skin sensitization, mucosal irritation, headache.",
        "chronic_risks": "Prolonged ingestion exceeding FSSAI MRL may cause renal and hepatic enzyme elevation.",
        "vulnerable_groups": "Children under 5 and individuals with pre-existing kidney disorders.",
        "decontamination_method": "Thorough washing followed by parboiling/milling removes significant hull residues."
    },
    "chlorpyrifos": {
        "class": "Organophosphate",
        "human_toxicity_level": "High (Acetylcholinesterase Inhibitor)",
        "acute_symptoms": "Abdominal cramps, vomiting, pinpoint pupils, muscle tremors, excessive sweating.",
        "chronic_risks": "Neurobehavioral impairment, neurodevelopmental delays in infants, memory deficits.",
        "vulnerable_groups": "Strictly hazardous for young children, developing fetuses, and pregnant women.",
        "decontamination_method": "Soak in warm 1% baking soda (sodium bicarbonate) solution for 15 minutes; peel skin completely."
    },
    "copper oxychloride": {
        "class": "Inorganic Copper Fungicide",
        "human_toxicity_level": "Moderate (Topical & Gastric Irritant)",
        "acute_symptoms": "Metallic taste in mouth, stomach irritation, vomiting, greenish stool discoloration.",
        "chronic_risks": "Chronic copper accumulation can induce hepatic stress and gastrointestinal inflammation.",
        "vulnerable_groups": "Individuals with Wilson's disease or chronic liver impairment.",
        "decontamination_method": "Surface wipe, vigorous mechanical washing under running water, and peeling."
    },
    "flonicamid": {
        "class": "Pyridinecarboxamide",
        "human_toxicity_level": "Low to Moderate",
        "acute_symptoms": "Mild mucosal dryness, transient headache if consumed in large quantities.",
        "chronic_risks": "Targeted insect behavior blocker; low human endocrine or carcinogenic risk profile.",
        "vulnerable_groups": "Standard washing protocols suffice.",
        "decontamination_method": "Rinse under running water for 60 seconds."
    }
}

def get_consumer_safety_profile(chemical_name: str) -> dict:
    """
    Matches any chemical name string to its toxicological profile.
    """
    clean = str(chemical_name).lower().strip()
    for key, data in CHEMICAL_TOXICOLOGY_REGISTRY.items():
        if key in clean:
            return data
            
    # Fallback profile for biologicals, cultural methods, or unspecified inputs
    if any(k in clean for k in ["deferred", "neem", "trichogramma", "not required", "unspecified"]):
        return {
            "class": "Bio-Organic / Non-Chemical Intervention",
            "human_toxicity_level": "Non-Toxic / Negligible Risk",
            "acute_symptoms": "No acute toxicity hazards associated with biological agents.",
            "chronic_risks": "Zero persistent synthetic chemical residue buildup in consumer diets.",
            "vulnerable_groups": "Safe for all consumer groups when standard food washing hygiene is maintained.",
            "decontamination_method": "Standard rinse under potable water prior to culinary preparation."
        }

    return {
        "class": "General Agricultural Chemical",
        "human_toxicity_level": "Indeterminate / Potentially Hazardous",
        "acute_symptoms": "Gastrointestinal distress, nausea, stomach pain, dizziness.",
        "chronic_risks": "Long-term consumption of unverified pesticide residues creates liver and kidney metabolic load.",
        "vulnerable_groups": "Infants, elderly individuals, and pregnant women.",
        "decontamination_method": "Wash produce vigorously under running tap water; peel edible skins wherever applicable."
    }