# ml/pathology_matrix.py

EXPANDED_PATHOLOGY_DB = {
    # ==================== COTTON ====================
    "bacterial_blight": {
        "crop": "Cotton",
        "scientific_name": "Xanthomonas citri pv. malvacearum",
        "pathogen_type": "Bacterial Pathogen",
        "detection_scale": {
            "microscopic_size": "0.4 - 0.6 µm width × 1.2 - 3.0 µm length (rod-shaped bacterium)",
            "macroscopic_lesion_range": "1 mm water-soaked specks to 4-10 mm angular foliar lesions"
        },
        "infection_stage": "Stage 2: Medium (Angular Leaf Spot to early Systemic Blackarm)",
        "stage_progression": {
            "initial": "Minute, 1-2 mm water-soaked angular leaf specks bounded by veins.",
            "medium": "Coalescing 3-8 mm dark-brown necrotic lesions spreading along petioles.",
            "late": "Stem girdling (Blackarm), 15-30 mm sunken cankers, boll rotting."
        },
        "crop_phenology_sync": "Squaring to early boll development (45 - 80 DAS)",
        "warning_threshold": "Economic Threshold Level (ETL): > 5-10% foliar canopy coverage across 20 sampled plants.",
        "management_alternatives": {
            "chemical_options": [
                {"name": "Copper Oxychloride 50% WP", "dosage": "2.5 g / Liter water (500 g / acre in 200L)"},
                {"name": "Streptocycline (Streptomycin + Tetracycline)", "dosage": "100 mg / Liter water (20 g / acre in 200L)"},
                {"name": "Kasugamycin 3% SL", "dosage": "2.0 ml / Liter water (400 ml / acre in 200L)"}
            ],
            "bio_organic_alternatives": [
                {"name": "Pseudomonas fluorescens 1% WP", "dosage": "10 g / Liter water (foliar spray)"},
                {"name": "Neem Seed Kernel Extract (NSKE 5%)", "dosage": "50 ml / Liter water"},
                {"name": "Cow urine fermented foliar broth (Jeevamrut)", "dosage": "100 ml / Liter water"}
            ]
        },
        "farmer_resources": {
            "kisan_call_center": "1800-180-1551 (Toll-free, 22 Official Languages)",
            "pesticide_dealers": "Licensed District Input Retailers & Block Primary Agricultural Credit Societies (PACS)",
            "water_tanker_lifeline": "Gram Panchayat Irrigation Tanker Desk / Sub-Divisional Agriculture Officer",
            "soil_testing_lab": "District Soil Testing & Plant Health Clinic (KVK)"
        }
    },

    "bollworm": {
        "crop": "Cotton",
        "scientific_name": "Helicoverpa armigera / Pectinophora gossypiella",
        "pathogen_type": "Lepidopteran Insect Pest",
        "detection_scale": {
            "microscopic_size": "Egg: 0.5 mm diameter; Early Larva: 1.5 - 3 mm length",
            "macroscopic_lesion_range": "Microscopic eggs (0.5 mm) & superficial foliar scraping (1 - 2 mm)"
        },
        "infection_stage": "Stage 1: Initial (Egg / 1st-2nd Instar Pre-Boring Phase)",
        "stage_progression": {
            "initial": "Eggs on bracts/leaves (0.5 mm); superficial foliar scraping (Active Early Detection).",
            "medium": "Larva entering bracteoles; flared squares visible (10-15% flared squares).",
            "late": "Internal hollowed-out bolls; rotted lint with exit bore holes."
        },
        "crop_phenology_sync": "Peak flowering to green boll maturation (60 - 110 DAS)",
        "warning_threshold": "⚠️ Early Warning: Larvae have not yet penetrated bolls/squares. This is the critical window for biocontrol.",
        "management_alternatives": {
            "chemical_options": [
                {"name": "Synthetic chemical intervention deferred", "dosage": "Not recommended prior to internal square entry (ETL not breached)"}
            ],
            "bio_organic_alternatives": [
                {"name": "Trichogramma egg parasitoid cards", "dosage": "3-4 cards / acre (release immediately)"},
                {"name": "Pheromone Traps", "dosage": "5 traps / acre to trap flying male adults and disrupt mating"},
                {"name": "Neem Seed Kernel Extract (NSKE 5%)", "dosage": "50 ml / Liter water (acts as an anti-feedant)"}
            ]
        },
        "farmer_resources": {
            "kisan_call_center": "1800-180-1551 (All regional languages)",
            "pesticide_dealers": "Block Agro-Service Centers / State Agro-Industries Outlets",
            "water_tanker_lifeline": "Taluka Krishi Adhikari Emergency Drip-Irrigation Assistance",
            "soil_testing_lab": "Central Institute for Cotton Research (CICR) Regional Extension Cell"
        }
    },

    "curl_virus": {
        "crop": "Cotton",
        "scientific_name": "Cotton Leaf Curl Multan Virus (CLCuMuV)",
        "pathogen_type": "Begomovirus (Whitefly-transmitted)",
        "detection_scale": {
            "microscopic_size": "Virion: 18 - 22 nm paired geminate particles",
            "macroscopic_lesion_range": "Leaf curling: 20 - 150 mm whole-leaf distortion; Enations: 2 - 10 mm"
        },
        "infection_stage": "Stage 2: Medium (Upward/Downward cupping, prominent vein thickening)",
        "stage_progression": {
            "initial": "Vein clearing and light green network on upper tender leaves.",
            "medium": "Downward leaf thickening, puckering, and enations (cups) beneath leaves.",
            "late": "Extreme stunting, suppressed branching, flower bud abortion."
        },
        "crop_phenology_sync": "Early vegetative to active canopy closure (30 - 75 DAS)",
        "warning_threshold": "ETL: 6 - 8 whitefly adults/leaf or appearance of initial vein clearing on 1% plants.",
        "management_alternatives": {
            "chemical_options": [
                {"name": "Diafenthiuron 50% WP", "dosage": "1.2 g / Liter water (250 g / acre in 200L)"},
                {"name": "Afidopyropen 50 g/L DC", "dosage": "2.0 ml / Liter water (400 ml / acre in 200L)"},
                {"name": "Pyriproxyfen 10% EC", "dosage": "2.0 ml / Liter water (400 ml / acre in 200L)"}
            ],
            "bio_organic_alternatives": [
                {"name": "Yellow Sticky Traps", "dosage": "10 - 12 traps / acre positioned 15 cm above canopy"},
                {"name": "Verticillium lecanii (Lecanicillium)", "dosage": "5 g / Liter water (1 kg / acre in 200L)"},
                {"name": "Azadirachtin 10,000 ppm (1%)", "dosage": "2.0 ml / Liter water (400 ml / acre in 200L)"}
            ]
        },
        "farmer_resources": {
            "kisan_call_center": "1800-180-1551 (Multilingual 24/7)",
            "pesticide_dealers": "Kisan Seva Kendras (District Agriculture Department)",
            "water_tanker_lifeline": "Rural Disaster Relief Water Cell",
            "soil_testing_lab": "State Agricultural University (SAU) Virology Diagnostic Lab"
        }
    },

    "herbicide_growth_damage": {
        "crop": "Cotton",
        "scientific_name": "Abiotic Chemical Phytotoxicity (2,4-D / Synthetic Auxin Drift)",
        "pathogen_type": "Abiotic Stressor",
        "detection_scale": {
            "microscopic_size": "Non-cellular chemical molecules (~221 Da molecular weight)",
            "macroscopic_lesion_range": "Affected leaves: 30 - 120 mm strap-shaped fan leaves"
        },
        "infection_stage": "Stage 1 to 2: Initial to Medium (Epinasty & Leaf Narrowing)",
        "stage_progression": {
            "initial": "Petiole twisting (epinasty) within 24-48 hours of herbicide drift.",
            "medium": "Strap-like leaf formation, feather-like veins, suppressed laminae.",
            "late": "Stem cracking, adventitious root formation, terminal meristem abortion."
        },
        "crop_phenology_sync": "Post-emergence weed-spraying window (20 - 55 DAS)",
        "warning_threshold": "Visual observation on > 2 consecutive rows adjacent to sprayed borders.",
        "management_alternatives": {
            "chemical_options": [
                {"name": "19:19:19 Water Soluble Fertilizer", "dosage": "5.0 g / Liter water (1 kg / acre in 200L)"},
                {"name": "Chelated Zinc (Zn-EDTA 12%)", "dosage": "1.0 g / Liter water (200 g / acre in 200L)"},
                {"name": "Gibberellic Acid (GA3 0.001%)", "dosage": "1.0 ml / Liter water (to break hormonal arrest)"}
            ],
            "bio_organic_alternatives": [
                {"name": "Humic Acid 12% liquid", "dosage": "3.0 ml / Liter water (soil drench / foliar)"},
                {"name": "Seaweed Extract (Ascophyllum nodosum)", "dosage": "2.0 ml / Liter water"},
                {"name": "Overhead water misting", "dosage": "500 L/acre clean wash if within 6 hours of drift"}
            ]
        },
        "farmer_resources": {
            "kisan_call_center": "1800-180-1551",
            "pesticide_dealers": "Block Agriculture Office Quality Control Inspector",
            "water_tanker_lifeline": "Local Canal Command Water User Association (WUA)",
            "soil_testing_lab": "District Agriculture Officer Plant Pathology & Residue Lab"
        }
    },

    "leaf_hopper_jassids": {
        "crop": "Cotton",
        "scientific_name": "Amrasca biguttula biguttula",
        "pathogen_type": "Hemipteran Sucking Pest",
        "detection_scale": {
            "microscopic_size": "Egg: 0.7 mm; Nymph: 0.9 - 1.8 mm",
            "macroscopic_lesion_range": "Adult: 2.5 - 3.2 mm; Foliar yellow/red margins: 10 - 50 mm"
        },
        "infection_stage": "Stage 2: Medium (Downward leaf cupping with yellow marginal borders)",
        "stage_progression": {
            "initial": "Nymphs feeding on lower epidermis; faint yellowing of leaf edges.",
            "medium": "Downward curling of margins, reddish-brown marginal necrosis (hopper burn).",
            "late": "Entire leaf turns bronzed/brown, brittle, and drops prematurely."
        },
        "crop_phenology_sync": "Early vegetative to peak flowering (30 - 85 DAS)",
        "warning_threshold": "ETL: 2 jassid nymphs or adults per leaf on 3rd-4th leaf from plant top.",
        "management_alternatives": {
            "chemical_options": [
                {"name": "Flonicamid 50% WG", "dosage": "0.35 g / Liter water (70 g / acre in 200L)"},
                {"name": "Thiamethoxam 25% WG", "dosage": "0.25 g / Liter water (50 g / acre in 200L)"},
                {"name": "Dinotefuran 20% SG", "dosage": "0.4 g / Liter water (80 g / acre in 200L)"}
            ],
            "bio_organic_alternatives": [
                {"name": "Neem Oil 10,000 ppm", "dosage": "2.5 ml / Liter water"},
                {"name": "Beauveria bassiana 1.15% WP", "dosage": "5.0 g / Liter water (1 kg / acre in 200L)"},
                {"name": "Yellow Sticky Traps", "dosage": "8 - 10 traps / acre"}
            ]
        },
        "farmer_resources": {
            "kisan_call_center": "1800-180-1551",
            "pesticide_dealers": "IFFCO / KRIBHCO Farmer Service Centers",
            "water_tanker_lifeline": "Panchayat Samiti Lift Irrigation Desk",
            "soil_testing_lab": "ICAR-CICR Krishi Vigyan Kendra"
        }
    },

    "leaf_redding": {
        "crop": "Cotton",
        "scientific_name": "Nutritional Stress / Anthocyanin Accumulation",
        "pathogen_type": "Physiological Disorder",
        "detection_scale": {
            "microscopic_size": "Cellular vacuolar pigment accumulation (anthocyanin)",
            "macroscopic_lesion_range": "30 - 150 mm broad interveinal foliar reddening"
        },
        "infection_stage": "Stage 2: Medium (Interveinal reddening with green veins)",
        "stage_progression": {
            "initial": "Pale chlorotic interveinal patches on mature middle-tier leaves.",
            "medium": "Pink to bright reddish-purple discoloration between veins.",
            "late": "Complete leaf bronzing, drying, and shedding; immature boll bursting."
        },
        "crop_phenology_sync": "Peak boll development to maturation (80 - 130 DAS)",
        "warning_threshold": "Visual reddening on > 15% of lower-middle canopy leaves.",
        "management_alternatives": {
            "chemical_options": [
                {"name": "Magnesium Sulfate (MgSO4)", "dosage": "10 g / Liter water (2 kg / acre in 200L)"},
                {"name": "Potassium Nitrate (13:00:45)", "dosage": "10 g / Liter water (2 kg / acre in 200L)"},
                {"name": "Urea (1%) foliar spray", "dosage": "10 g / Liter water (2 kg / acre in 200L)"}
            ],
            "bio_organic_alternatives": [
                {"name": "Wood ash aqueous extract", "dosage": "20 g / Liter water (rich in K and Mg)"},
                {"name": "Vermicompost tea foliar wash", "dosage": "100 ml / Liter water"},
                {"name": "Soil moisture conservation mulch", "dosage": "Spread straw mulch @ 2 tons/acre"}
            ]
        },
        "farmer_resources": {
            "kisan_call_center": "1800-180-1551",
            "pesticide_dealers": "Block Fertilizer Allotment Depot",
            "water_tanker_lifeline": "Emergency Farm Pond (Shet-Tale) Water Network",
            "soil_testing_lab": "District Soil Testing Laboratory"
        }
    },

    "leaf_variegation": {
        "crop": "Cotton",
        "scientific_name": "Somatic Plastid Chimera / Genetic Mosaicism",
        "pathogen_type": "Genetic Variation (Non-infectious)",
        "detection_scale": {
            "microscopic_size": "Chloroplast-deficient cell lineages",
            "macroscopic_lesion_range": "10 - 80 mm sectoral white/pale yellow patterns"
        },
        "infection_stage": "Non-pathological / Stable Genetic Trait",
        "stage_progression": {
            "initial": "Single sectoral white/cream streak on expanding leaf blade.",
            "medium": "Sharp mosaic borders separating green and albino tissue.",
            "late": "Persists on branch without spreading to new adjoining plants."
        },
        "crop_phenology_sync": "All vegetative stages",
        "warning_threshold": "None (Harmless condition; no intervention required).",
        "management_alternatives": {
            "chemical_options": [
                {"name": "No chemical application required", "dosage": "0 ml / L (Avoid pesticide misuse)"}
            ],
            "bio_organic_alternatives": [
                {"name": "Maintain standard NPK balanced nutrition", "dosage": "Standard package of practices"}
            ]
        },
        "farmer_resources": {
            "kisan_call_center": "1800-180-1551",
            "pesticide_dealers": "Not applicable",
            "water_tanker_lifeline": "Standard irrigation cycle",
            "soil_testing_lab": "SAU Genetics and Plant Breeding Division"
        }
    },

    "healthy": {
        "crop": "Cotton / Paddy",
        "scientific_name": "Intact Physiological Plant Canopy",
        "pathogen_type": "Normal Plant State",
        "detection_scale": {
            "microscopic_size": "Intact cell walls and stomatal complexes",
            "macroscopic_lesion_range": "0 mm (Zero lesion coverage)"
        },
        "infection_stage": "Disease-Free Baseline",
        "stage_progression": {
            "initial": "Healthy green foliage.",
            "medium": "Optimal photosynthetic activity.",
            "late": "Normal reproductive maturity."
        },
        "crop_phenology_sync": "All developmental phases",
        "warning_threshold": "0% infection detected.",
        "management_alternatives": {
            "chemical_options": [
                {"name": "Do not spray preventive broad-spectrum chemicals", "dosage": "0 ml / L"}
            ],
            "bio_organic_alternatives": [
                {"name": "Balanced nutrient maintenance & beneficial insect preservation", "dosage": "Routine care"}
            ]
        },
        "farmer_resources": {
            "kisan_call_center": "1800-180-1551",
            "pesticide_dealers": "Routine Certified Seed & Fertilizer Dealers",
            "water_tanker_lifeline": "Standard Irrigation Scheduling",
            "soil_testing_lab": "Periodic Annual Soil Health Card Assessment"
        }
    },

    # ==================== PADDY / RICE ====================
    "brown_planthopper": {
        "crop": "Paddy / Rice",
        "scientific_name": "Nilaparvata lugens",
        "pathogen_type": "Hemipteran Delphacid Pest",
        "detection_scale": {
            "microscopic_size": "Egg: 0.8 - 1.0 mm; Nymph: 0.6 - 2.5 mm",
            "macroscopic_lesion_range": "Isolated nymphs; early honeydew specks on stem base (1 - 3 mm)"
        },
        "infection_stage": "Stage 1: Initial (Early Nymph / Stem-Base Colonization)",
        "stage_progression": {
            "initial": "Eggs inside sheath; early nymphs gathering at stem base (Current Early Detection).",
            "medium": "Sticky honeydew, sooty mold, circular yellowing patches (ETL breach).",
            "late": "Complete drying and lodging ('Hopper Burn') over several meters."
        },
        "crop_phenology_sync": "Active tillering to milk stage (40 - 90 DAT)",
        "warning_threshold": "⚠️ Early Warning: Population is below critical hopper-burn threshold. Apply non-chemical prevention now.",
        "management_alternatives": {
            "chemical_options": [
                {"name": "Chemical sprays deferred", "dosage": "Not required at early stage; prevents destroying natural spider predators"}
            ],
            "bio_organic_alternatives": [
                {"name": "Alternate Wetting and Drying (AWD)", "dosage": "Drain standing field water for 3–4 days to desiccate early nymph clusters"},
                {"name": "Neem Oil (Azadirachtin 10,000 ppm)", "dosage": "2.5 ml / Liter water directed at the plant stem base"},
                {"name": "Conserve Wolf Spiders (Lycosa pseudoannulata)", "dosage": "Natural biological suppression active in field"}
            ]
        },
        "farmer_resources": {
            "kisan_call_center": "1800-180-1551 (Rice Agro-Advisory Helpline)",
            "pesticide_dealers": "Primary Agricultural Cooperative Societies (PACS)",
            "water_tanker_lifeline": "Canal Irrigation Executive Engineer Emergency Water Discharge Cell",
            "soil_testing_lab": "National Rice Research Institute (NRRI) / Regional Rice Station"
        }
    },

    "green_leafhopper": {
        "crop": "Paddy / Rice",
        "scientific_name": "Nephotettix virescens",
        "pathogen_type": "Hemipteran Cicadellid Vector",
        "detection_scale": {
            "microscopic_size": "Egg: 1.0 mm; Nymph: 1.2 - 2.8 mm",
            "macroscopic_lesion_range": "Adult: 3.5 - 5.0 mm bright green with black markings"
        },
        "infection_stage": "Stage 1 to 2: Initial to Medium (Foliar Sap Extraction & Tungro Risk)",
        "stage_progression": {
            "initial": "Nymphs and adults feed on leaf blades; slight yellowing of tips.",
            "medium": "Prominent yellow-orange discoloration, reduced tillering (vectoring Tungro).",
            "late": "Extreme stunting of hills and empty, sterile panicles."
        },
        "crop_phenology_sync": "Nursery to panicle initiation (20 - 65 DAT)",
        "warning_threshold": "ETL: 2 insects/hill in Tungro-endemic areas; 5 insects/hill in general fields.",
        "management_alternatives": {
            "chemical_options": [
                {"name": "Thiamethoxam 25% WG", "dosage": "0.25 g / Liter water (50 g / acre in 200L)"},
                {"name": "Buprofezin 25% SC", "dosage": "1.5 ml / Liter water (300 ml / acre in 200L)"},
                {"name": "Monocrotophos 36% SL (Restricted use)", "dosage": "1.5 ml / Liter water"}
            ],
            "bio_organic_alternatives": [
                {"name": "Light Traps", "dosage": "1 trap / acre (burn between 7 PM - 10 PM)"},
                {"name": "Neem Oil 3000 ppm", "dosage": "3.0 ml / Liter water"},
                {"name": "Mirid Bug (Cyrtorhinus lividipennis) preservation", "dosage": "Conserve in field bunds"}
            ]
        },
        "farmer_resources": {
            "kisan_call_center": "1800-180-1551",
            "pesticide_dealers": "Block Agricultural Office Supply Outlet",
            "water_tanker_lifeline": "Command Area Development Authority (CADA)",
            "soil_testing_lab": "District Agriculture Extension Center"
        }
    },

    "leaf_folder": {
        "crop": "Paddy / Rice",
        "scientific_name": "Cnaphalocrocis medinalis",
        "pathogen_type": "Lepidopteran Foliar Caterpillar",
        "detection_scale": {
            "microscopic_size": "Egg: 0.9 mm; Early Larva: 2.0 mm",
            "macroscopic_lesion_range": "Mature Larva: 12 - 20 mm; Folded leaf tube: 50 - 200 mm"
        },
        "infection_stage": "Stage 2: Medium (Tubular leaf stitching with white scraped streaks)",
        "stage_progression": {
            "initial": "Single leaf longitudinal folding; transparent whitish scrape marks.",
            "medium": "Multiple stitched leaves per hill; white papery canopy appearance.",
            "late": "Canopy scorching; reduction in functional photosynthetic flag leaves."
        },
        "crop_phenology_sync": "Tillering to active booting phase (30 - 75 DAT)",
        "warning_threshold": "ETL: 1-2 freshly folded damaged leaves per hill during tillering.",
        "management_alternatives": {
            "chemical_options": [
                {"name": "Flubendiamide 39.35% SC", "dosage": "0.25 ml / Liter water (50 ml / acre in 200L)"},
                {"name": "Chlorantraniliprole 18.5% SC", "dosage": "0.3 ml / Liter water (60 ml / acre in 200L)"},
                {"name": "Cartap Hydrochloride 50% SP", "dosage": "1.25 g / Liter water (250 g / acre in 200L)"}
            ],
            "bio_organic_alternatives": [
                {"name": "Trichogramma chilonis egg parasitoid", "dosage": "2-3 cards / acre (50,000 parasitized eggs/acre)"},
                {"name": "Manual thorn/coir rope dislodging", "dosage": "Drag rope across canopy before 10 AM to tear folds"},
                {"name": "Beauveria bassiana 1% WP", "dosage": "5.0 g / Liter water"}
            ]
        },
        "farmer_resources": {
            "kisan_call_center": "1800-180-1551",
            "pesticide_dealers": "Block Agro Chemicals Depot",
            "water_tanker_lifeline": "Minor Irrigation Division Emergency Desk",
            "soil_testing_lab": "State Rice Bio-Control Laboratory"
        }
    },

    "rice_bug": {
        "crop": "Paddy / Rice",
        "scientific_name": "Leptocorisa oratorius (Gundhi Bug)",
        "pathogen_type": "Hemipteran Grain Feeder",
        "detection_scale": {
            "microscopic_size": "Egg: 1.2 mm; Nymph: 2.0 - 7.0 mm",
            "macroscopic_lesion_range": "Adult: 14 - 17 mm slender body; Grain puncture mark: 0.5 mm"
        },
        "infection_stage": "Stage 2 to 3: Medium to Late (Milky Grain Extraction)",
        "stage_progression": {
            "initial": "Adults present on panicles during early morning/evening; foul odor.",
            "medium": "Stylet probing of milky grains; white/brown puncture spots on hulls.",
            "late": "Erect panicles with completely empty, chaffy grains (chitta/safed bali)."
        },
        "crop_phenology_sync": "Heading to milk/soft dough stage (75 - 105 DAT)",
        "warning_threshold": "ETL: 1-2 bugs per hill or 5 bugs / m² sweep net count.",
        "management_alternatives": {
            "chemical_options": [
                {"name": "Lambda-cyhalothrin 5% EC", "dosage": "1.0 ml / Liter water (200 ml / acre in 200L)"},
                {"name": "Malathion 5% Dust", "dosage": "10 kg / acre (dust during morning hours)"},
                {"name": "Deltamethrin 2.8% EC", "dosage": "0.75 ml / Liter water (150 ml / acre in 200L)"}
            ],
            "bio_organic_alternatives": [
                {"name": "Rotten meat/fish bait traps", "dosage": "5 baited traps / acre to trap feeding adults"},
                {"name": "Field bund weed sanitation", "dosage": "Clear wild Echinochloa grasses prior to panicle emergence"},
                {"name": "Neem Oil 10,000 ppm", "dosage": "2.5 ml / Liter water"}
            ]
        },
        "farmer_resources": {
            "kisan_call_center": "1800-180-1551",
            "pesticide_dealers": "District Cooperative Marketing Federation",
            "water_tanker_lifeline": "Gram Panchayat Water Supply Engineer",
            "soil_testing_lab": "Divisional Rice Quality Inspection Lab"
        }
    },

    "stem_borer": {
        "crop": "Paddy / Rice",
        "scientific_name": "Scirpophaga incertulas (Yellow Stem Borer)",
        "pathogen_type": "Lepidopteran Internal Stem Tunneler",
        "detection_scale": {
            "microscopic_size": "Egg mass: 5 - 8 mm (under buff hair felt); Larva: 1.5 - 20 mm",
            "macroscopic_lesion_range": "Exit hole: 1.5 - 2.5 mm; Dead central tiller: 200 - 800 mm"
        },
        "infection_stage": "Stage 2: Medium (Stem Tunnelling producing 'Dead Hearts')",
        "stage_progression": {
            "initial": "Egg masses with brownish anal tufts on leaf tips; tiny bore holes at sheath base.",
            "medium": "Larva feeds inside internodes; central shoot dries up ('Dead Heart' in vegetative stage).",
            "late": "Empty, bleached, erect white panicles ('White Earhead' at reproductive stage)."
        },
        "crop_phenology_sync": "Early tillering to flowering/heading stage (25 - 95 DAT)",
        "warning_threshold": "ETL: 1 egg mass/m² or 2-5% Dead Hearts in vegetative stage; 1-2% White Earheads.",
        "management_alternatives": {
            "chemical_options": [
                {"name": "Cartap Hydrochloride 4% GR", "dosage": "10 kg / acre broadcast in standing water"},
                {"name": "Chlorantraniliprole 0.4% GR", "dosage": "4 kg / acre broadcast"},
                {"name": "Chlorantraniliprole 18.5% SC", "dosage": "0.3 ml / Liter water (60 ml / acre in 200L foliar)"}
            ],
            "bio_organic_alternatives": [
                {"name": "Clip seedling tips before transplanting", "dosage": "Eliminates > 80% of seedbed egg masses"},
                {"name": "Trichogramma japonicum egg parasitoids", "dosage": "3-4 cards / acre (weekly from 30 DAT)"},
                {"name": "Pheromone Traps (Scirpophaga specific)", "dosage": "5 traps / acre with yellow rubber septa lures"}
            ]
        },
        "farmer_resources": {
            "kisan_call_center": "1800-180-1551",
            "pesticide_dealers": "Kisan Credit Card (KCC) Approved Agricultural Outlets",
            "water_tanker_lifeline": "Zilla Parishad Irrigation Assistance Cell",
            "soil_testing_lab": "State Biocontrol & Parasitoid Multiplication Unit"
        }
    },

    "whorl_maggot": {
        "crop": "Paddy / Rice",
        "scientific_name": "Hydrellia philippina",
        "pathogen_type": "Dipteran Foliar Maggot",
        "detection_scale": {
            "microscopic_size": "Egg: 0.6 mm cigar-shaped; Maggot: 1.0 - 4.5 mm transparent",
            "macroscopic_lesion_range": "Feeding pinholes and margin serrations: 2 - 25 mm"
        },
        "infection_stage": "Stage 1 to 2: Initial to Medium (Whorl Margin Scraping)",
        "stage_progression": {
            "initial": "Eggs on leaves floating on water; maggots bore into unopened central whorl.",
            "medium": "Unfolding leaves show ragged edges, pinhole perforations, and yellow bands.",
            "late": "Stunted tillers; leaves break under wind stress; delayed heading."
        },
        "crop_phenology_sync": "Seedling to early tillering stage (< 35 DAT)",
        "warning_threshold": "ETL: 20% damaged hills showing chewed foliar whorls up to 30 days after transplanting.",
        "management_alternatives": {
            "chemical_options": [
                {"name": "Chlorpyrifos 20% EC", "dosage": "2.0 ml / Liter water (400 ml / acre in 200L)"},
                {"name": "Carbofuran 3% CG", "dosage": "10 kg / acre granular application in shallow water"},
                {"name": "Fipronil 5% SC", "dosage": "2.0 ml / Liter water (400 ml / acre in 200L)"}
            ],
            "bio_organic_alternatives": [
                {"name": "Intermittent water draining", "dosage": "Drain standing water for 2-3 days during early establishment"},
                {"name": "Neem Cake application in soil", "dosage": "100 kg / acre applied at transplanting"},
                {"name": "Avoid standing water pools", "dosage": "Level field properly to prevent puddle formation"}
            ]
        },
        "farmer_resources": {
            "kisan_call_center": "1800-180-1551",
            "pesticide_dealers": "Taluka Agro-Input Distribution Societies",
            "water_tanker_lifeline": "Irrigation Sub-Division Control Room",
            "soil_testing_lab": "Regional Agricultural Research Station (RARS)"
        }
    }
}