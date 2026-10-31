# ml/lifecycle_db.py

LIFECYCLE_PROFILES = {
    # ==================== COTTON CLASSES ====================
    "bacterial_blight": {
        "crop": "Cotton",
        "organism_type": "Bacterial Pathogen (Xanthomonas citri pv. malvacearum)",
        "stages": [
            {
                "stage_name": "Inoculum Survival & Entry",
                "duration_days": "1 - 3 days",
                "thermal_requirement": "Base 12°C, optimal 30-35°C",
                "biological_process": "Bacteria enter through stomata, hydathodes, or micro-wounds created by wind/sand.",
                "vulnerability_window": "Seedling emergence & cotyledon stage",
                "targeted_intervention": "Delinting seed treatment with Vitavax/Streptocycline."
            },
            {
                "stage_name": "Angular Leaf Colonization",
                "duration_days": "5 - 8 days",
                "thermal_requirement": "120 - 150 Accumulated GDD",
                "biological_process": "Intercellular multiplication bounded by veinlets, producing water-soaked angular lesions.",
                "vulnerability_window": "Early vegetative growth",
                "targeted_intervention": "Copper Oxychloride (0.2%) + Streptocycline spray."
            },
            {
                "stage_name": "Systemic Vascular Spread (Blackarm)",
                "duration_days": "10 - 15 days",
                "thermal_requirement": "220 - 280 Accumulated GDD",
                "biological_process": "Bacteria advance down petioles into the main stem, forming dark lesions and girdling branches.",
                "vulnerability_window": "Peak squaring & canopy development",
                "targeted_intervention": "Sanitary pruning of infected twigs; suppress overhead sprinkler irrigation."
            },
            {
                "stage_name": "Boll Rot & Seed Transmission",
                "duration_days": "14 - 20 days",
                "thermal_requirement": "> 350 Accumulated GDD",
                "biological_process": "Direct infection of young bolls causing rotting, fiber staining, and seed embryo dormancy.",
                "vulnerability_window": "Boll maturation",
                "targeted_intervention": "Harvest separation; avoid using infected field lint for replanting."
            }
        ]
    },

    "bollworm": {
        "crop": "Cotton",
        "organism_type": "Lepidopteran Insect (Helicoverpa armigera / Pectinophora gossypiella)",
        "stages": [
            {
                "stage_name": "Egg (Oviposition)",
                "duration_days": "3 - 5 days",
                "thermal_requirement": "45 - 55 Accumulated GDD",
                "biological_process": "Female lays spherical, sculptured eggs singly on squares, young leaves, and bracteoles.",
                "vulnerability_window": "Squaring to early flowering",
                "targeted_intervention": "Deploy Trichogramma egg parasitoids; light/pheromone traps."
            },
            {
                "stage_name": "Early Instar Larva (1st - 2nd)",
                "duration_days": "4 - 6 days",
                "thermal_requirement": "70 - 90 Accumulated GDD",
                "biological_process": "Larvae feed externally on tender foliage and square bracts before boring inside.",
                "vulnerability_window": "Pre-boring window (Crucial IPM Stage)",
                "targeted_intervention": "Neem oil / Azadirachtin or Bacillus thuringiensis (Bt) foliar spray."
            },
            {
                "stage_name": "Late Instar Larva (3rd - 5th)",
                "duration_days": "10 - 14 days",
                "thermal_requirement": "160 - 200 Accumulated GDD",
                "biological_process": "Internal feeding inside bolls/squares, causing flaring of bracts and boll dropping.",
                "vulnerability_window": "Internal destructive phase",
                "targeted_intervention": "Chlorantraniliprole 18.5% SC or Emamectin Benzoate 5% SG."
            },
            {
                "stage_name": "Pupation & Adult Emergence",
                "duration_days": "8 - 12 days",
                "thermal_requirement": "130 - 160 Accumulated GDD",
                "biological_process": "Larvae drop to ground and pupate in earthen cells 5-10 cm beneath the soil surface.",
                "vulnerability_window": "Post-harvest / soil stage",
                "targeted_intervention": "Deep summer plowing to expose pupae to predatory birds and solar heat."
            }
        ]
    },

    "curl_virus": {
        "crop": "Cotton",
        "organism_type": "Viral Complex (Cotton Leaf Curl Multan Virus - CLCuMuV)",
        "stages": [
            {
                "stage_name": "Vector Acquisition & Inoculation",
                "duration_days": "4 - 8 hours",
                "thermal_requirement": "Optimal 32-38°C for whitefly activity",
                "biological_process": "Bemisia tabaci (whitefly) feeds on infected sap, acquiring virus persistent-circulatively.",
                "vulnerability_window": "Early vegetative stage (up to 60 DAS)",
                "targeted_intervention": "Yellow sticky traps; eliminate weed hosts (Abutilon indicum)."
            },
            {
                "stage_name": "Systemic Phloem Translocation",
                "duration_days": "7 - 12 days",
                "thermal_requirement": "150 - 180 Accumulated GDD",
                "biological_process": "Viral DNA moves cell-to-cell via plasmodesmata to vascular tissues, disrupting auxin flow.",
                "vulnerability_window": "Pre-symptomatic phase",
                "targeted_intervention": "Systemic vector control (Diafenthiuron or Afidopyropen)."
            },
            {
                "stage_name": "Hyperplastic Symptom Expression",
                "duration_days": "14 - 30 days",
                "thermal_requirement": "> 300 Accumulated GDD",
                "biological_process": "Vein thickening, upward/downward leaf curling, and foliar enations (leaf-like outgrowths).",
                "vulnerability_window": "Mid-vegetative canopy",
                "targeted_intervention": "Rogue out early-infected plants; apply foliar zinc and boron to mitigate stress."
            },
            {
                "stage_name": "Terminal Stunting & Yield Collapse",
                "duration_days": "Persistent throughout season",
                "thermal_requirement": "Continuous",
                "biological_process": "Internodal shortening, flower bud abortion, and severe suppression of sympodial branching.",
                "vulnerability_window": "Reproductive phase",
                "targeted_intervention": "Focus on protecting neighboring unaffected plots."
            }
        ]
    },

    "herbicide_growth_damage": {
        "crop": "Cotton",
        "organism_type": "Abiotic Chemical Injury (e.g., 2,4-D drift, Glyphosate exposure)",
        "stages": [
            {
                "stage_name": "Cuticular Absorption",
                "duration_days": "1 - 24 hours",
                "thermal_requirement": "High temp (>32°C) accelerates uptake",
                "biological_process": "Chemical droplet penetrates waxy leaf cuticle and enters spongy mesophyll cells.",
                "vulnerability_window": "Immediate post-application drift",
                "targeted_intervention": "Immediate overhead sprinkler wash if detected within 2-4 hours."
            },
            {
                "stage_name": "Epinastic Deformation",
                "duration_days": "2 - 5 days",
                "thermal_requirement": "Dependent on plant metabolic rate",
                "biological_process": "Auxin mimicry causes asymmetric petiole elongation, strap-shaped leaves, and fan-like venation.",
                "vulnerability_window": "Vegetative shoots",
                "targeted_intervention": "Foliar application of 1% Urea + 0.5% Zinc Sulfate to stimulate new flush."
            },
            {
                "stage_name": "Meristematic Arrest or Recovery",
                "duration_days": "7 - 18 days",
                "thermal_requirement": "> 180 GDD for compensatory nodes",
                "biological_process": "Terminal bud abortion or gradual metabolism of herbicide molecules via cytochrome P450 pathways.",
                "vulnerability_window": "Secondary branching nodes",
                "targeted_intervention": "Gibberellic Acid (GA3) @ 10-20 ppm to break chemical dormancy."
            }
        ]
    },

    "leaf_hopper_jassids": {
        "crop": "Cotton",
        "organism_type": "Hemipteran Sucking Insect (Amrasca biguttula biguttula)",
        "stages": [
            {
                "stage_name": "Egg (Endophytic Insertion)",
                "duration_days": "4 - 9 days",
                "thermal_requirement": "60 - 80 Accumulated GDD",
                "biological_process": "Eggs inserted inside leaf veins and midrib tissues on lower leaf surfaces.",
                "vulnerability_window": "Tender leaf flushing",
                "targeted_intervention": "Conserve predatory geocorid bugs and spiders."
            },
            {
                "stage_name": "Nymphal Stages (1st to 5th Instar)",
                "duration_days": "7 - 14 days",
                "thermal_requirement": "110 - 150 Accumulated GDD",
                "biological_process": "Wingless nymphs feed on lower epidermis, injecting toxic saliva and sucking phloem sap.",
                "vulnerability_window": "Peak hopper-burn risk",
                "targeted_intervention": "Flonicamid 50 WG @ 0.3 g/L or Thiamethoxam 25 WG @ 0.2 g/L."
            },
            {
                "stage_name": "Adult Stage",
                "duration_days": "20 - 35 days",
                "thermal_requirement": "> 200 Accumulated GDD",
                "biological_process": "Highly mobile wedge-shaped adults hop sideways; cause characteristic marginal yellowing and leaf cupping.",
                "vulnerability_window": "Canopy-wide dispersion",
                "targeted_intervention": "Yellow sticky traps; manage intercropped companion trap crops (okra/cowpea borders)."
            }
        ]
    },

    "leaf_redding": {
        "crop": "Cotton",
        "organism_type": "Physiological / Nutritional Anomaly (Anthocyanin Accumulation)",
        "stages": [
            {
                "stage_name": "Chlorophyll Degradation",
                "duration_days": "3 - 7 days",
                "thermal_requirement": "Sudden drop in night temp (<15°C) & high soil moisture tension",
                "biological_process": "Magnesium deficiency or cold stress halts chlorophyll synthesis in mature leaves.",
                "vulnerability_window": "Boll development / high nutrient sink demand",
                "targeted_intervention": "Foliar spray of 1% Magnesium Sulfate (MgSO4)."
            },
            {
                "stage_name": "Anthocyanin Biosynthesis",
                "duration_days": "7 - 12 days",
                "thermal_requirement": "Prolonged low thermal index",
                "biological_process": "Accumulation of cyanidin/anthocyanin pigments as a photoprotective mechanism, turning leaves crimson red.",
                "vulnerability_window": "Sub-terminal leaves",
                "targeted_intervention": "Foliar application of 19:19:19 water-soluble fertilizer (5 g/L) + MgSO4."
            },
            {
                "stage_name": "Premature Senescence & Shedding",
                "duration_days": "14 - 20 days",
                "thermal_requirement": "Continuous stress",
                "biological_process": "Foliar abscission layer forms; reduced photosynthetic canopy leads to bad boll opening (kawdi).",
                "vulnerability_window": "Pre-harvest canopy",
                "targeted_intervention": "Light irrigation to alleviate soil moisture deficit."
            }
        ]
    },

    "leaf_variegation": {
        "crop": "Cotton",
        "organism_type": "Genetic / Chimeric Plastid Anomaly",
        "stages": [
            {
                "stage_name": "Plastid Sector Partitioning",
                "duration_days": "Somatic lineage development",
                "thermal_requirement": "Non-thermal / Genetic mutation",
                "biological_process": "Unequal division of defective chloroplasts during cell division yields sectors lacking chlorophyll.",
                "vulnerability_window": "Vegetative shoot emergence",
                "targeted_intervention": "No chemical intervention needed; harmless non-pathogenic condition."
            },
            {
                "stage_name": "Mosaic Leaf Expansion",
                "duration_days": "Co-occurs with vegetative flush",
                "thermal_requirement": "Standard crop GDD",
                "biological_process": "Irregular white/pale yellow and dark green patches persist without necrosis or vein swelling.",
                "vulnerability_window": "All growth stages",
                "targeted_intervention": "Differentiate from viral disease to avoid unnecessary pesticide use."
            }
        ]
    },

    "healthy": {
        "crop": "Cotton / Paddy",
        "organism_type": "Physiologically Normal Crop Foliage",
        "stages": [
            {
                "stage_name": "Active Vegetative Assimilation",
                "duration_days": "Continuous across season",
                "thermal_requirement": "Target GDD according to variety",
                "biological_process": "Optimal photosystem II efficiency, balanced transpiration, and intact cuticular barrier.",
                "vulnerability_window": "Zero pathology threshold",
                "targeted_intervention": "Follow balanced NPK recommendation; scout weekly."
            }
        ]
    },

    # ==================== PADDY / RICE CLASSES ====================
    "brown_planthopper": {
        "crop": "Paddy / Rice",
        "organism_type": "Hemipteran Phloem Feeder (Nilaparvata lugens)",
        "stages": [
            {
                "stage_name": "Egg Stage",
                "duration_days": "6 - 9 days",
                "thermal_requirement": "80 - 105 Accumulated GDD",
                "biological_process": "Crescent-shaped eggs laid in straight clusters inside the leaf sheath near water line.",
                "vulnerability_window": "Tillering stage",
                "targeted_intervention": "Maintain Alternate Wetting & Drying (AWD) to desiccate egg clutches."
            },
            {
                "stage_name": "Nymphal Instars (1st - 5th)",
                "duration_days": "12 - 16 days",
                "thermal_requirement": "160 - 210 Accumulated GDD",
                "biological_process": "Gregarious feeding at the stem base; excretion of honeydew producing sooty mold.",
                "vulnerability_window": "Maximum tillering to panicle initiation (ETL: 5-10/hill)",
                "targeted_intervention": "Triflumezopyrim 10% SC @ 0.48 ml/L or Pymetrozine 50% WG @ 0.6 g/L."
            },
            {
                "stage_name": "Macropterous / Brachypterous Adult",
                "duration_days": "15 - 25 days",
                "thermal_requirement": "> 240 Accumulated GDD",
                "biological_process": "Winged forms migrate between fields; wingless forms breed rapidly, causing circular patches of lodging ('Hopper Burn').",
                "vulnerability_window": "Booting to grain filling",
                "targeted_intervention": "Form alleyways (1 foot gap every 2 meters) for aeration and sunlight penetration."
            }
        ]
    },

    "green_leafhopper": {
        "crop": "Paddy / Rice",
        "organism_type": "Hemipteran Vector (Nephotettix virescens)",
        "stages": [
            {
                "stage_name": "Egg Clutches",
                "duration_days": "5 - 8 days",
                "thermal_requirement": "65 - 85 Accumulated GDD",
                "biological_process": "Serrated ovipositor inserts eggs under epidermis of leaf sheaths.",
                "vulnerability_window": "Nursery to early tillering",
                "targeted_intervention": "Protect mirid bug (*Cyrtorhinus lividipennis*) populations."
            },
            {
                "stage_name": "Nymphal Stage",
                "duration_days": "13 - 18 days",
                "thermal_requirement": "140 - 180 Accumulated GDD",
                "biological_process": "Pale green nymphs feed on upper leaf blades; vector for Rice Tungro Spherical and Bacilliform Viruses.",
                "vulnerability_window": "Active tillering",
                "targeted_intervention": "Install light traps; neem-based sprays."
            },
            {
                "stage_name": "Adult Stage",
                "duration_days": "20 - 30 days",
                "thermal_requirement": "> 200 Accumulated GDD",
                "biological_process": "Active fliers with prominent black markings on wings; feed on leaf veins causing tip burning.",
                "vulnerability_window": "Booting stage",
                "targeted_intervention": "Dinotefuran 20% SG @ 0.4 g/L or Thiamethoxam 25% WG."
            }
        ]
    },

    "leaf_folder": {
        "crop": "Paddy / Rice",
        "organism_type": "Lepidopteran Foliar Pest (Cnaphalocrocis medinalis)",
        "stages": [
            {
                "stage_name": "Egg (Scale-like)",
                "duration_days": "3 - 5 days",
                "thermal_requirement": "50 - 65 Accumulated GDD",
                "biological_process": "Flat, oval eggs laid singly or in small groups on lower surface of leaves.",
                "vulnerability_window": "Early vegetative flush",
                "targeted_intervention": "Release Trichogramma chilonis @ 40,000/acre."
            },
            {
                "stage_name": "Larval Feeding (Foliar Folding)",
                "duration_days": "15 - 25 days",
                "thermal_requirement": "180 - 240 Accumulated GDD",
                "biological_process": "Larva spins silken threads to stitch leaf margins longitudinally; feeds on green mesophyll inside, leaving white transparent streaks.",
                "vulnerability_window": "Tillering to booting (ETL: 2 damaged leaves/hill)",
                "targeted_intervention": "Drag thorny brush/ropes across field to open leaf folds; apply Flubendiamide 39.35% SC @ 0.2 ml/L."
            },
            {
                "stage_name": "Pupation & Moth Flight",
                "duration_days": "6 - 10 days",
                "thermal_requirement": "100 - 130 Accumulated GDD",
                "biological_process": "Pupation inside folded leaf tubular retreat; yellowish-brown moths emerge with wavy wing bands.",
                "vulnerability_window": "Adult dispersal",
                "targeted_intervention": "Light traps to monitor adult swarm flushes."
            }
        ]
    },

    "rice_bug": {
        "crop": "Paddy / Rice",
        "organism_type": "Hemipteran Grain Feeder (Leptocorisa oratorius / Gundhi Bug)",
        "stages": [
            {
                "stage_name": "Egg Clusters",
                "duration_days": "5 - 7 days",
                "thermal_requirement": "70 - 90 Accumulated GDD",
                "biological_process": "Disc-shaped dark reddish-brown eggs laid in straight double rows on upper leaf surfaces.",
                "vulnerability_window": "Heading emergence",
                "targeted_intervention": "Hand-netting during early mornings."
            },
            {
                "stage_name": "Nymphal Instars",
                "duration_days": "15 - 20 days",
                "thermal_requirement": "170 - 220 Accumulated GDD",
                "biological_process": "Slender green nymphs emit defensive pungent odor; insert stylets into developing grains.",
                "vulnerability_window": "Milky stage (Extremely Critical Window)",
                "targeted_intervention": "Apply Malathion 5% dust @ 10 kg/acre or Lambda-cyhalothrin 5% EC during early morning."
            },
            {
                "stage_name": "Adult Grain Feeding",
                "duration_days": "30 - 50 days",
                "thermal_requirement": "> 300 Accumulated GDD",
                "biological_process": "Adults suck starchy milk from developing kernels, leaving empty chaffy grains with brown puncture spots.",
                "vulnerability_window": "Dough stage",
                "targeted_intervention": "Deploy rotten snail/crab meat baits; clean bunds of wild grassy weeds (Echinochloa)."
            }
        ]
    },

    "stem_borer": {
        "crop": "Paddy / Rice",
        "organism_type": "Lepidopteran Stem Tunneler (Scirpophaga incertulas / Yellow Stem Borer)",
        "stages": [
            {
                "stage_name": "Egg Mass with Buff Hair Felt",
                "duration_days": "5 - 8 days",
                "thermal_requirement": "75 - 95 Accumulated GDD",
                "biological_process": "Egg masses covered with brownish hairs from female anal tufts near leaf tips.",
                "vulnerability_window": "Seedbed / transplanted tillers",
                "targeted_intervention": "Clip seedling tips before transplanting to destroy egg masses."
            },
            {
                "stage_name": "Early Borer Penetration",
                "duration_days": "3 - 5 days",
                "thermal_requirement": "40 - 60 Accumulated GDD",
                "biological_process": "Newly hatched larvae bore between leaf sheath and stem before entering internodes.",
                "vulnerability_window": "Penetration window (Only chance for systemic contact)",
                "targeted_intervention": "Cartap Hydrochloride 4G @ 10 kg/acre or Chlorantraniliprole 0.4% GR @ 4 kg/acre."
            },
            {
                "stage_name": "Internal Vascular Tunnelling",
                "duration_days": "20 - 30 days",
                "thermal_requirement": "240 - 320 Accumulated GDD",
                "biological_process": "Larvae feed internally on stem pith: produces 'Dead Hearts' in vegetative stage and 'White Ears' (empty panicles) in flowering stage.",
                "vulnerability_window": "Internal irreversible stage",
                "targeted_intervention": "Release Trichogramma japonicum @ 40,000/acre at weekly intervals."
            },
            {
                "stage_name": "Pupation at Stem Base",
                "duration_days": "6 - 10 days",
                "thermal_requirement": "90 - 120 Accumulated GDD",
                "biological_process": "White silken cocoon spun inside tiller above water level with exit hole prepared for moth escape.",
                "vulnerability_window": "Pre-emergence",
                "targeted_intervention": "Stubble cutting at ground level and submergence after harvest."
            }
        ]
    },

    "whorl_maggot": {
        "crop": "Paddy / Rice",
        "organism_type": "Dipteran Foliar Pest (Hydrellia philippina)",
        "stages": [
            {
                "stage_name": "Egg (Cigar-shaped)",
                "duration_days": "2 - 4 days",
                "thermal_requirement": "30 - 45 Accumulated GDD",
                "biological_process": "Laid singly on leaves lying flat on standing irrigation water surfaces.",
                "vulnerability_window": "Early seedling establishment (<30 DAT)",
                "targeted_intervention": "Drain standing field water intermittently during early post-transplant."
            },
            {
                "stage_name": "Internal Maggot Mining",
                "duration_days": "10 - 15 days",
                "thermal_requirement": "120 - 160 Accumulated GDD",
                "biological_process": "Transparent maggots mine unopened central whorl leaves, producing ragged pinholes and yellow margins as leaves unfold.",
                "vulnerability_window": "Early vegetative growth",
                "targeted_intervention": "Chlorpyrifos 20% EC or broadcast granular Carbofuran 3G."
            },
            {
                "stage_name": "Pupation & Adult Fly Emergence",
                "duration_days": "7 - 10 days",
                "thermal_requirement": "90 - 110 Accumulated GDD",
                "biological_process": "Pupates within leaf sheath margins; small gray flies emerge and rest near water puddles.",
                "vulnerability_window": "Canopy closure",
                "targeted_intervention": "Damage ceases once vegetative canopy closes (>40 days after transplanting)."
            }
        ]
    }
}