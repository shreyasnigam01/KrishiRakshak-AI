"""
ml/stage_prescriptions.py
Comprehensive Stage-Specific Pest Lifecycle & Precise Pesticide Dosage Matrix
Covers Stage 1 (Initial), Stage 2 (Medium), and Stage 3 (Severe) for ALL 14 crop conditions.
"""

from typing import Dict, Any

STAGE_PRESCRIPTIONS: Dict[str, Dict[int, Dict[str, Any]]] = {
    # ==================== COTTON ====================
    "bacterial_blight": {
        1: {
            "pest_stage_name": "Inoculum Penetration & Water-Soaked Angular Specks",
            "pest_biological_process": "Xanthomonas bacteria enter through open stomata or wind micro-abrasions; micro-colonies form intercellularly in spongy mesophyll.",
            "etl_status": "Below ETL (< 5% foliar incidence) — Preventive Bio-Window Active",
            "vulnerability_window": "Seedling emergence to early squaring",
            "preventive_measures": [
                "Seed treatment with Pseudomonas fluorescens @ 10g/kg or hot water delinting.",
                "Avoid excessive overhead sprinkler irrigation during high atmospheric humidity.",
                "Ensure balanced nitrogen application; avoid excess urea which promotes succulent susceptible tissues.",
                "Spray prophylactic bio-fungicide (Trichoderma / Pseudomonas) before rainfall."
            ],
            "chemical_options": [
                {
                    "name": "Copper Oxychloride 50% WP + Streptocycline",
                    "dose_per_liter": "2.0 g COC + 50 mg Streptocycline / L water",
                    "dose_per_15l_pump": "30 g COC + 0.75 g Streptocycline per 15L tank",
                    "dose_per_acre": "400 g COC + 10 g Streptocycline in 200 L water / acre",
                    "phi_days": 14,
                    "timing": "Spray in early morning before high heat"
                }
            ],
            "bio_options": [
                {
                    "name": "Pseudomonas fluorescens 1% WP",
                    "dose_per_liter": "10 g / Liter water",
                    "dose_per_15l_pump": "150 g per 15L tank",
                    "dose_per_acre": "1.0 kg in 200 L water / acre",
                    "instructions": "Colonizes leaf surface to competitively exclude bacterial pathogen"
                },
                {
                    "name": "Fermented Cow Urine Broth (Jeevamrut)",
                    "dose_per_liter": "50 ml / Liter water",
                    "dose_per_15l_pump": "750 ml per 15L tank",
                    "dose_per_acre": "10 Liters in 200 L water / acre",
                    "instructions": "Natural antimicrobial organic foliar tonic"
                }
            ]
        },
        2: {
            "pest_stage_name": "Active Angular Leaf Spot & Petiole Water-Soaking",
            "pest_biological_process": "Bacteria rapidly proliferate bounded by leaf veinlets, forming angular brown necrotic lesions; advancing down petioles.",
            "etl_status": "ETL Reached (8 - 12% foliar canopy coverage) — Curative Action Mandatory",
            "vulnerability_window": "Active vegetative growth to mid-squaring",
            "preventive_measures": [
                "Remove and burn severely infected leaves to prevent secondary bacterial spread.",
                "Disinfect pruning tools and avoid mechanical field operations when canopy is wet.",
                "Maintain broad border rows and improve intra-row air circulation."
            ],
            "chemical_options": [
                {
                    "name": "Copper Oxychloride 50% WP + Streptocycline",
                    "dose_per_liter": "2.5 g COC + 100 mg Streptocycline / L water",
                    "dose_per_15l_pump": "37.5 g COC + 1.5 g Streptocycline per 15L tank",
                    "dose_per_acre": "500 g COC + 20 g Streptocycline in 200 L water / acre",
                    "phi_days": 14,
                    "timing": "Thorough coverage of both upper and lower leaf surfaces"
                },
                {
                    "name": "Kasugamycin 3% SL",
                    "dose_per_liter": "2.0 ml / Liter water",
                    "dose_per_15l_pump": "30 ml per 15L tank",
                    "dose_per_acre": "400 ml in 200 L water / acre",
                    "phi_days": 10,
                    "timing": "Systemic bactericide spray during cloud-free hours"
                }
            ],
            "bio_options": [
                {
                    "name": "Bacillus subtilis foliar formulation",
                    "dose_per_liter": "5 g / Liter water",
                    "dose_per_15l_pump": "75 g per 15L tank",
                    "dose_per_acre": "1.0 kg in 200 L water / acre",
                    "instructions": "Produces lipopeptide antibiotics that degrade bacterial cell walls"
                }
            ]
        },
        3: {
            "pest_stage_name": "Systemic Vascular Blackarm & Boll Canker Phase",
            "pest_biological_process": "Bacteria enter vascular xylem vessels, causing dark girdling lesions (blackarm) on branches, stem breakage, and direct boll rotting.",
            "etl_status": "Severe Outbreak (> 25% canopy damage + branch lesions) — Rescue Protocol",
            "vulnerability_window": "Peak boll development to boll opening",
            "preventive_measures": [
                "Sanitary field rogueing: cut out and deeply bury blackarm-girdled branches.",
                "Immediately cease overhead watering; switch to furrow or drip irrigation.",
                "Segregate harvested lint; do not save seed from this plot for the next sowing season."
            ],
            "chemical_options": [
                {
                    "name": "Copper Hydroxide 53.8% DF + Streptocycline",
                    "dose_per_liter": "2.0 g + 100 mg / L water",
                    "dose_per_15l_pump": "30 g + 1.5 g per 15L tank",
                    "dose_per_acre": "400 g + 20 g in 200 L water / acre",
                    "phi_days": 21,
                    "timing": "High pressure spray targeting stems, branches, and young bolls"
                }
            ],
            "bio_options": [
                {
                    "name": "Neem Oil 10,000 ppm + Copper soap",
                    "dose_per_liter": "3.0 ml / Liter water",
                    "dose_per_15l_pump": "45 ml per 15L tank",
                    "dose_per_acre": "600 ml in 200 L water / acre",
                    "instructions": "Helps seal micro-lesions and retards secondary bacterial exudation"
                }
            ]
        }
    },

    "bollworm": {
        1: {
            "pest_stage_name": "Stage 1: Egg / Oviposition & 1st Instar Pre-Boring Phase",
            "pest_biological_process": "Moths lay tiny 0.5 mm cream-white spherical eggs singly on leaves, squares, and young bracts. Newly hatched 1st instar larvae scrape leaf surface before boring.",
            "etl_status": "Crucial Biological Window (1 egg / plant or 5% flared squares) — Biocontrol Peak",
            "vulnerability_window": "Squaring to early flowering (45 - 70 DAS)",
            "preventive_measures": [
                "Install Gossyplure / Helilure pheromone traps @ 5 traps/acre immediately for adult moth trapping.",
                "Release Trichogramma bactrae / chilonis egg parasitoid cards @ 60,000 eggs/acre weekly.",
                "Maintain 5% non-Bt cotton refuge border rows around the field.",
                "Apply Neem Seed Kernel Extract (NSKE 5%) as an oviposition deterrent and anti-feedant."
            ],
            "chemical_options": [
                {
                    "name": "Synthetic chemicals deferred at this early stage",
                    "dose_per_liter": "0 ml / L (Preserve beneficial predatory insects & chrysoperla)",
                    "dose_per_15l_pump": "0 ml (Chemicals destroy natural predators in early stage)",
                    "dose_per_acre": "0 (Deploy pheromone traps & bio-parasitoids instead)",
                    "phi_days": 0,
                    "timing": "Reserve chemical insecticides until ETL is breached"
                }
            ],
            "bio_options": [
                {
                    "name": "Neem Seed Kernel Extract (NSKE 5%) or Azadirachtin 10,000 ppm",
                    "dose_per_liter": "2.5 ml / Liter water (or 50 ml NSKE / L)",
                    "dose_per_15l_pump": "37.5 ml Azadirachtin per 15L tank",
                    "dose_per_acre": "500 ml in 200 L water / acre",
                    "instructions": "Repels female moths and prevents newly hatched larvae from feeding"
                },
                {
                    "name": "Trichogramma bactrae Parasitoid Cards",
                    "dose_per_liter": "Not applicable (Field card staple)",
                    "dose_per_15l_pump": "Not applicable",
                    "dose_per_acre": "3 - 4 cards / acre (60,000 parasitized eggs)",
                    "instructions": "Staple cards underside middle leaves in early morning"
                }
            ]
        },
        2: {
            "pest_stage_name": "Stage 2: 2nd - 3rd Instar Larva Active Feeding & Square Boring",
            "pest_biological_process": "Larvae (8-15 mm) bore into squares and young bolls, resulting in 'flaring' of bracteoles, yellowing, and premature square drop.",
            "etl_status": "ETL Breached (10% flared squares or 1 larva/plant) — Curative Chemical Intervention",
            "vulnerability_window": "Mid-flowering to early boll formation (70 - 95 DAS)",
            "preventive_measures": [
                "Collect and destroy flared squares and dropped bolls from the soil daily.",
                "Increase pheromone trap density to 8 traps/acre to track flight peaks.",
                "Avoid spraying broad-spectrum pyrethroids which induce resurgence of whiteflies and mites."
            ],
            "chemical_options": [
                {
                    "name": "Chlorantraniliprole 18.5% SC (Coragen)",
                    "dose_per_liter": "0.3 ml / Liter water",
                    "dose_per_15l_pump": "4.5 ml per 15L tank",
                    "dose_per_acre": "60 ml in 200 L water / acre",
                    "phi_days": 14,
                    "timing": "Spray late afternoon; targets ryanodine receptors with high rainfastness"
                },
                {
                    "name": "Flubendiamide 39.35% SC (Fame)",
                    "dose_per_liter": "0.25 ml / Liter water",
                    "dose_per_15l_pump": "3.75 ml per 15L tank",
                    "dose_per_acre": "50 ml in 200 L water / acre",
                    "phi_days": 15,
                    "timing": "Fast stomach action paralyzing feeding within 2 hours"
                },
                {
                    "name": "Emamectin Benzoate 5% SG (Proclaim)",
                    "dose_per_liter": "0.4 g / Liter water",
                    "dose_per_15l_pump": "6.0 g per 15L tank",
                    "dose_per_acre": "80 g in 200 L water / acre",
                    "phi_days": 10,
                    "timing": "Penetrates leaf cuticle; highly effective against early instar larvae"
                }
            ],
            "bio_options": [
                {
                    "name": "Bacillus thuringiensis var. kurstaki (Bt 55,000 ITU/mg)",
                    "dose_per_liter": "2.0 g / Liter water",
                    "dose_per_15l_pump": "30 g per 15L tank",
                    "dose_per_acre": "400 g in 200 L water / acre",
                    "instructions": "Ingestion produces endotoxins that paralyze caterpillar digestive tract"
                }
            ]
        },
        3: {
            "pest_stage_name": "Stage 3: 4th - 5th Instar Internal Boll Destruction & Pupation Descent",
            "pest_biological_process": "Full grown larvae (25-35 mm) feed internally inside maturing bolls, hollowing out seed locules and staining lint with excreta, before dropping to soil to pupate.",
            "etl_status": "Severe Damage (> 20% damaged bolls) — Emergency Salvage & Soil Barrier",
            "vulnerability_window": "Late boll development to harvesting (95 - 140 DAS)",
            "preventive_measures": [
                "Carry out deep summer plowing immediately after harvest to expose overwintering pupae to predatory birds and solarization.",
                "Handpick and dispose of rotted/burrowed bolls to prevent adult emergence.",
                "Install light traps along field borders to suppress adult moth mating flights."
            ],
            "chemical_options": [
                {
                    "name": "Spinetoram 11.7% SC",
                    "dose_per_liter": "0.8 ml / Liter water",
                    "dose_per_15l_pump": "12 ml per 15L tank",
                    "dose_per_acre": "160 ml in 200 L water / acre",
                    "phi_days": 14,
                    "timing": "High-potency rescue insecticide with translaminar activity"
                },
                {
                    "name": "Chlorpyrifos 50% + Cypermethrin 5% EC",
                    "dose_per_liter": "2.0 ml / Liter water",
                    "dose_per_15l_pump": "30 ml per 15L tank",
                    "dose_per_acre": "400 ml in 200 L water / acre",
                    "phi_days": 21,
                    "timing": "Knockdown contact and fumigant action for mature escaping larvae"
                }
            ],
            "bio_options": [
                {
                    "name": "Metarhizium anisopliae (Entomopathogenic fungus)",
                    "dose_per_liter": "5.0 g / Liter water (directed at soil base)",
                    "dose_per_15l_pump": "75 g per 15L tank",
                    "dose_per_acre": "1.0 kg in 200 L water / acre (soil drench)",
                    "instructions": "Infects larvae entering soil and pupating in earthen chambers"
                }
            ]
        }
    },

    "brown_planthopper": {
        1: {
            "pest_stage_name": "Stage 1: Early Nymph / Stem-Base Aggregation Window",
            "pest_biological_process": "1st and 2nd instar nymphs (0.6 - 1.2 mm) congregate at the base of rice tillers just above standing water line, probing vascular bundles.",
            "etl_status": "Below ETL (1 - 5 nymphs/hill) — Alternate Wetting & Drying Window",
            "vulnerability_window": "Active tillering to panicle initiation (35 - 60 DAT)",
            "preventive_measures": [
                "Alternate Wetting and Drying (AWD): Drain standing water from the field for 3-4 days to desiccate early nymphs.",
                "Conserve native wolf spiders (Lycosa pseudoannulata) and mirid bugs (Cyrtorhinus) in field bunds.",
                "Avoid excessive split doses of urea; apply balanced potash (MOP) to harden stem cuticle.",
                "Create alleyways (skip 1 row every 2-3 meters) to increase sunlight penetration to the stem base."
            ],
            "chemical_options": [
                {
                    "name": "Chemical sprays deferred at this early stage",
                    "dose_per_liter": "0 ml / L (Preserve spider predators)",
                    "dose_per_15l_pump": "0 ml (Chemicals destroy wolf spiders and trigger resurgence)",
                    "dose_per_acre": "0 (Drain water and apply neem at stem base instead)",
                    "phi_days": 0,
                    "timing": "Chemical intervention deferred unless nymphs exceed 15-20/hill"
                }
            ],
            "bio_options": [
                {
                    "name": "Neem Oil 10,000 ppm (Azadirachtin)",
                    "dose_per_liter": "2.5 ml / Liter water",
                    "dose_per_15l_pump": "37.5 ml per 15L tank",
                    "dose_per_acre": "500 ml in 200 L water / acre",
                    "instructions": "Direct spray strictly at stem base near soil line, not on top canopy"
                }
            ]
        },
        2: {
            "pest_stage_name": "Stage 2: 3rd - 5th Nymph & Adult Sap Feeding (Honeydew Phase)",
            "pest_biological_process": "Heavy feeding removes huge volumes of phloem sap; copious sugary honeydew coats stems, leading to black sooty mold and early yellowing patches.",
            "etl_status": "ETL Breached (15 - 20 hoppers/hill) — Targeted Systemic Feeding Blocker Required",
            "vulnerability_window": "Panicle initiation to flowering / milking stage (60 - 85 DAT)",
            "preventive_measures": [
                "Immediately drain standing field water.",
                "Open alleyways by tying adjacent tillers to improve aeration and spray penetration.",
                "Direct spray nozzles strictly into the lower third of the rice canopy."
            ],
            "chemical_options": [
                {
                    "name": "Pymetrozine 50% WDG (Chess)",
                    "dose_per_liter": "0.6 g / Liter water",
                    "dose_per_15l_pump": "9.0 g per 15L tank",
                    "dose_per_acre": "120 g in 200 L water / acre",
                    "phi_days": 15,
                    "timing": "Permanently blocks stylet probing; insects starve within 48 hours"
                },
                {
                    "name": "Triflumezopyrim 10% SC (Pexalon)",
                    "dose_per_liter": "0.5 ml / Liter water",
                    "dose_per_15l_pump": "7.5 ml per 15L tank",
                    "dose_per_acre": "94 ml in 200 L water / acre",
                    "phi_days": 21,
                    "timing": "Single dose provides up to 21 days residual control at stem base"
                }
            ],
            "bio_options": [
                {
                    "name": "Verticillium lecanii 1.15% WP",
                    "dose_per_liter": "5.0 g / Liter water",
                    "dose_per_15l_pump": "75 g per 15L tank",
                    "dose_per_acre": "1.0 kg in 200 L water / acre",
                    "instructions": "High efficacy against sucking nymphs under dense wet canopy"
                }
            ]
        },
        3: {
            "pest_stage_name": "Stage 3: Severe 'Hopper Burn' & Circular Crop Lodging",
            "pest_biological_process": "Vascular collapse caused by massive sap extraction; circular patches of rice crop turn yellow, then golden-brown, dry out completely and collapse ('hopper burn'). Winged adults migrate to adjoining plots.",
            "etl_status": "Critical Disaster Outbreak (> 50 hoppers/hill, circular dead patches) — Containment Barrier",
            "vulnerability_window": "Milking to dough stage (80 - 105 DAT)",
            "preventive_measures": [
                "Establish a chemical barrier ring: spray a 5-meter boundary belt around the burned circle first to trap migrating hoppers.",
                "Drain water completely to stop nymphs floating to adjoining hills.",
                "Harvest surviving mature surrounding hills immediately to limit crop loss."
            ],
            "chemical_options": [
                {
                    "name": "Triflumezopyrim 10% SC + Pymetrozine 50% WDG",
                    "dose_per_liter": "0.5 ml + 0.5 g / L water",
                    "dose_per_15l_pump": "7.5 ml + 7.5 g per 15L tank",
                    "dose_per_acre": "100 ml + 100 g in 200 L water / acre",
                    "phi_days": 21,
                    "timing": "High volume spray (250 L/acre) directed straight into base of collapsed circles"
                }
            ],
            "bio_options": [
                {
                    "name": "Neem Oil 10,000 ppm + Garlic Extract",
                    "dose_per_liter": "5.0 ml / Liter water",
                    "dose_per_15l_pump": "75 ml per 15L tank",
                    "dose_per_acre": "1.0 L in 200 L water / acre",
                    "instructions": "Fumigant repellency to stop adult migration to undamaged plots"
                }
            ]
        }
    },

    "curl_virus": {
        1: {
            "pest_stage_name": "Stage 1: Whitefly Inoculation & Initial Vein Clearing",
            "pest_biological_process": "Bemisia tabaci (whitefly) vectors the virus into phloem during feeding; first symptoms appear as faint vein clearing on uppermost tender leaves.",
            "etl_status": "Below Foliar ETL, but Whitefly Vector ETL Active (> 5 whiteflies/leaf)",
            "vulnerability_window": "Early vegetative growth (20 - 45 DAS)",
            "preventive_measures": [
                "Install bright yellow sticky traps @ 10 - 12 traps/acre placed 15 cm above the crop canopy.",
                "Eliminate collateral weed hosts (Abutilon indicum, Parthenium) around field bunds.",
                "Intercrop with barrier crops (2-3 rows of maize, sorghum, or pearl millet) to intercept flying whiteflies.",
                "Spray Neem Seed Kernel Extract (NSKE 5%) or Azadirachtin to prevent whitefly egg laying."
            ],
            "chemical_options": [
                {
                    "name": "Pyriproxyfen 10% EC (Vector Nymph IGR)",
                    "dose_per_liter": "2.0 ml / Liter water",
                    "dose_per_15l_pump": "30 ml per 15L tank",
                    "dose_per_acre": "400 ml in 200 L water / acre",
                    "phi_days": 15,
                    "timing": "Inhibits whitefly egg hatching and nymph metamorphosis"
                }
            ],
            "bio_options": [
                {
                    "name": "Yellow Sticky Traps",
                    "dose_per_liter": "Not applicable",
                    "dose_per_15l_pump": "Not applicable",
                    "dose_per_acre": "10 - 12 traps / acre",
                    "instructions": "Position 15 cm above crop canopy to capture flying vector adults"
                },
                {
                    "name": "Azadirachtin 10,000 ppm (1%)",
                    "dose_per_liter": "2.0 ml / Liter water",
                    "dose_per_15l_pump": "30 ml per 15L tank",
                    "dose_per_acre": "400 ml in 200 L water / acre",
                    "instructions": "Anti-feedant and repellent against whitefly stylet insertion"
                }
            ]
        },
        2: {
            "pest_stage_name": "Stage 2: Vein Thickening & Upward/Downward Foliar Cupping",
            "pest_biological_process": "Viral DNA induces cellular hypertrophy; veins thicken prominently, leaf margins curl upward or downward, and small cup-like enations develop beneath leaves.",
            "etl_status": "Vector ETL Breached (8 - 10 whiteflies/leaf or 5% symptomatic plants) — Vector Knockdown",
            "vulnerability_window": "Active vegetative to squaring (45 - 75 DAS)",
            "preventive_measures": [
                "Rogue out and bury severely infected stunted plants if crop is under 50 days old.",
                "Apply micronutrient foliar spray (Zinc + Magnesium + Boron) to alleviate metabolic stress.",
                "Ensure uniform field spray coverage including the underside of leaves."
            ],
            "chemical_options": [
                {
                    "name": "Diafenthiuron 50% WP (Pegasus)",
                    "dose_per_liter": "1.2 g / Liter water",
                    "dose_per_15l_pump": "18 g per 15L tank",
                    "dose_per_acre": "250 g in 200 L water / acre",
                    "phi_days": 21,
                    "timing": "Photo-activated insecticide; spray when sunlight is present"
                },
                {
                    "name": "Afidopyropen 50 g/L DC (Sefina)",
                    "dose_per_liter": "2.0 ml / Liter water",
                    "dose_per_15l_pump": "30 ml per 15L tank",
                    "dose_per_acre": "400 ml in 200 L water / acre",
                    "phi_days": 14,
                    "timing": "Quickly halts whitefly feeding within 15 minutes of contact"
                }
            ],
            "bio_options": [
                {
                    "name": "Verticillium lecanii 1.15% WP",
                    "dose_per_liter": "5.0 g / Liter water",
                    "dose_per_15l_pump": "75 g per 15L tank",
                    "dose_per_acre": "1.0 kg in 200 L water / acre",
                    "instructions": "Targets whitefly nymphs and puparia"
                }
            ]
        },
        3: {
            "pest_stage_name": "Stage 3: Severe Foliar Puckering, Stunting & Bud Abortion",
            "pest_biological_process": "Total systemic disruption of auxin and gibberellin hormone transport; plant becomes severely stunted with shortened internodes, bushy appearance, and flower drop.",
            "etl_status": "Severe Viral Stunting (> 20% plants infected) — Growth Revival & Vector Suppression",
            "vulnerability_window": "Squaring to peak boll set (75 - 110 DAS)",
            "preventive_measures": [
                "Spray foliar booster (19:19:19 @ 5g/L + Micronutrients) to maintain yield from unaffected branches.",
                "Suppress remaining whitefly vectors to prevent migration into late-planted or neighboring fields.",
                "Plan next season with certified CLCuD-resistant hybrids."
            ],
            "chemical_options": [
                {
                    "name": "Spiromesifen 22.9% SC (Oberon)",
                    "dose_per_liter": "1.0 ml / Liter water",
                    "dose_per_15l_pump": "15 ml per 15L tank",
                    "dose_per_acre": "200 ml in 200 L water / acre",
                    "phi_days": 21,
                    "timing": "Lipid biosynthesis inhibitor targeting resistant whitefly populations"
                }
            ],
            "bio_options": [
                {
                    "name": "Seaweed Extract + Cow Milk Broth",
                    "dose_per_liter": "2.0 ml seaweed extract + 20 ml cow milk / L",
                    "dose_per_15l_pump": "30 ml seaweed + 300 ml cow milk per 15L tank",
                    "dose_per_acre": "400 ml seaweed in 200 L water / acre",
                    "instructions": "Milk proteins help bind viral particles; seaweed provides hormonal recovery"
                }
            ]
        }
    },

    "leaf_folder": {
        1: {
            "pest_stage_name": "Stage 1: Egg Mass & Early Leaf Shearing Phase",
            "pest_biological_process": "Adult moths lay disc-shaped translucent eggs singly or in pairs on the underside of young rice leaves; 1st instar larvae scrape chlorophyll along veins.",
            "etl_status": "Below ETL (< 1 folded leaf / hill) — Egg Parasitoid Release Phase",
            "vulnerability_window": "Early tillering (25 - 45 DAT)",
            "preventive_measures": [
                "Release Trichogramma chilonis egg parasitoid cards @ 50,000 eggs/acre.",
                "Drag a thorny bamboo branch or rough coir rope across the field before 10 AM to tear folds and expose larvae to sunlight.",
                "Avoid high nitrogen applications that create succulent foliage attractive to adult moths."
            ],
            "chemical_options": [
                {
                    "name": "Chemicals deferred at early stage",
                    "dose_per_liter": "0 ml / L (Encourage native predatory wasps and spiders)",
                    "dose_per_15l_pump": "0 ml",
                    "dose_per_acre": "0",
                    "phi_days": 0,
                    "timing": "Monitor twice weekly"
                }
            ],
            "bio_options": [
                {
                    "name": "Bacillus thuringiensis var. kurstaki (Bt)",
                    "dose_per_liter": "2.0 g / Liter water",
                    "dose_per_15l_pump": "30 g per 15L tank",
                    "dose_per_acre": "400 g in 200 L water / acre",
                    "instructions": "Effective on surface-feeding young larvae before tight leaf rolling"
                }
            ]
        },
        2: {
            "pest_stage_name": "Stage 2: Longitudinal Tubular Folding & Transparent Streaks",
            "pest_biological_process": "Larvae weave silk threads to stitch the two leaf margins together longitudinally, residing inside and scraping green mesophyll tissue, leaving white papery streaks.",
            "etl_status": "ETL Breached (1-2 freshly folded damaged leaves per hill) — Curative Action",
            "vulnerability_window": "Active tillering to booting (45 - 75 DAT)",
            "preventive_measures": [
                "Unfold damaged leaves manually where feasible and destroy caterpillars.",
                "Maintain clean field bunds free of grassy weeds (Echinochloa) that serve as secondary hosts.",
                "Ensure spray volume penetrates deeply into the folded leaves."
            ],
            "chemical_options": [
                {
                    "name": "Chlorantraniliprole 18.5% SC (Coragen)",
                    "dose_per_liter": "0.3 ml / Liter water",
                    "dose_per_15l_pump": "4.5 ml per 15L tank",
                    "dose_per_acre": "60 ml in 200 L water / acre",
                    "phi_days": 14,
                    "timing": "High rainfastness; paralyzes caterpillars inside tubes within hours"
                },
                {
                    "name": "Flubendiamide 39.35% SC (Fame)",
                    "dose_per_liter": "0.25 ml / Liter water",
                    "dose_per_15l_pump": "3.75 ml per 15L tank",
                    "dose_per_acre": "50 ml in 200 L water / acre",
                    "phi_days": 15,
                    "timing": "Translaminar penetration through woven leaf membranes"
                },
                {
                    "name": "Cartap Hydrochloride 50% SP",
                    "dose_per_liter": "1.25 g / Liter water",
                    "dose_per_15l_pump": "18.75 g per 15L tank",
                    "dose_per_acre": "250 g in 200 L water / acre",
                    "phi_days": 21,
                    "timing": "Systemic and contact action against caterpillars"
                }
            ],
            "bio_options": [
                {
                    "name": "Beauveria bassiana 1% WP",
                    "dose_per_liter": "5.0 g / Liter water",
                    "dose_per_15l_pump": "75 g per 15L tank",
                    "dose_per_acre": "1.0 kg in 200 L water / acre",
                    "instructions": "Spray during humid or overcast days to ensure fungal spore viability"
                }
            ]
        },
        3: {
            "pest_stage_name": "Stage 3: Severe Canopy Blanched Appearance & Flag Leaf Loss",
            "pest_biological_process": "Massive infestation where > 40% of leaves including critical flag leaves are folded and skeletonized; field looks scorched/white from a distance, severely reducing grain filling.",
            "etl_status": "Severe Canopy Destruction (> 30% damaged flag leaves) — Rescue Foliar Spray",
            "vulnerability_window": "Booting to heading (70 - 95 DAT)",
            "preventive_measures": [
                "Apply potassium nitrate (13:00:45 @ 10g/L) alongside insecticide to aid panicle grain filling.",
                "Ensure thorough high-volume spray (250 L water/acre).",
                "Cut and feed severely damaged non-flag leaves to livestock only after PHI period."
            ],
            "chemical_options": [
                {
                    "name": "Spinetoram 11.7% SC",
                    "dose_per_liter": "0.75 ml / Liter water",
                    "dose_per_15l_pump": "11.25 ml per 15L tank",
                    "dose_per_acre": "150 ml in 200 L water / acre",
                    "phi_days": 14,
                    "timing": "Rapid knockdown rescue insecticide"
                }
            ],
            "bio_options": [
                {
                    "name": "Azadirachtin 10,000 ppm + Bt kurstaki",
                    "dose_per_liter": "2.0 ml Azadirachtin + 2.0 g Bt / L water",
                    "dose_per_15l_pump": "30 ml + 30 g per 15L tank",
                    "dose_per_acre": "400 ml + 400 g in 200 L water / acre",
                    "instructions": "Dual action bio-cocktail"
                }
            ]
        }
    },

    "stem_borer": {
        1: {
            "pest_stage_name": "Stage 1: Egg Mass on Foliar Tips & Sheath Scraping",
            "pest_biological_process": "Moths deposit rounded egg masses covered with buff-colored hair felt on upper leaf tips; 1st instar larvae crawl down and scrape inside leaf sheaths.",
            "etl_status": "Below ETL (< 1 egg mass / m²) — Parasitoid & Clipping Phase",
            "vulnerability_window": "Nursery to early tillering (15 - 35 DAT)",
            "preventive_measures": [
                "Clip top 2-3 cm of rice seedling leaves before transplanting to eliminate > 80% of seedbed egg masses.",
                "Install yellow rubber septa pheromone traps @ 5 traps/acre.",
                "Release egg parasitoid Trichogramma japonicum @ 40,000/acre weekly."
            ],
            "chemical_options": [
                {
                    "name": "Preventive granular application deferred unless egg masses exceed ETL",
                    "dose_per_liter": "0 ml / L",
                    "dose_per_15l_pump": "0 ml",
                    "dose_per_acre": "0",
                    "phi_days": 0,
                    "timing": "Focus on seedling tip clipping"
                }
            ],
            "bio_options": [
                {
                    "name": "Trichogramma japonicum parasitoid cards",
                    "dose_per_liter": "Not applicable",
                    "dose_per_15l_pump": "Not applicable",
                    "dose_per_acre": "2 - 3 cards / acre",
                    "instructions": "Release weekly starting 20 days after transplanting"
                }
            ]
        },
        2: {
            "pest_stage_name": "Stage 2: Stem Internode Boring ('Dead Heart' Vegetative Phase)",
            "pest_biological_process": "Larvae bore into central tiller stems, severing vascular bundles. The central emerging shoot wilts, turns brown, and dies ('Dead Heart').",
            "etl_status": "ETL Breached (2-5% Dead Hearts at tillering) — Granular / Systemic Intervention",
            "vulnerability_window": "Active tillering to stem elongation (35 - 65 DAT)",
            "preventive_measures": [
                "Maintain 2-3 cm standing water in field when applying granular insecticides for uniform root uptake.",
                "Pull out dead hearts manually and destroy residing larvae.",
                "Avoid excessive water ponding that softens lower stem internodes."
            ],
            "chemical_options": [
                {
                    "name": "Cartap Hydrochloride 4% GR (Caldan)",
                    "dose_per_liter": "Broadcast granules in standing water",
                    "dose_per_15l_pump": "Not applicable (broadcast)",
                    "dose_per_acre": "10 kg / acre broadcast evenly",
                    "phi_days": 21,
                    "timing": "Broadcast when 2-3 cm standing water is present; hold water 3 days"
                },
                {
                    "name": "Chlorantraniliprole 0.4% GR (Ferterra)",
                    "dose_per_liter": "Broadcast granules in standing water",
                    "dose_per_15l_pump": "Not applicable (broadcast)",
                    "dose_per_acre": "4.0 kg / acre broadcast evenly",
                    "phi_days": 28,
                    "timing": "Absorbed through roots; provides 3-4 weeks systemic stem protection"
                },
                {
                    "name": "Chlorantraniliprole 18.5% SC (Coragen)",
                    "dose_per_liter": "0.3 ml / Liter water",
                    "dose_per_15l_pump": "4.5 ml per 15L tank",
                    "dose_per_acre": "60 ml in 200 L water / acre (foliar)",
                    "phi_days": 14,
                    "timing": "Foliar spray if water is not available for broadcasting granules"
                }
            ],
            "bio_options": [
                {
                    "name": "Bacillus thuringiensis var. kurstaki",
                    "dose_per_liter": "2.5 g / Liter water",
                    "dose_per_15l_pump": "37.5 g per 15L tank",
                    "dose_per_acre": "500 g in 200 L water / acre",
                    "instructions": "Direct spray at stem base to intercept newly boring larvae"
                }
            ]
        },
        3: {
            "pest_stage_name": "Stage 3: Peduncle Severing ('White Earhead' Reproductive Phase)",
            "pest_biological_process": "Larvae bore into the base of the panicle peduncle during flowering, resulting in bleached, erect, empty white panicles with zero grain filling ('White Earhead').",
            "etl_status": "Severe Reproductive Damage (1-2% White Earheads) — Emergency Containment",
            "vulnerability_window": "Booting to panicle heading (65 - 90 DAT)",
            "preventive_measures": [
                "White earheads are empty and cannot be cured; prevent remaining tillers from getting severed.",
                "Ensure proper disposal of rice stubbles after harvest by burning or deep rotavation.",
                "Avoid broad-spectrum pyrethroid sprays during flowering to protect pollinators."
            ],
            "chemical_options": [
                {
                    "name": "Fipronil 5% SC",
                    "dose_per_liter": "2.0 ml / Liter water",
                    "dose_per_15l_pump": "30 ml per 15L tank",
                    "dose_per_acre": "400 ml in 200 L water / acre",
                    "phi_days": 32,
                    "timing": "High volume foliar spray directed onto upper stem nodes"
                }
            ],
            "bio_options": [
                {
                    "name": "Neem Oil 10,000 ppm",
                    "dose_per_liter": "3.0 ml / Liter water",
                    "dose_per_15l_pump": "45 ml per 15L tank",
                    "dose_per_acre": "600 ml in 200 L water / acre",
                    "instructions": "Repellent and egg mortality enhancer"
                }
            ]
        }
    },

    "healthy": {
        1: {
            "pest_stage_name": "Zero Pathogen / Pest Presence — Pristine Plant State",
            "pest_biological_process": "Intact leaf epidermis, active stomatal gas exchange, and optimal chlorophyll photosynthesis.",
            "etl_status": "0% Infection — Preventive Natural Maintenance",
            "vulnerability_window": "All developmental phases",
            "preventive_measures": [
                "Maintain balanced N-P-K nutrient application according to soil health card.",
                "Avoid unnecessary preventive chemical sprays which destroy predatory insects.",
                "Scout weekly to spot any initial insect oviposition or foliar micro-spots early."
            ],
            "chemical_options": [
                {
                    "name": "No chemical pesticide required",
                    "dose_per_liter": "0 ml / L (Do not spray healthy crops)",
                    "dose_per_15l_pump": "0 ml",
                    "dose_per_acre": "0",
                    "phi_days": 0,
                    "timing": "Maintain regular agronomic care"
                }
            ],
            "bio_options": [
                {
                    "name": "Jeevamrut / Cow dung fermented tonic",
                    "dose_per_liter": "50 ml / Liter water",
                    "dose_per_15l_pump": "750 ml per 15L tank",
                    "dose_per_acre": "10 Liters / acre foliar spray",
                    "instructions": "Stimulates beneficial foliar and soil microbiomes"
                }
            ]
        },
        2: {
            "pest_stage_name": "Zero Pathogen / Pest Presence — Pristine Plant State",
            "pest_biological_process": "Normal physiological growth and flowering.",
            "etl_status": "0% Infection",
            "vulnerability_window": "All developmental phases",
            "preventive_measures": ["Continue routine irrigation and weed-free bund management."],
            "chemical_options": [{"name": "No chemical required", "dose_per_liter": "0 ml / L", "dose_per_15l_pump": "0 ml", "dose_per_acre": "0", "phi_days": 0, "timing": "N/A"}],
            "bio_options": [{"name": "Routine organic compost", "dose_per_liter": "N/A", "dose_per_15l_pump": "N/A", "dose_per_acre": "2 tons / acre", "instructions": "Soil health maintenance"}]
        },
        3: {
            "pest_stage_name": "Zero Pathogen / Pest Presence — Pristine Plant State",
            "pest_biological_process": "Normal ripening and maturation.",
            "etl_status": "0% Infection",
            "vulnerability_window": "All developmental phases",
            "preventive_measures": ["Harvest at physiological maturity."],
            "chemical_options": [{"name": "No chemical required", "dose_per_liter": "0 ml / L", "dose_per_15l_pump": "0 ml", "dose_per_acre": "0", "phi_days": 0, "timing": "N/A"}],
            "bio_options": [{"name": "Standard agronomic practices", "dose_per_liter": "N/A", "dose_per_15l_pump": "N/A", "dose_per_acre": "N/A", "instructions": "Routine care"}]
        }
    }
}

def get_stage_prescription(disease: str, stage_num: int) -> Dict[str, Any]:
    """
    Returns the stage-specific prescription for the given disease and stage number (1, 2, or 3).
    Falls back gracefully if the exact stage is not directly mapped.
    """
    stage_num = int(min(3, max(1, stage_num)))
    
    # 1. Direct lookup
    if disease in STAGE_PRESCRIPTIONS and stage_num in STAGE_PRESCRIPTIONS[disease]:
        return STAGE_PRESCRIPTIONS[disease][stage_num]
        
    # 2. Check if a parent key matches
    for k in STAGE_PRESCRIPTIONS:
        if k in disease or disease in k:
            if stage_num in STAGE_PRESCRIPTIONS[k]:
                return STAGE_PRESCRIPTIONS[k][stage_num]

    # 3. Dynamic agronomist prescription for secondary / abiotic / minor classes
    is_early = (stage_num == 1)
    is_late = (stage_num == 3)
    
    clean_name = disease.replace("_", " ").title()
    stage_title = "Initial / Early Incubation" if is_early else ("Advanced / Severe Blight" if is_late else "Moderate / Active Foliar Expansion")
    etl = "Below ETL — Prophylactic Bio-Control Window" if is_early else ("Severe Breach — Rescue Intervention" if is_late else "At ETL — Targeted Curative Action")
    
    return {
        "pest_stage_name": f"Stage {stage_num}: {stage_title}",
        "pest_biological_process": f"Foliar pathology for {clean_name} active at intensity stage {stage_num}.",
        "etl_status": etl,
        "vulnerability_window": "Active crop canopy phase",
        "preventive_measures": [
            f"Monitor {clean_name} progression weekly; check both leaf surfaces with a hand lens.",
            "Install sticky or pheromone monitoring traps @ 8 traps/acre.",
            "Ensure balanced fertilization and maintain optimal irrigation drainage.",
            "Rogue out and destroy severely diseased plant tissue."
        ],
        "chemical_options": [
            {
                "name": "Targeted Broad-Spectrum Formulation",
                "dose_per_liter": "1.5 - 2.0 ml or g / Liter water",
                "dose_per_15l_pump": "25 - 30 ml or g per 15L tank",
                "dose_per_acre": "350 - 400 ml or g in 200 L water / acre",
                "phi_days": 14,
                "timing": "Spray during calm morning (7-10 AM) or evening (4-6 PM) hours"
            }
        ],
        "bio_options": [
            {
                "name": "Neem Oil 10,000 ppm (Azadirachtin)",
                "dose_per_liter": "2.5 ml / Liter water",
                "dose_per_15l_pump": "37.5 ml per 15L tank",
                "dose_per_acre": "500 ml in 200 L water / acre",
                "instructions": "Natural repellent, anti-feedant, and oviposition deterrent"
            },
            {
                "name": "Trichoderma / Pseudomonas Bio-formulation",
                "dose_per_liter": "5.0 g / Liter water",
                "dose_per_15l_pump": "75 g per 15L tank",
                "dose_per_acre": "1.0 kg in 200 L water / acre",
                "instructions": "Competitive bio-antagonist suppresses foliar and soil pathogens"
            }
        ]
    }
