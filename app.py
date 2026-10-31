import re
import os
import requests
import pandas as pd
from PIL import Image
import streamlit as st

from datetime import datetime
import streamlit.components.v1 as components

from ml.lifecycle_db import LIFECYCLE_PROFILES
from ml.pathology_matrix import EXPANDED_PATHOLOGY_DB
from ml.inference import run_inference
from backend.weather_service import fetch_current_weather, calculate_daily_gdd
from backend.alert_service import evaluate_outbreak_cluster
from backend.chatbot_engine import generate_chat_response, QUICK_CHIPS
from backend.gemini_service import diagnose_with_gemini, chat_with_gemini, test_gemini_connection
from backend.report_generator import generate_advisory_html
from safety.consumer_toxicology import get_consumer_safety_profile

# Auto-load .env file if present
_env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env_path):
    try:
        with open(_env_path, "r", encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    _k, _v = _k.strip(), _v.strip().strip("'\"")
                    if _k and _v and _k not in os.environ:
                        os.environ[_k] = _v
    except Exception:
        pass

st.set_page_config(
    page_title="KrishiRakshak - Crop DSS & Stage Diagnosis",
    page_icon="🌱",
    layout="wide"
)

# --- SESSION STATE INITIALIZATION FOR FARMER REGISTRY & CHAT ---
if "farmers_registry" not in st.session_state:
    st.session_state.farmers_registry = [
        {"Name": "HULK", "Phone": "+919352627188", "Village": "Akola", "Crop": "Cotton"},
        {"Name": "BABU", "Phone": "+919422899011", "Village": "Murtizapur", "Crop": "Paddy"},
        {"Name": "MANAS LUTE", "Phone": "+917020455678", "Village": "Barshitakli", "Crop": "Cotton"}
    ]

if "current_diagnosis" not in st.session_state:
    st.session_state.current_diagnosis = None

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "ai_disclaimer_accepted" not in st.session_state:
    st.session_state.ai_disclaimer_accepted = False

# --- DYNAMIC ALL-INDIA GEOCODER ---
@st.cache_data(ttl=86400)
def geocode_indian_place(place_name: str):
    clean_name = place_name.strip()
    if not clean_name:
        return 20.7002, 77.0082, "Akola, Maharashtra (Default)"
        
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": clean_name,
        "count": 5,
        "language": "en",
        "format": "json",
        "countryCode": "IN"
    }
    
    try:
        response = requests.get(url, params=params, timeout=4).json()
        results = response.get("results", [])
        if results:
            best = results[0]
            lat = float(best["latitude"])
            lon = float(best["longitude"])
            district = best.get("admin2", best.get("name", ""))
            state = best.get("admin1", "India")
            return lat, lon, f"{best['name']}, {district}, {state}"
    except Exception:
        pass
        
    return 20.7002, 77.0082, f"{clean_name} (Not found, defaulted to Akola)"

# --- COMPREHENSIVE MULTILINGUAL LOCALIZATION DICTIONARY ---
I18N = {
    "English": {
        "title": "🌱 KrishiRakshak: Smart Biocontrol & Pathogen Surveillance",
        "subtitle": "Institutional Decision Support System — Department of Agriculture",
        "sidebar_header": "📍 Field Microclimate & Location",
        "tab1_title": "🔬 Image Diagnosis & Plant Pathology",
        "tab_chat_title": "💬 Krishi AI Chatbot / Sahayak",
        "tab2_title": "👥 Registered Farmers Registry",
        "upload_label": "Upload Leaf Sample Image (Any Stage)",
        "pathogen": "Identified Pathogen / Pest",
        "trophic": "Trophic Lifestyle",
        "entry": "Infection Route",
        "susceptible": "Peak Vulnerable Stage",
        "r_genes": "Host Defense Traits (R-Genes)",
        "biocontrol": "Integrated Pest Management (IPM) & Biocontrol",
        "varieties": "Recommended Resistant Cultivars",
        "send_sms_btn": "🚨 Broadcast SMS Alert to Registered Farmers",
        "sms_success": "SMS broadcast successfully dispatched to all registered farmers!",
        "healthy_note": "Specimen is diagnosed as Healthy. SMS alert dispatch is not required.",
        "ood_warn": "⚠️ Inconclusive Diagnosis",
        "ood_info": "The sample does not match primary crop foliar classes or reflects abiotic stress.",
        "detection_scale": "🔬 Biological Detection Scale & Lesion Range",
        "inf_stage": "📊 Identified Infection Stage",
        "threshold": "⚠️ Warning Threshold / Economic Injury Level (ETL)",
        "chem_sol": "🧪 Certified Chemical Pesticides & Dosages",
        "bio_sol": "🌿 Certified Biological & Organic Alternatives",
        "resources": "📞 Farmer Lifelines & Critical Inputs Desk",
        "leaf_stage_title": "🍃 Diagnosed Leaf Damage Stage",
        "pest_stage_title": "🐛 Biological Pest / Pathogen Lifecycle Stage",
        "visual_heatmap": "🔬 Lesion Segmentation & Heatmap Inspection",
        "preventive_header": "🛡️ Proactive & Preventive Agronomic Measures",
        "chat_placeholder": "Ask about pesticide dosage, organic remedies, weather advice...",
        "anomaly_meter_title": "🛡️ Specimen Validity & Foliar Anomaly Meter",
        "anomaly_risk": "Anomaly / OOD Risk Index",
        "foliar_integrity": "Foliar Tissue Integrity",
        "report_header": "📄 Official Institutional Field Advisory Report",
        "report_btn": "📄 Generate Printable Advisory Report (Print / PDF)",
        "report_download_btn": "📥 Download Official Field Report (HTML / Print)",
        "disclaimer_header": "⚠️ Mandatory Institutional AI Advisory Disclaimer",
        "disclaimer_text": "Krishi Sahayak is an institutional AI decision support assistant. AI-generated insights are decision aids and do not substitute on-site inspection by a certified agricultural officer. Chemical pesticides carry environmental, dietary, and occupational hazards. Always consult your local Krishi Vigyan Kendra (KVK) or State Agricultural University / Block Agriculture Officer before chemical application. Strictly adhere to CIBRC-approved formulations, personal protective equipment (PPE), and mandatory Pre-Harvest Intervals (PHI).",
        "disclaimer_checkbox": "I understand and agree that this AI advice is a decision support aid and requires field verification.",
        "disclaimer_accept_btn": "Accept Terms & Access Krishi Sahayak",
        "pmfby_label": "PM Fasal Bima Yojana (PMFBY)",
        "ncipm_label": "ICAR-NCIPM Technical Verification"
    },
    "मराठी": {
        "title": "🌱 कृषीरक्षक: जैविक नियंत्रण आणि कीड-रोग नियंत्रण प्रणाली",
        "subtitle": "कृषी विभाग व आयसीएआर आधारित निर्णय समर्थन प्रणाली",
        "sidebar_header": "📍 शेत सूक्ष्म हवामान व स्थान",
        "tab1_title": "🔬 रोग निदान आणि वनस्पती पॅथॉलॉजी",
        "tab_chat_title": "💬 कृषीरक्षक AI संवाद / मदतनीस",
        "tab2_title": "👥 नोंदणीकृत शेतकरी यादी",
        "upload_label": "कोणत्याही अवस्थेतील पानाचा फोटो अपलोड करा",
        "pathogen": "रोगकारक घटक (Pathogen / Pest)",
        "trophic": "पोषण प्रकार (Trophic Mode)",
        "entry": "संक्रमण मार्ग (Entry Route)",
        "susceptible": "संवेदनशील पीक अवस्था",
        "r_genes": "प्रतिरोधक जनुकीय वैशिष्ट्ये (R-Genes)",
        "biocontrol": "सेंद्रिय व एकात्मिक कीड व्यवस्थापन (IPM)",
        "varieties": "शिफारस केलेले प्रतिकारक वाण",
        "send_sms_btn": "🚨 नोंदणीकृत शेतकऱ्यांना SMS अलर्ट पाठवा",
        "sms_success": "सर्व नोंदणीकृत शेतकऱ्यांना SMS यशस्वीरित्या पाठवला गेला आहे!",
        "healthy_note": "पीक निरोगी आहे. SMS अलर्ट पाठवण्याची आवश्यकता नाही.",
        "ood_warn": "⚠️ अनिर्णित किंवा दुय्यम लक्षणे",
        "ood_info": "अपलोड केलेले पान मुख्य वर्गांशी जुळत नाही किंवा अन्नद्रव्यांची कमतरता असू शकते.",
        "detection_scale": "🔬 जैविक आकारमान व रोगाच्या डागांची व्याप्ती",
        "inf_stage": "📊 संसर्गाची नेमकी अवस्था",
        "threshold": "⚠️ धोक्याची पातळी (आर्थिक नुकसान पातळी - ETL)",
        "chem_sol": "🧪 शिफारस केलेली रासायनिक कीटकनाशके व प्रमाण",
        "bio_sol": "🌿 सेंद्रिय व जैविक पर्यायी उपाय",
        "resources": "📞 शेतकरी मदत केंद्र व तातडीची संपर्क यंत्रणा",
        "leaf_stage_title": "🍃 पानावरील नुकसानीचा नेमका टप्पा",
        "pest_stage_title": "🐛 कीड किंवा रोगाची जैविक अवस्था",
        "visual_heatmap": "🔬 रोगग्रस्त डागांचे सूक्ष्म विश्लेषण (Heatmap)",
        "preventive_header": "🛡️ प्रतिबंधात्मक व सेंद्रिय उपाययोजना",
        "chat_placeholder": "औषध प्रमाण, सेंद्रिय अर्क, हवामानाबद्दल प्रश्न विचारा...",
        "anomaly_meter_title": "🛡️ नमुना वैधता आणि विकृती (Anomaly) मापक",
        "anomaly_risk": "विकृती / OOD जोखीम निर्देशांक",
        "foliar_integrity": "पानाच्या ऊतींची अखंडता",
        "report_header": "📄 अधिकृत संस्थात्मक शेती सल्लागार अहवाल",
        "report_btn": "📄 मुद्रणयोग्य सल्लागार अहवाल तयार करा (Print / PDF)",
        "report_download_btn": "📥 अधिकृत शेती अहवाल डाउनलोड करा (HTML / Print)",
        "disclaimer_header": "⚠️ अनिवार्य संस्थात्मक AI सल्लागार अस्वीकरण (Disclaimer)",
        "disclaimer_text": "कृषी सहाय्यक ही एक संस्थात्मक कृत्रिम बुद्धिमत्ता (AI) आधारित निर्णय समर्थन प्रणाली आहे. रासायनिक कीटकनाशकांचा वापर करण्यापूर्वी आपल्या स्थानिक कृषी विज्ञान केंद्र (KVK) किंवा तालुका कृषी अधिकाऱ्यांचा सल्ला घ्या. CIBRC मान्यताप्राप्त योग्य औषध प्रमाण, वैयक्तिक सुरक्षा साधने (PPE) आणि फवारणीनंतर काढणीची प्रतीक्षा मुदत (PHI) यांचे काटेकोर पालन करा.",
        "disclaimer_checkbox": "मी नियम व अटी वाचल्या असून मान्य करतो की हा AI सल्ला शेतीतील प्रत्यक्ष पडताळणीवर आधारित असणे आवश्यक आहे.",
        "disclaimer_accept_btn": "अटी मान्य करून कृषी सहाय्यक सुरू करा",
        "pmfby_label": "पंतप्रधान पीक विमा योजना (PMFBY)",
        "ncipm_label": "आयसीएआर-एनसीआयपीएम (ICAR-NCIPM) तांत्रिक संदर्भ"
    },
    "हिंदी": {
        "title": "🌱 कृषिरक्षक: जैविक नियंत्रण एवं रोग निगरानी प्रणाली",
        "subtitle": "कृषि विभाग आधारित संस्थागत निर्णय समर्थन प्रणाली",
        "sidebar_header": "📍 खेत का सूक्ष्म मौसम एवं स्थान",
        "tab1_title": "🔬 रोग निदान एवं पादप रोग विज्ञान",
        "tab_chat_title": "💬 कृषिरक्षक AI चैटबॉट / सहायक",
        "tab2_title": "👥 पंजीकृत किसान डेटाबेस",
        "upload_label": "किसी भी अवस्था की संक्रमित पत्ती या कीट का फोटो अपलोड करें",
        "pathogen": "पहचाना गया रोगकारक / कीट",
        "trophic": "पोषण प्रकार (Trophic Mode)",
        "entry": "संक्रमण मार्ग (Entry Route)",
        "susceptible": "अत्यधिक संवेदनशील अवस्था",
        "r_genes": "प्रतिरोधी लक्षण (R-Genes)",
        "biocontrol": "एकीकृत कीट प्रबंधन (IPM) एवं जैविक नियंत्रण",
        "varieties": "अनुशंसित प्रतिरोधी किस्में",
        "send_sms_btn": "🚨 पंजीकृत किसानों को SMS अलर्ट भेजें",
        "sms_success": "सभी पंजीकृत किसानों को SMS अलर्ट सफलतापूर्वक भेज दिया गया है!",
        "healthy_note": "फसल पूरी तरह स्वस्थ है। SMS चेतावनी भेजने की आवश्यकता नहीं है।",
        "ood_warn": "⚠️ अनिर्णायक निदान",
        "ood_info": "अपलोड किया गया नमूना मुख्य वर्गों से मेल नहीं खाता या पोषक तत्वों की कमी हो सकती है।",
        "detection_scale": "🔬 जैविक पहचान आकार एवं घाव का फैलाव",
        "inf_stage": "📊 संक्रमण की वर्तमान अवस्था",
        "threshold": "⚠️ चेतावनी स्तर / आर्थिक क्षति सीमा (ETL)",
        "chem_sol": "🧪 अनुशंसित रासायनिक कीटनाशक एवं सही मात्रा",
        "bio_sol": "🌿 प्रमाणित जैविक एवं प्राकृतिक विकल्प",
        "resources": "📞 किसान हेल्पलाइन एवं आपातकालीन सहायता केंद्र",
        "leaf_stage_title": "🍃 पत्ती पर क्षति का चरण",
        "pest_stage_title": "🐛 कीट / रोग का जैविक जीवन चरण",
        "visual_heatmap": "🔬 घाव एवं क्षति का हीटमैप विश्लेषण",
        "preventive_header": "🛡️ सक्रिय एवं निवारक कृषि उपाय",
        "chat_placeholder": "दवा की मात्रा, जैविक कीटनाशक, मौसम की अनुकूलता के बारे में पूछें...",
        "anomaly_meter_title": "🛡️ नमूना वैधता एवं विसंगति (Anomaly) मापक",
        "anomaly_risk": "विसंगति / OOD जोखिम सूचकांक",
        "foliar_integrity": "पत्ती ऊतक अखंडता",
        "report_header": "📄 आधिकारिक संस्थागत कृषि परामर्श रिपोर्ट",
        "report_btn": "📄 प्रिंट करने योग्य परामर्श रिपोर्ट तैयार करें (Print / PDF)",
        "report_download_btn": "📥 आधिकारिक फील्ड रिपोर्ट डाउनलोड करें (HTML / Print)",
        "disclaimer_header": "⚠️ अनिवार्य संस्थागत AI परामर्श अस्वीकरण (Disclaimer)",
        "disclaimer_text": "कृषिरक्षक सहायक एक संस्थागत AI निर्णय समर्थन प्रणाली है। किसी भी रासायनिक कीटनाशक के छिड़काव से पहले अपने नजदीकी कृषि विज्ञान केंद्र (KVK) या खंड कृषि अधिकारी से अवश्य सलाह लें। CIBRC द्वारा स्वीकृत दवाओं की सही मात्रा, व्यक्तिगत सुरक्षा उपकरण (PPE) और फसल कटाई पूर्व प्रतीक्षा अवधि (PHI) का कड़ाई से पालन करें।",
        "disclaimer_checkbox": "मैंने सभी नियम व शर्तें पढ़ ली हैं और स्वीकार करता हूँ कि यह AI सलाह केवल निर्णय सहायता हेतु है।",
        "disclaimer_accept_btn": "शर्तें स्वीकार कर कृषिरक्षक सहायक शुरू करें",
        "pmfby_label": "प्रधानमंत्री फसल बीमा योजना (PMFBY)",
        "ncipm_label": "आईसीएआर-एनसीआईपीएम (ICAR-NCIPM) तकनीकी संदर्भ"
    },
    "తెలుగు": {
        "title": "🌱 కృషీరక్షక్: బయోకంట్రోల్ మరియు చీడపీడల పర్యవేక్షణ వ్యవస్థ",
        "subtitle": "వ్యవసాయ శాఖ నిర్ణయ మద్దతు వ్యవస్థ",
        "sidebar_header": "📍 పొలం వాతావరణం మరియు స్థానం",
        "tab1_title": "🔬 వ్యాధి నిర్ధారణ & పాథాలజీ",
        "tab_chat_title": "💬 కృషీరక్షక్ AI చాట్‌బాట్",
        "tab2_title": "👥 నమోదిత రైతుల జాబితా",
        "upload_label": "ఏదైనా దశలోని తెగులు సోకిన ఆకు ఫోటోను అప్‌లోడ్ చేయండి",
        "pathogen": "గుర్తించిన వ్యాధికారకం / కీటకం",
        "trophic": "పోషణ రకం",
        "entry": "వ్యాప్తి మార్గం",
        "susceptible": "ప్రభావిత పంట దశ",
        "r_genes": "నిరోధక లక్షణాలు (R-Genes)",
        "biocontrol": "సమగ్ర సస్యరక్షణ (IPM)",
        "varieties": "సిఫార్సు చేయబడిన రకాలు",
        "send_sms_btn": "🚨 రైతులకు SMS హెచ్చరిక పంపండి",
        "sms_success": "రైతులకు SMS హెచ్చరిక విజయవంతంగా పంపబడింది!",
        "healthy_note": "పంట ఆరోగ్యంగా ఉంది. SMS అవసరం లేదు.",
        "ood_warn": "⚠️ అనిశ్చిత నిర్ధారణ",
        "ood_info": "నమూనా స్పష్టంగా లేదు లేదా పోషకాహార లోపం కావచ్చు.",
        "detection_scale": "🔬 జీవసంబంధ పరిమాణం & తెగులు విస్తీర్ణం",
        "inf_stage": "📊 గుర్తించిన వ్యాధి దశ",
        "threshold": "⚠️ హెచ్చరిక స్థాయి / నష్ట పరిమితి (ETL)",
        "chem_sol": "🧪 సిఫార్సు చేసిన రసాయనాలు & మోతాదు",
        "bio_sol": "🌿 సేంద్రీయ & జీవ ప్రత్యామ్నాయాలు",
        "resources": "📞 రైతు సహాయ కేంద్రం & వనరులు",
        "leaf_stage_title": "🍃 ఆకు నష్టం దశ",
        "pest_stage_title": "🐛 పురుగు జీవన చక్ర దశ",
        "visual_heatmap": "🔬 వ్యాధి లక్షణాల హీట్‌మ్యాప్",
        "preventive_header": "🛡️ సమగ్ర నివారణ చర్యలు",
        "chat_placeholder": "మందుల మోతాదు, సేంద్రీయ పద్ధతుల గురించి అడగండి...",
        "anomaly_meter_title": "🛡️ నమూనా ప్రామాణికత & అనోమలీ డిటెక్షన్ మీటర్",
        "anomaly_risk": "అనోమలీ / OOD రిస్క్ ఇండెక్స్",
        "foliar_integrity": "ఆకు కణజాల సమగ్రత",
        "report_header": "📄 అధికారిక వ్యవసాయ క్షేత్ర సలహా నివేదిక",
        "report_btn": "📄 ముద్రించదగిన సలహా నివేదికను రూపొందించండి (Print / PDF)",
        "report_download_btn": "📥 అధికారిక నివేదికను డౌన్‌లోడ్ చేయండి (HTML / Print)",
        "disclaimer_header": "⚠️ తప్పనిసరి సంస్థాగత AI నిరాకరణ (Disclaimer)",
        "disclaimer_text": "కృషీ సహాయక్ అనేది సంస్థాగత AI నిర్ణయ మద్దతు వ్యవస్థ. రసాయన క్రిమిసంహారకాలు వాడే ముందు స్థానిక కృషి విజ్ఞాన కేంద్రం (KVK) లేదా వ్యవసాయ శాఖాధికారిని సంప్రదించండి. CIBRC ఆమోదించిన మోతాదులు, రక్షణ పరికరాలు (PPE) మరియు పంట కోతకు ముందు వ్యవధి (PHI) నిబంధనలను ఖచ్చితంగా పాటించండి.",
        "disclaimer_checkbox": "నేను నిబంధనలను చదివాను మరియు ఈ AI సలహా క్షేత్రస్థాయి ధృవీకరణపై ఆధారపడి ఉంటుందని అంగీకరిస్తున్నాను.",
        "disclaimer_accept_btn": "నిబంధనలను అంగీకరించి కృషీ సహాయక్ ప్రారంభించండి",
        "pmfby_label": "ప్రధాన మంత్రి ఫసల్ బీమా యోజన (PMFBY)",
        "ncipm_label": "ICAR-NCIPM సాంకేతిక ధృవీకరణ"
    },
    "தமிழ்": {
        "title": "🌱 கிருஷிரக்ஷக்: நுண்ணுயிர் கட்டுப்பாடு மற்றும் பயிர் பாதுகாப்பு",
        "subtitle": "வேளாண்மை துறை நிறுவன ஆதரவு அமைப்பு",
        "sidebar_header": "📍 கள வானிலை மற்றும் இருப்பிடம்",
        "tab1_title": "🔬 பயிர் நோய் கண்டறிதல்",
        "tab_chat_title": "💬 கிருஷிரக்ஷக் AI உரையாடல்",
        "tab2_title": "👥 பதிவுசெய்த விவசாயிகள் பட்டியல்",
        "upload_label": "எந்த நிலையிலும் பாதிக்கப்பட்ட இலையின் படத்தை பதிவேற்றவும்",
        "pathogen": "கண்டறியப்பட்ட நோய்க்கிருமி",
        "trophic": "ஊட்டச்சத்து முறை",
        "entry": "தாக்கும் வழிமுறை",
        "susceptible": "பாதிக்கப்படக்கூடிய பருவம்",
        "r_genes": "எதிர்ப்பு மரபணுக்கள் (R-Genes)",
        "biocontrol": "ஒருங்கிணைந்த பூச்சி மேலாண்மை (IPM)",
        "varieties": "பரிந்துரைக்கப்பட்ட ரகங்கள்",
        "send_sms_btn": "🚨 விவசாயிகளுக்கு SMS எச்சரிக்கை அனுப்பு",
        "sms_success": "விவசாயிகளுக்கு SMS எச்சரிக்கை அனுப்பப்பட்டது!",
        "healthy_note": "பயிர் ஆரோக்கியமாக உள்ளது. SMS தேவையில்லை.",
        "ood_warn": "⚠️ தெளிவற்ற கண்டறிதல்",
        "ood_info": "மாதிரி முதன்மை வகைகளுடன் பொருந்தவில்லை.",
        "detection_scale": "🔬 நோய்க்கிருமி அளவு & பாதிப்பு பரப்பளவு",
        "inf_stage": "📊 கண்டறியப்பட்ட நோய்த்தொற்று நிலை",
        "threshold": "⚠️ எச்சரிக்கை வரம்பு (ETL)",
        "chem_sol": "🧪 பரிந்துரைக்கப்பட்ட பூச்சிக்கொல்லிகள் & அளவு",
        "bio_sol": "🌿 இயற்கை மற்றும் உயிரியல் மாற்றுகள்",
        "resources": "📞 உழவர் உதவி எண்கள் மற்றும் அவசர தொடர்பு",
        "leaf_stage_title": "🍃 இலையின் பாதிப்பு நிலை",
        "pest_stage_title": "🐛 பூச்சியின் வளர்ச்சி நிலை",
        "visual_heatmap": "🔬 பாதிப்பு வரைபட ஆய்வு (Heatmap)",
        "preventive_header": "🛡️ தடுப்பு மற்றும் பாதுகாப்பு வழிமுறைகள்",
        "chat_placeholder": "மருந்து அளவு, இயற்கை முறைகள் பற்றி கேளுங்கள்...",
        "anomaly_meter_title": "🛡️ மாதிரி செல்லுபடியாகும் தன்மை மற்றும் முரண்பாடு அளவீடு",
        "anomaly_risk": "முரண்பாடு / OOD இடர் குறியீடு",
        "foliar_integrity": "இலை திசு ஒருமைப்பாடு",
        "report_header": "📄 அதிகாரப்பூர்வ நிறுவன கள ஆலோசனை அறிக்கை",
        "report_btn": "📄 அச்சிடக்கூடிய ஆலோசனை அறிக்கையை உருவாக்கு (Print / PDF)",
        "report_download_btn": "📥 அதிகாரப்பூர்வ அறிக்கையைப் பதிவிறக்கு (HTML / Print)",
        "disclaimer_header": "⚠️ கட்டாய நிறுவன AI ஆலோசனை மறுப்பு (Disclaimer)",
        "disclaimer_text": "கிருஷி சகாயக் என்பது ஒரு நிறுவன AI முடிவெடுக்கும் உதவி அமைப்பாகும். பூச்சிக்கொல்லிகளைப் பயன்படுத்துவதற்கு முன் உங்கள் உள்ளூர் வேளாண் அறிவியல் மையம் (KVK) அல்லது வட்டார வேளாண்மை அலுவலரை அணுகவும். CIBRC அங்கீகரிக்கப்பட்ட மருந்தளவு, பாதுகாப்பு உபகரணங்கள் (PPE) மற்றும் அறுவடைக்கு முந்தைய காத்திருப்பு காலம் (PHI) ஆகியவற்றை கண்டிப்பாகப் பின்பற்றவும்.",
        "disclaimer_checkbox": "விதிமுறைகளைப் படித்து ஒப்புக்கொள்கிறேன்; இந்த AI ஆலோசனை நேரடி சரிபார்ப்பிற்கு உட்பட்டது என்பதை ஏற்கிறேன்.",
        "disclaimer_accept_btn": "விதிமுறைகளை ஏற்று கிருஷி சகாயக் தொடங்கவும்",
        "pmfby_label": "பிரதமர் பயிர் காப்பீட்டுத் திட்டம் (PMFBY)",
        "ncipm_label": "ICAR-NCIPM தொழில்நுட்ப சரிபார்ப்பு"
    },
    "ಕನ್ನಡ": {
        "title": "🌱 ಕೃಷಿರಕ್ಷಕ್: ಸ್ಮಾರ್ಟ್ ಜೈವಿಕ ನಿಯಂತ್ರಣ ಮತ್ತು ರೋಗ ಕಣ್ಗಾವಲು ವ್ಯವಸ್ಥೆ",
        "subtitle": "ಕೃಷಿ ಇಲಾಖೆ ನಿರ್ಧಾರ ಬೆಂಬಲ ವ್ಯವಸ್ಥೆ",
        "sidebar_header": "📍 ಕ್ಷೇತ್ರದ ಹವಾಮಾನ ಮತ್ತು ಸ್ಥಳ",
        "tab1_title": "🔬 ರೋಗ ಪತ್ತೆ ಮತ್ತು ಸಸ್ಯ ರೋಗಶಾಸ್ತ್ರ",
        "tab_chat_title": "💬 ಕೃಷಿರಕ್ಷಕ್ AI ಚಾಟ್‌ಬಾಟ್",
        "tab2_title": "👥 ನೋಂದಾಯಿತ ರೈತರ ಪಟ್ಟಿ",
        "upload_label": "ಯಾವುದೇ ಹಂತದ ರೋಗಪೀಡಿತ ಎಲೆಯ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "pathogen": "ರೋಗಕಾರಕ / ಕೀಟ",
        "trophic": "ಪೋಷಣೆಯ ವಿಧಾನ",
        "entry": "ಸೋಂಕಿನ ಮಾರ್ಗ",
        "susceptible": "ಬೆಳೆಯ ಸೂಕ್ಷ್ಮ ಹಂತ",
        "r_genes": "ಪ್ರತಿರೋಧಕ ಗುಣಲಕ್ಷಣಗಳು (R-Genes)",
        "biocontrol": "ಸಮಗ್ರ ಕೀಟ ನಿರ್ವಹಣೆ (IPM)",
        "varieties": "ಶಿಫಾರಸು ಮಾಡಿದ ತಳಿಗಳು",
        "send_sms_btn": "🚨 ರೈತರಿಗೆ SMS ಎಚ್ಚರಿಕೆ ಕಳುಹಿಸಿ",
        "sms_success": "ಎಲ್ಲಾ ರೈತರಿಗೆ SMS ಎಚ್ಚರಿಕೆ ಕಳುಹಿಸಲಾಗಿದೆ!",
        "healthy_note": "ಬೆಳೆ ಆರೋಗ್ಯಕರವಾಗಿದೆ. SMS ಅಗತ್ಯವಿಲ್ಲ.",
        "ood_warn": "⚠️ ಅನಿರ್ದಿಷ್ಟ ರೋಗನಿರ್ಣಯ",
        "ood_info": "ಮಾದರಿಯು ಮುಖ್ಯ ವರ್ಗಗಳಿಗೆ ಹೊಂದಿಕೆಯಾಗುತ್ತಿಲ್ಲ.",
        "detection_scale": "🔬 ರೋಗಕಾರಕ ಗಾತ್ರ ಮತ್ತು ಗಾಯದ ವ್ಯಾಪ್ತಿ",
        "inf_stage": "📊 ಸೋಂಕಿನ ಪ್ರಸ್ತುತ ಹಂತ",
        "threshold": "⚠️ ಎಚ್ಚರಿಕೆ ಮಟ್ಟ (ETL)",
        "chem_sol": "🧪 ಶಿಫಾರಸು ಮಾಡಲಾದ ರಾಸಾಯನಿಕಗಳು ಮತ್ತು ಪ್ರಮಾಣ",
        "bio_sol": "🌿 ಸಾವಯವ ಮತ್ತು ಜೈವಿಕ ಪರ್ಯಾಯಗಳು",
        "resources": "📞 ರೈತ ಸಹಾಯವಾಣಿ ಮತ್ತು ಸಂಪನ್ಮೂಲಗಳು",
        "leaf_stage_title": "🍃 ಎಲೆಯ ಹಾನಿಯ ಹಂತ",
        "pest_stage_title": "🐛 ಕೀಟದ ಜೈವಿಕ ಹಂತ",
        "visual_heatmap": "🔬 ರೋಗದ ಕಲೆಗಳ ಹೀಟ್‌ಮ್ಯಾಪ್ ವಿಶ್ಲೇಷಣೆ",
        "preventive_header": "🛡️ ಮುನ್ನೆಚ್ಚರಿಕೆ ಮತ್ತು ಜೈವಿಕ ಕ್ರಮಗಳು",
        "chat_placeholder": "ಕೀಟನಾಶಕ ಪ್ರಮಾಣ, ಸಾವಯವ ಪರಿಹಾರಗಳ ಬಗ್ಗೆ ಕೇಳಿ...",
        "anomaly_meter_title": "🛡️ ಮಾದರಿ ಸಿಂಧುತ್ವ ಮತ್ತು ಅಸಹಜತೆ ಪತ್ತೆ ಮೀಟರ್",
        "anomaly_risk": "ಅಸಹಜತೆ / OOD ಅಪಾಯ ಸೂಚ್ಯಂಕ",
        "foliar_integrity": "ಎಲೆಯ ಅಂಗಾಂಶ ಸಮಗ್ರತೆ",
        "report_header": "📄 ಅಧಿಕೃತ ಸಾಂಸ್ಥಿಕ ಕೃಷಿ ಸಲಹಾ ವರದಿ",
        "report_btn": "📄 ಮುದ್ರಿಸಬಹುದಾದ ಸಲಹಾ ವರದಿಯನ್ನು ರಚಿಸಿ (Print / PDF)",
        "report_download_btn": "📥 ಅಧಿಕೃತ ವರದಿಯನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ (HTML / Print)",
        "disclaimer_header": "⚠️ ಕಡ್ಡಾಯ ಸಾಂಸ್ಥಿಕ AI ಸಲಹಾ ಹಕ್ಕುತ್ಯಾಗ (Disclaimer)",
        "disclaimer_text": "ಕೃಷಿ ಸಹಾಯಕವು ಸಾಂಸ್ಥಿಕ AI ನಿರ್ಧಾರ ಬೆಂಬಲ ವ್ಯವಸ್ಥೆಯಾಗಿದೆ. ಕೀಟನಾಶಕಗಳನ್ನು ಬಳಸುವ ಮೊದಲು ಸ್ಥಳೀಯ ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರ (KVK) ಅಥವಾ ಕೃಷಿ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ. CIBRC ಅನುಮೋದಿತ ಪ್ರಮಾಣ, ವೈಯಕ್ತಿಕ ರಕ್ಷಣಾ ಸಾಧನಗಳು (PPE) ಮತ್ತು ಕೊಯ್ಲಿನ ಮುಂಚಿನ ಕಾಯುವ ಅವಧಿ (PHI) ನಿಯಮಗಳನ್ನು ಕಟ್ಟುನಿಟ್ಟಾಗಿ ಪಾಲಿಸಿ.",
        "disclaimer_checkbox": "ನಾನು ನಿಯಮಗಳನ್ನು ಓದಿದ್ದೇನೆ ಮತ್ತು ಈ AI ಸಲಹೆಯು ಕ್ಷೇತ್ರ ಪರಿಶೀಲನೆಗೆ ಒಳಪಟ್ಟಿರುತ್ತದೆ ಎಂದು ಒಪ್ಪಿಕೊಳ್ಳುತ್ತೇನೆ.",
        "disclaimer_accept_btn": "ಷರತ್ತುಗಳನ್ನು ಒಪ್ಪಿ ಕೃಷಿ ಸಹಾಯಕ ಪ್ರಾರಂಭಿಸಿ",
        "pmfby_label": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಫಸಲ್ ಬಿಮಾ ಯೋಜನೆ (PMFBY)",
        "ncipm_label": "ICAR-NCIPM ತಾಂತ್ರಿಕ ಪರಿಶೀಲನೆ"
    },
    "ਪੰਜਾਬੀ": {
        "title": "🌱 ਕ੍ਰਿਸ਼ੀਰਕਸ਼ਕ: ਸਮਾਰਟ ਬਾਇਓਕੰਟਰੋਲ ਅਤੇ ਕੀਟ-ਰੋਗ ਨਿਗਰਾਨੀ ਪ੍ਰਣਾਲੀ",
        "subtitle": "ਖੇਤੀਬਾੜੀ ਵਿਭਾਗ ਫੈਸਲਾ ਸਹਾਇਤਾ ਪ੍ਰਣਾਲੀ",
        "sidebar_header": "📍 ਖੇਤ ਦਾ ਮੌਸਮ ਅਤੇ ਸਥਾਨ",
        "tab1_title": "🔬 ਰੋਗ ਨਿਦਾਨ ਅਤੇ ਪੌਦਾ ਰੋਗ ਵਿਗਿਆਨ",
        "tab_chat_title": "💬 ਕ੍ਰਿਸ਼ੀਰਕਸ਼ਕ AI ਚੈਟਬੋਟ",
        "tab2_title": "👥 ਰਜਿਸਟਰਡ ਕਿਸਾਨਾਂ ਦੀ ਸੂਚੀ",
        "upload_label": "ਕਿਸੇ ਵੀ ਪੜਾਅ ਦੇ ਬਿਮਾਰ ਪੱਤੇ ਦੀ ਫੋਟੋ ਅੱਪਲੋਡ ਕਰੋ",
        "pathogen": "ਪਛਾਣਿਆ ਗਿਆ ਰੋਗਾਣੂ / ਕੀੜਾ",
        "trophic": "ਪੋਸ਼ਣ ਢੰਗ",
        "entry": "ਹਮਲੇ ਦਾ ਰਸਤਾ",
        "susceptible": "ਸੰਵੇਦਨਸ਼ੀਲ ਫਸਲ ਅਵਸਥਾ",
        "r_genes": "ਰੋਧਕ ਜੀਨ (R-Genes)",
        "biocontrol": "ਏਕੀਕ੍ਰਿਤ ਕੀਟ ਪ੍ਰਬੰਧਨ (IPM)",
        "varieties": "ਸਿਫਾਰਸ਼ ਕੀਤੀਆਂ ਕਿਸਮਾਂ",
        "send_sms_btn": "🚨 ਕਿਸਾਨਾਂ ਨੂੰ SMS ਚੇਤਾਵਨੀ ਭੇਜੋ",
        "sms_success": "ਸਾਰੇ ਕਿਸਾਨਾਂ ਨੂੰ SMS ਸਫਲਤਾਪੂਰਵਕ ਭੇਜਿਆ ਗਿਆ!",
        "healthy_note": "ਫਸਲ ਬਿਲਕੁਲ ਤੰਦਰੁਸਤ ਹੈ। SMS ਦੀ ਲੋੜ ਨਹੀਂ ਹੈ।",
        "ood_warn": "⚠️ ਅਸਪਸ਼ਟ ਨਿਦਾਨ",
        "ood_info": "ਅੱਪਲੋਡ ਕੀਤਾ ਨਮੂਨਾ ਮੁੱਖ ਸ਼੍ਰੇਣੀਆਂ ਨਾਲ ਮੇਲ ਨਹੀਂ ਖਾਂਦਾ।",
        "detection_scale": "🔬 ਰੋਗਾਣੂ ਦਾ ਆਕਾਰ ਅਤੇ ਨੁਕਸਾਨ ਦਾ ਘੇਰਾ",
        "inf_stage": "📊 ਸੰਕ੍ਰਮਣ ਦਾ ਪੜਾਅ",
        "threshold": "⚠️ ਚੇਤਾਵਨੀ ਪੱਧਰ (ETL)",
        "chem_sol": "🧪 ਸਿਫਾਰਸ਼ ਕੀਤੀਆਂ ਰਸਾਇਣਕ ਦਵਾਈਆਂ ਅਤੇ ਮਾਤਰਾ",
        "bio_sol": "🌿 ਜੈਵਿਕ ਅਤੇ ਕੁਦਰਤੀ ਵਿਕਲਪ",
        "resources": "📞 ਕਿਸਾਨ ਹੈਲਪਲਾਈਨ ਅਤੇ ਐਮਰਜੈਂਸੀ ਸਹਾਇਤਾ",
        "leaf_stage_title": "🍃 ਪੱਤੇ ਦੇ ਨੁਕਸਾਨ ਦਾ ਪੜਾਅ",
        "pest_stage_title": "🐛 ਕੀੜੇ ਦਾ ਜੀਵਨ ਚੱਕਰ ਪੜਾਅ",
        "visual_heatmap": "🔬 ਨੁਕਸਾਨ ਦਾ ਹੀਟਮੈਪ ਵਿਸ਼ਲੇਸ਼ਣ",
        "preventive_header": "🛡️ ਬਚਾਅ ਅਤੇ ਕੁਦਰਤੀ ਰੋਕਥਾਮ ਉਪਾਅ",
        "chat_placeholder": "ਦਵਾਈ ਦੀ ਮਾਤਰਾ, ਜੈਵਿਕ ਉਪਚਾਰਾਂ ਬਾਰੇ ਪੁੱਛੋ...",
        "anomaly_meter_title": "🛡️ ਨਮੂਨਾ ਪ੍ਰਮਾਣਿਕਤਾ ਅਤੇ ਅਸਧਾਰਨਤਾ (ਐਨੋਮਲੀ) ਮੀਟਰ",
        "anomaly_risk": "ਅਸਧਾਰਨਤਾ / OOD ਜੋਖਮ ਸੂਚਕ",
        "foliar_integrity": "ਪੱਤੇ ਦੇ ਟਿਸ਼ੂ ਦੀ ਇਕਸਾਰਤਾ",
        "report_header": "📄 ਅਧਿਕਾਰਤ ਸੰਸਥਾਗਤ ਖੇਤੀ ਸਲਾਹਕਾਰ ਰਿਪੋਰਟ",
        "report_btn": "📄 ਪ੍ਰਿੰਟਯੋਗ ਸਲਾਹਕਾਰ ਰਿਪੋਰਟ ਤਿਆਰ ਕਰੋ (Print / PDF)",
        "report_download_btn": "📥 ਅਧਿਕਾਰਤ ਖੇਤ ਰਿਪੋਰਟ ਡਾਊਨਲੋਡ ਕਰੋ (HTML / Print)",
        "disclaimer_header": "⚠️ ਲਾਜ਼ਮੀ ਸੰਸਥਾਗਤ AI ਸਲਾਹਕਾਰ ਬੇਦਾਅਵਾ (Disclaimer)",
        "disclaimer_text": "ਕ੍ਰਿਸ਼ੀ ਸਹਾਇਕ ਇੱਕ ਸੰਸਥਾਗਤ AI ਫੈਸਲਾ ਸਹਾਇਤਾ ਪ੍ਰਣਾਲੀ ਹੈ। ਕੀਟਨਾਸ਼ਕਾਂ ਦੀ ਵਰਤੋਂ ਕਰਨ ਤੋਂ ਪਹਿਲਾਂ ਆਪਣੇ ਨਜ਼ਦੀਕੀ ਕ੍ਰਿਸ਼ੀ ਵਿਗਿਆਨ ਕੇਂਦਰ (KVK) ਜਾਂ ਖੇਤੀਬਾੜੀ ਅਧਿਕਾਰੀ ਨਾਲ ਸੰਪਰਕ ਕਰੋ। CIBRC ਦੁਆਰਾ ਪ੍ਰਮਾਣਿਤ ਖੁਰਾਕ, ਸੁਰੱਖਿਆ ਉਪਕਰਣ (PPE) ਅਤੇ ਵਾਢੀ ਤੋਂ ਪਹਿਲਾਂ ਦੀ ਮਿਆਦ (PHI) ਦੀ ਸਖਤੀ ਨਾਲ ਪਾਲਣਾ ਕਰੋ।",
        "disclaimer_checkbox": "ਮੈਂ ਨਿਯਮ ਅਤੇ ਸ਼ਰਤਾਂ ਪੜ੍ਹ ਲਈਆਂ ਹਨ ਅਤੇ ਸਹਿਮਤ ਹਾਂ ਕਿ ਇਹ AI ਸਲਾਹ ਸਿਰਫ ਸਹਾਇਤਾ ਲਈ ਹੈ।",
        "disclaimer_accept_btn": "ਸ਼ਰਤਾਂ ਸਵੀਕਾਰ ਕਰੋ ਅਤੇ ਕ੍ਰਿਸ਼ੀ ਸਹਾਇਕ ਸ਼ੁਰੂ ਕਰੋ",
        "pmfby_label": "ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਫਸਲ ਬੀਮਾ ਯੋਜਨਾ (PMFBY)",
        "ncipm_label": "ICAR-NCIPM ਤਕਨੀਕੀ ਤਸਦੀਕ"
    },
    "ગુજરાતી": {
        "title": "🌱 કૃષિરક્ષક: સ્માર્ટ જૈવિક નિયંત્રણ અને રોગ સર્વેક્ષણ પ્રણાલી",
        "subtitle": "કૃષિ વિભાગ સંસ્થાકીય નિર્ણય સહાયક પ્રણાલી",
        "sidebar_header": "📍 ખેત આબોહવા અને સ્થળ",
        "tab1_title": "🔬 રોગ નિદાન અને વનસ્પતિ રોગવિજ્ઞાન",
        "tab_chat_title": "💬 કૃષિરક્ષક AI ચેટબોટ",
        "tab2_title": "👥 નોંધાયેલ ખેડૂત ડેટાબેઝ",
        "upload_label": "કોઈપણ તબક્કાના રોગિષ્ઠ પાનનો ફોટો અપલોડ કરો",
        "pathogen": "ઓળખાયેલ રોગકારક / જીવાત",
        "trophic": "પોષણ પ્રકાર",
        "entry": "ચેપ લાગવાનો માર્ગ",
        "susceptible": "સંવેદનશીલ પાકનો તબક્કો",
        "r_genes": "રોગપ્રતિકારક લક્ષણો (R-Genes)",
        "biocontrol": "સંકલિત જીવાત નિયંત્રણ (IPM)",
        "varieties": "ભલામણ કરેલ જાતો",
        "send_sms_btn": "🚨 ખેડૂતોને SMS ચેતવણી મોકલો",
        "sms_success": "બધા ખેડૂતોને SMS સફળતાપૂર્વક મોકલવામાં આવ્યો!",
        "healthy_note": "પાક તંદુરસ્ત છે. SMS ની જરૂર નથી.",
        "ood_warn": "⚠️ અનિર્ણિત નિદાન",
        "ood_info": "નમૂનો મુખ્ય વર્ગો સાથે મેળ ખાતો નથી.",
        "detection_scale": "🔬 જીવાણુનું કદ અને નુકસાનનો વ્યાપ",
        "inf_stage": "📊 ચેપનો વર્તમાન તબક્કો",
        "threshold": "⚠️ ચેતવણી સ્તર (ETL)",
        "chem_sol": "🧪 ભલામણ કરેલ રાસાયણિક દવાઓ અને પ્રમાણ",
        "bio_sol": "🌿 પ્રમાણિત જૈવિક અને કુદરતી વિકલ્પો",
        "resources": "📞 કિસાન હેલ્પલાઈન અને કટોકટી સહાય કેન્દ્ર",
        "leaf_stage_title": "🍃 પાન પર નુકસાનનો તબક્કો",
        "pest_stage_title": "🐛 જીવાતનો જૈવિક જીવન તબક્કો",
        "visual_heatmap": "🔬 રોગના ડાઘાનું હીટમેપ વિશ્લેષણ",
        "preventive_header": "🛡️ નિવારક અને જૈવિક પગલાં",
        "chat_placeholder": "દવાઓનું માપ, જૈવિક ઉપાયો વિશે પૂછો...",
        "anomaly_meter_title": "🛡️ નમૂનાની માન્યતા અને વિસંગતતા (Anomaly) મીટર",
        "anomaly_risk": "વિસંગતતા / OOD જોખમ ઇન્ડેક્સ",
        "foliar_integrity": "પાનના પેશીની અખંડિતતા",
        "report_header": "📄 સત્તાવાર સંસ્થાકીય કૃષિ સલાહકાર અહેવાલ",
        "report_btn": "📄 પ્રિન્ટ કરી શકાય તેવો સલાહ અહેવાલ બનાવો (Print / PDF)",
        "report_download_btn": "📥 સત્તાવાર ખેત અહેવાલ ડાઉનલોડ કરો (HTML / Print)",
        "disclaimer_header": "⚠️ ફરજિયાત સંસ્થાકીય AI સલાહ અસ્વીકરણ (Disclaimer)",
        "disclaimer_text": "કૃષિ સહાયક એ સંસ્થાકીય AI નિર્ણય સહાયક પ્રણાલી છે. જંતુનાશકોનો ઉપયોગ કરતા પહેલા તમારા સ્થાનિક કૃષિ વિજ્ઞાન કેન્દ્ર (KVK) અથવા કૃષિ અધિકારીની સલાહ લો. CIBRC માન્ય દવાઓનું પ્રમાણ, અંગત સુરક્ષા સાધનો (PPE) અને કાપણી પહેલાંનો સમયગાળો (PHI) નું કડક પાલન કરો.",
        "disclaimer_checkbox": "મેં શરતો વાંચી છે અને સ્વીકારું છું કે આ AI સલાહ ક્ષેત્રીય ચકાસણી પર આધારિત હોવી જરૂરી છે.",
        "disclaimer_accept_btn": "શરતો સ્વીકારી કૃષિ સહાયક શરૂ કરો",
        "pmfby_label": "પ્રધાનમંત્રી ફસલ બીમા યોજના (PMFBY)",
        "ncipm_label": "ICAR-NCIPM ટેકનિકલ સંદર્ભ"
    },
    "বাংলা": {
        "title": "🌱 কৃষিরক্ষক: স্মার্ট জৈব নিয়ন্ত্রণ ও ফসল রোগ নজরদারি ব্যবস্থা",
        "subtitle": "কৃষি বিভাগ প্রাতিষ্ঠানিক সিদ্ধান্ত সহায়তা ব্যবস্থা",
        "sidebar_header": "📍 খামারের ক্ষুদ্র আবহাওয়া ও অবস্থান",
        "tab1_title": "🔬 রোগ নির্ণয় ও উদ্ভিদ রোগতত্ত্ব",
        "tab_chat_title": "💬 কৃষিরক্ষক AI চ্যাটবট / সহায়ক",
        "tab2_title": "👥 নিবন্ধিত কৃষক তথ্যপঞ্জী",
        "upload_label": "যেকোনো ধাপের সংক্রামিত পাতার ছবি আপলোড করুন",
        "pathogen": "শনাক্তকৃত প্যাথোজেন / পোকা",
        "trophic": "পুষ্টি গ্রহণের ধরন (Trophic Mode)",
        "entry": "সংক্রমণ পথ (Entry Route)",
        "susceptible": "সর্বাধিক সংবেদনশীল ফসলের পর্যায়",
        "r_genes": "প্রতিরোধী বৈশিষ্ট্য (R-Genes)",
        "biocontrol": "সমন্বিত বালাই ব্যবস্থাপনা (IPM) ও জৈব নিয়ন্ত্রণ",
        "varieties": "অনুমোদিত প্রতিরোধী জাত",
        "send_sms_btn": "🚨 নিবন্ধিত কৃষকদের SMS সতর্কতা পাঠান",
        "sms_success": "সকল নিবন্ধিত কৃষককে সফলভাবে SMS সতর্কতা পাঠানো হয়েছে!",
        "healthy_note": "ফসল সম্পূর্ণ সুস্থ রয়েছে। SMS সতর্কতার প্রয়োজন নেই।",
        "ood_warn": "⚠️ সিদ্ধান্তহীন বা ব্যতিক্রমী নমুনা",
        "ood_info": "আপলোড করা নমুনাটি মূল ক্লাসের সাথে মেলে না বা পুষ্টির অভাব হতে পারে।",
        "detection_scale": "🔬 জৈবিক আকার ও ক্ষতের ব্যাপ্তি",
        "inf_stage": "📊 বর্তমান সংক্রমণের পর্যায়",
        "threshold": "⚠️ সতর্কতা মাত্রা / অর্থনৈতিক ক্ষতির সীমা (ETL)",
        "chem_sol": "🧪 অনুমোদিত রাসায়নিক কীটনাশক ও সঠিক মাত্রা",
        "bio_sol": "🌿 প্রত্যয়িত জৈব ও প্রাকৃতিক বিকল্প",
        "resources": "📞 কিষাণ হেল্পলাইন ও জরুরি সহায়তা কেন্দ্র",
        "leaf_stage_title": "🍃 পাতায় ক্ষতির পর্যায়",
        "pest_stage_title": "🐛 পোকা বা রোগের জৈবিক পর্যায়",
        "visual_heatmap": "🔬 ক্ষত ও ক্ষতির হিটম্যাপ বিশ্লেষণ",
        "preventive_header": "🛡️ আগাম ও প্রতিরোধমূলক কৃষি ব্যবস্থা",
        "chat_placeholder": "কীটনাশকের মাত্রা, জৈব বালাইনাশক, আবহাওয়া সম্পর্কে জিজ্ঞাসা করুন...",
        "anomaly_meter_title": "🛡️ নমুনা বৈধতা ও অসঙ্গতি (Anomaly) পরিমাপক",
        "anomaly_risk": "অসঙ্গতি / OOD ঝুঁকি সূচক",
        "foliar_integrity": "পাতার কলার অখণ্ডতা",
        "report_header": "📄 অফিসিয়াল প্রাতিষ্ঠানিক কৃষি পরামর্শ প্রতিবেদন",
        "report_btn": "📄 প্রিন্টযোগ্য পরামর্শ রিপোর্ট তৈরি করুন (Print / PDF)",
        "report_download_btn": "📥 অফিসিয়াল ফিল্ড রিপোর্ট ডাউনলোড করুন (HTML / Print)",
        "disclaimer_header": "⚠️ বাধ্যতামূলক প্রাতিষ্ঠানিক AI পরামর্শ অস্বীকৃতি (Disclaimer)",
        "disclaimer_text": "কৃষি সহায়ক হলো একটি প্রাতিষ্ঠানিক কৃত্রিম বুদ্ধিমত্তা (AI) সিদ্ধান্ত সহায়তা ব্যবস্থা। কোনো রাসায়নিক কীটনাশক প্রয়োগের পূর্বে আপনার নিকটস্থ কৃষি বিজ্ঞান কেন্দ্র (KVK) বা কৃষি কর্মকর্তার পরামর্শ নিন। CIBRC অনুমোদিত সঠিক মাত্রা, ব্যক্তিগত সুরক্ষা সরঞ্জাম (PPE) এবং ফসল তোলার পূর্ববর্তী অপেক্ষা সময় (PHI) কঠোরভাবে মেনে চলুন।",
        "disclaimer_checkbox": "আমি শর্তাবলী পড়েছি এবং স্বীকার করছি যে এই AI পরামর্শ শুধুমাত্র সিদ্ধান্ত সহায়তার জন্য।",
        "disclaimer_accept_btn": "শর্তাবলী স্বীকার করে কৃষি সহায়ক শুরু করুন",
        "pmfby_label": "প্রধানমন্ত্রী ফসল বীমা যোজনা (PMFBY)",
        "ncipm_label": "আইসিএআর-এনসিআইপিএম (ICAR-NCIPM) প্রযুক্তিগত রেফারেন্স"
    }
}

# --- SIDEBAR CONTROLS ---
lang = st.sidebar.selectbox(
    "🌐 Language / भाषा निवडा / ভাষা নির্বাচন করুন",
    list(I18N.keys())
)
t = I18N[lang]

st.title(t["title"])
st.caption(t["subtitle"])

st.sidebar.header(t["sidebar_header"])
place_input = st.sidebar.text_input(
    "🔍 Location / Village / City",
    value="Akola",
    help="Type any village, taluka, or district in India (e.g., Wardha, Bhatinda, Guntur, Cuttack)"
)

lat, lon, resolved_label = geocode_indian_place(place_input)
st.sidebar.caption(f"📍 Mapped: **{resolved_label}**")

weather = fetch_current_weather(lat, lon)
gdd = calculate_daily_gdd(weather.get("temp_max", 32.0), weather.get("temp_min", 24.0))

st.sidebar.metric("Temperature", f"{weather.get('temperature', 30.0)} °C")
st.sidebar.metric("Humidity", f"{weather.get('humidity', 70)} %")
st.sidebar.metric("Condition", str(weather.get("condition", "Normal")).title())
st.sidebar.metric("Daily GDD (Base 12°C)", f"{gdd} DD")
st.sidebar.caption(f"Coordinates: `{lat:.4f}°N, {lon:.4f}°E`")
st.sidebar.caption(f"Source: `{weather.get('source', 'Agro Model')}`")

# Optional Gemini API Key input
st.sidebar.markdown("---")
st.sidebar.markdown("### ✨ Advanced AI Engine")
env_key = os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))
gemini_key = st.sidebar.text_input(
    "🔑 Gemini API Key (Optional)",
    value=env_key,
    type="password",
    help="Enter Google Gemini API Key for multimodal AI leaf vision and chat."
)
if gemini_key:
    st.sidebar.success("✨ Gemini Key Detected")
    if st.sidebar.button("🧪 Test API Key Connection"):
        with st.sidebar.spinner("Testing Gemini connection..."):
            test_res = test_gemini_connection(gemini_key)
            if test_res.get("success"):
                st.sidebar.success(f"✅ {test_res.get('message')}")
            else:
                st.sidebar.error(f"❌ {test_res.get('message')}")
else:
    st.sidebar.info("💡 Tip: Enter key to enable Gemini Vision & Chat, or leave blank to use built-in local models.")

# --- MAIN APPLICATION TABS (Diagnosis, AI Chatbot, Farmer Registry) ---
tab1, tab_chat, tab2 = st.tabs([t["tab1_title"], t["tab_chat_title"], t["tab2_title"]])

with tab1:
    uploaded = st.file_uploader(t["upload_label"], type=["jpg", "png", "jpeg"])
    if uploaded:
        img = Image.open(uploaded)
        
        # 1. Base ML & CV Stage inference
        res = run_inference(img, weather)
        
        # 2. If Gemini API key is present, enhance with Gemini multimodal vision
        if gemini_key and gemini_key.strip():
            with st.spinner("🤖 Consulting Gemini Multimodal AI Vision..."):
                gemini_res, gemini_err = diagnose_with_gemini(img, gemini_key.strip(), lang)
                if gemini_res:
                    if gemini_res.get("is_valid_crop_leaf") is False:
                        res["status"] = "ANOMALY_NON_PLANT"
                        res["disease_label"] = "Non-Crop / Invalid Specimen"
                        if "anomaly" in res:
                            res["anomaly"]["anomaly_status"] = "OUT_OF_DISTRIBUTION"
                            res["anomaly"]["anomaly_type"] = "NON_PLANT_OOD"
                            res["anomaly"]["badge_label"] = "🔴 Non-Plant / Foreign Specimen"
                            res["anomaly"]["badge_color"] = "#dc3545"
                            res["anomaly"]["anomaly_score"] = 99.0
                            if gemini_res.get("anomaly_warning"):
                                res["anomaly"]["explanation"] = gemini_res["anomaly_warning"]
                    else:
                        # Enrich diagnosis with Gemini's high-precision classification
                        res["disease_label"] = gemini_res.get("disease_label", res["disease_label"])
                        res["confidence"] = gemini_res.get("confidence", res["confidence"])
                        res["status"] = "CONFIRMED"
                        if "leaf_stage" in gemini_res and isinstance(gemini_res["leaf_stage"], dict):
                            res["leaf_stage"].update(gemini_res["leaf_stage"])
                        if "pest_stage" in gemini_res and isinstance(gemini_res["pest_stage"], dict):
                            res["pest_stage"].update(gemini_res["pest_stage"])
                        if "chemical_options" in gemini_res and gemini_res["chemical_options"]:
                            res["chemical_options"] = gemini_res["chemical_options"]
                        if "bio_options" in gemini_res and gemini_res["bio_options"]:
                            res["bio_options"] = gemini_res["bio_options"]
                        if "preventive_measures" in gemini_res and gemini_res["preventive_measures"]:
                            res["preventive_measures"] = gemini_res["preventive_measures"]
                        if "details" in gemini_res and gemini_res["details"]:
                            res["details"].update(gemini_res["details"])
                    res["ai_model_source"] = gemini_res.get("source", "Gemini Multimodal AI")
                    st.success(f"✨ **AI Diagnosis Generated by {res['ai_model_source']}!**")
                else:
                    st.warning(f"⚠️ Gemini Vision could not process image: `{gemini_err}`. Using local MobileNetV2 fallback.")

        st.session_state.current_diagnosis = res
        
        # Dual-column layout: Uploaded Original vs Visual Lesion Segmentation Overlay
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.markdown("#### 📷 Uploaded Leaf Specimen")
            st.image(img, use_container_width=True)
            
        with col_img2:
            st.markdown(f"#### {t['visual_heatmap']}")
            if res.get("visual_overlay"):
                st.image(res["visual_overlay"], use_container_width=True)

        st.markdown("---")
        
        # --- SPECIMEN VALIDITY & ANOMALY DETECTION METER ---
        anomaly = res.get("anomaly", {})
        if anomaly:
            st.markdown(f"### {t.get('anomaly_meter_title', '🛡️ Specimen Validity & Foliar Anomaly Meter')}")
            
            anom_c1, anom_c2, anom_c3, anom_c4 = st.columns([1.6, 1, 1, 1])
            with anom_c1:
                badge_col = anomaly.get("badge_color", "#28a745")
                badge_lbl = anomaly.get("badge_label", "🟢 Verified Crop Foliar Specimen")
                st.markdown(
                    f"<div style='margin-top:6px; font-weight:bold; font-size:15px; color:{badge_col};'>"
                    f"{badge_lbl}</div>",
                    unsafe_allow_html=True
                )
                anom_score = float(anomaly.get("anomaly_score", 0.0))
                st.caption(f"Status: `{anomaly.get('anomaly_status', 'IN_DISTRIBUTION')}` | Type: `{anomaly.get('anomaly_type', 'NORMAL')}`")
            with anom_c2:
                st.metric(t.get("foliar_integrity", "Foliar Tissue"), f"{anomaly.get('foliar_percentage', 100)} %")
            with anom_c3:
                st.metric(t.get("anomaly_risk", "Anomaly Risk"), f"{anomaly.get('anomaly_score', 0)} %")
            with anom_c4:
                st.metric("Model Uncertainty", f"{anomaly.get('entropy_index', 0)} %")

            # Progress gauge for anomaly risk
            st.progress(min(max(int(anom_score), 0), 100))
            
            # Advisory callout
            st.markdown(
                f"<div style='padding: 10px 14px; border-radius: 6px; background: rgba(0,0,0,0.03); border-left: 4px solid {badge_col}; margin-bottom: 12px;'>"
                f"<strong style='color:{badge_col};'>Evaluation:</strong> {anomaly.get('explanation', '')}<br/>"
                f"<strong>Recommended Action:</strong> {anomaly.get('recommendation', '')}"
                f"</div>",
                unsafe_allow_html=True
            )
            st.markdown("---")
        
        # Diagnostic Outcome Header
        disease = res.get('disease_label', 'unknown')
        confidence = res.get('confidence', 0)
        status = res.get("status", "CONFIRMED")
        leaf_stage = res.get("leaf_stage", {})
        pest_stage = res.get("pest_stage", {})

        if status == "ANOMALY_NON_PLANT":
            st.error("🚫 **Specimen Rejected: Non-Plant / Foreign Object Detected**")
            st.warning("The uploaded image contains insufficient foliar tissue to constitute an agricultural crop leaf. To prevent hazardous misapplication of agricultural chemicals, diagnosis and pesticide prescriptions are withheld.")
            st.info("💡 **Farmer Instruction:** Please take a well-lit, close-up photograph directly facing a single cotton or rice leaf and re-upload.")
        elif status == "ANOMALY_NOVEL_PATHOLOGY":
            st.error("⚠️ **Alert: Suspected Novel or Unregistered Foliar Pathology**")
            st.warning("Visual lesion pattern shows significant statistical divergence from the 14 standard trained pathogen classes. This indicates a novel fungal/bacterial strain, extreme viral mutation, or severe complex abiotic damage.")
            st.info("🔬 **Action Required:** Isolate affected plants in the field and transport fresh leaf samples inside an ice cooler to your nearest Krishi Vigyan Kendra (KVK) or State Agricultural University plant pathology clinic for PCR molecular confirmation.")
            
            res_c1, res_c2, res_c3 = st.columns([2, 1, 1])
            with res_c1:
                st.subheader("Diagnosis: Novel Foliar Pathology")
                st.caption(f"AI Engine: **{res.get('ai_model_source', 'MobileNetV2 + Anomaly Engine')}** | Classification: `Out-of-Distribution`")
            with res_c2:
                st.metric("Lesion Coverage", f"{leaf_stage.get('lesion_percentage', 0)} %")
            with res_c3:
                st.metric("Photosynthetic Health", f"{leaf_stage.get('photosynthetic_health', 100)} %")
        elif status == "OUT_OF_SCOPE":
            st.warning(f"**{t['ood_warn']} (Confidence: {confidence}%)**")
            st.info(t["ood_info"])
        else:
            disease_clean = disease.replace('_', ' ').title()
            res_c1, res_c2, res_c3 = st.columns([2, 1, 1])
            with res_c1:
                st.subheader(f"Diagnosis: {disease_clean}")
                st.progress(min(int(confidence), 100))
                model_info = res.get("ai_model_source", "MobileNetV2 + Computer Vision")
                st.caption(f"AI Model: **{model_info}** | Confidence: **{confidence}%** | Status: `{status}`")
            with res_c2:
                st.metric("Lesion Coverage", f"{leaf_stage.get('lesion_percentage', 0)} %")
            with res_c3:
                st.metric("Photosynthetic Health", f"{leaf_stage.get('photosynthetic_health', 100)} %")

            # --- DUAL STAGE IDENTIFICATION CARDS (LEAF STAGE + PEST LIFECYCLE STAGE) ---
            st.markdown("---")
            stage_c1, stage_c2 = st.columns(2)
            
            with stage_c1:
                st.markdown(f"### {t['leaf_stage_title']}")
                stage_color = leaf_stage.get('severity_color', '#28a745')
                st.markdown(
                    f"<div style='padding: 14px; border-radius: 8px; border-left: 6px solid {stage_color}; background: rgba(0,0,0,0.03);'>"
                    f"<h4 style='margin:0; color: {stage_color};'>{leaf_stage.get('title', 'Stage 1')}</h4>"
                    f"<p style='margin-top:6px; margin-bottom:0;'>{leaf_stage.get('description', '')}</p>"
                    f"<span style='display:inline-block; margin-top:8px; font-weight:bold; font-size:12px; background:{stage_color}22; color:{stage_color}; padding:3px 8px; border-radius:4px;'>Severity: {leaf_stage.get('severity_label', 'Normal')}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

            with stage_c2:
                st.markdown(f"### {t['pest_stage_title']}")
                st.markdown(
                    f"<div style='padding: 14px; border-radius: 8px; border-left: 6px solid #17a2b8; background: rgba(0,0,0,0.03);'>"
                    f"<h4 style='margin:0; color: #17a2b8;'>{pest_stage.get('stage_name', 'Stage 1')}</h4>"
                    f"<p style='margin-top:6px; margin-bottom:0;'>{pest_stage.get('biological_process', '')}</p>"
                    f"<p style='margin-top:8px; margin-bottom:0; font-size:13px;'>🚨 <strong>ETL Status:</strong> {pest_stage.get('etl_status', 'Monitored')}</p>"
                    f"</div>",
                    unsafe_allow_html=True
                )

            # --- SMS BROADCAST ACTION SECTION ---
            st.markdown("---")
            if disease != "healthy":
                alert = evaluate_outbreak_cluster(lat, lon, disease) or {}
                dispatch = alert.get("sms_dispatch") or {}

                lang_code_map = {
                    "English": "message_en",
                    "मराठी": "message_mr",
                    "हिंदी": "message_hi",
                    "বাংলা": "message_bn",
                    "తెలుగు": "message_te",
                    "தமிழ்": "message_ta",
                    "ಕನ್ನಡ": "message_kn",
                    "ਪੰਜਾਬੀ": "message_pa",
                    "ગુજરાતી": "message_gu"
                }
                msg_key = lang_code_map.get(lang, "message_en")
                msg_text = dispatch.get(msg_key) or dispatch.get("message_en", f"🚨 KrishiRakshak Alert: Outbreak of {disease_clean} detected nearby. Apply recommended IPM measures immediately.")
                
                st.info(f"**SMS Template Preview ({lang}):**\n\n> {msg_text}")
                
                if st.button(t["send_sms_btn"], type="primary"):
                    recipient_count = len(st.session_state.farmers_registry)
                    st.success(f"{t['sms_success']} ({recipient_count} Farmers)")
            else:
                st.success(f"✅ {t['healthy_note']}")

        # --- HOST-PATHOGEN INTERACTION (PPI) PROFILE & EXTENDED PROTOCOLS ---
        if status != "ANOMALY_NON_PLANT":
            details = res.get("details", {})
            st.markdown("---")
            st.markdown("### 🧬 Host-Pathogen Interaction Profile")
        
            ppi_col_left, ppi_col_right = st.columns(2)
            with ppi_col_left:
                st.markdown(f"**{t['pathogen']}:** `{details.get('pathogen_agent', details.get('pathogen', 'N/A'))}`")
                st.markdown(f"**{t['trophic']}:** `{details.get('trophic_type', 'N/A')}`")
                st.markdown(f"**{t['entry']}:** {details.get('entry_route', 'N/A')}")
            
            with ppi_col_right:
                st.markdown(f"**{t['r_genes']}:** `{details.get('key_r_genes', details.get('r_genes', 'N/A'))}`")
                st.markdown(f"**{t['susceptible']}:** {details.get('susceptible_stage', 'N/A')}")
                st.markdown(f"**{t['varieties']}:** {', '.join(details.get('resistant_cultivars', ['Regional Recommended']))}")
            
            st.markdown(f"**{t['biocontrol']}:**")
            for step in details.get("biocontrol_ipm", []):
                st.write(f"- {step}")

            # --- EXTENDED PATHOLOGY MATRIX (Size, Stages, Alternatives & Resources) ---
            raw_disease = res.get('disease_label', 'healthy')
            matrix = EXPANDED_PATHOLOGY_DB.get(raw_disease, {})

            if matrix and raw_disease != "healthy":
                st.markdown("---")
                
                # 1. Biological Physical Scale & Infection Stage
                st.subheader(t["detection_scale"])
                sc1, sc2 = st.columns(2)
                with sc1:
                    st.markdown(f"🔬 **Microscopic Organism Range:**\n`{matrix['detection_scale']['microscopic_size']}`")
                    st.markdown(f"📏 **Visible Lesion Damage Range:**\n`{matrix['detection_scale']['macroscopic_lesion_range']}`")
                with sc2:
                    st.markdown(f"📊 **Current Infection Classification:**\n**{matrix['infection_stage']}**")
                    st.markdown(f"🌱 **Susceptible Crop Phase:**\n`{matrix['crop_phenology_sync']}`")
                
                # Stage progression breakdown
                st.markdown("#### ⏳ Stage Progression Breakdown")
                prog = matrix.get("stage_progression", {})
                p1, p2, p3 = st.columns(3)
                
                # Highlight current active stage
                curr_stage_num = leaf_stage.get("stage_num", 1)
                if curr_stage_num == 1:
                    p1.success(f"🟢 **Initial Stage (Active Diagnosis)**\n\n{prog.get('initial')}")
                    p2.info(f"🟠 **Medium Stage**\n\n{prog.get('medium')}")
                    p3.warning(f"🔴 **Late / Terminal**\n\n{prog.get('late')}")
                elif curr_stage_num == 2:
                    p1.info(f"🟡 **Initial Stage**\n\n{prog.get('initial')}")
                    p2.warning(f"🟠 **Medium Stage (Active Diagnosis)**\n\n{prog.get('medium')}")
                    p3.error(f"🔴 **Late / Terminal**\n\n{prog.get('late')}")
                else:
                    p1.info(f"🟡 **Initial Stage**\n\n{prog.get('initial')}")
                    p2.warning(f"🟠 **Medium Stage**\n\n{prog.get('medium')}")
                    p3.error(f"🔴 **Late / Terminal (Active Diagnosis)**\n\n{prog.get('late')}")

                # 2. Quantified Warning Threshold (ETL)
                st.markdown(f"### {t['threshold']}")
                st.error(f"🚨 **Action Threshold:** {matrix['warning_threshold']}")

                # 3. Tiered Treatment Protocols & Exact Chemical / Bio Formulations
                st.markdown("---")
                st.subheader("💊 Tiered Treatment Protocols & Application Guidelines")
                treat_c1, treat_c2 = st.columns(2)

                with treat_c1:
                    st.markdown(f"#### {t['chem_sol']}")
                    chems_to_show = res.get("chemical_options") or matrix.get('management_alternatives', {}).get('chemical_options', [])
                    for chem in chems_to_show:
                        dose_info = chem.get('dose_per_liter', chem.get('dosage', 'Standard dilution'))
                        tank_info = chem.get('dose_per_15l_pump', '')
                        acre_info = chem.get('dose_per_acre', '')
                        phi_info = f" | *PHI:* `{chem.get('phi_days')} days`" if chem.get('phi_days') else ""
                        tank_line = f"  \n  *15L Tank:* `{tank_info}` | *Acre:* `{acre_info}`{phi_info}" if tank_info else ""
                        st.markdown(f"- **{chem['name']}**  \n  *Dilution:* `{dose_info}`{tank_line}")

                with treat_c2:
                    st.markdown(f"#### {t['bio_sol']}")
                    bios_to_show = res.get("bio_options") or matrix.get('management_alternatives', {}).get('bio_organic_alternatives', [])
                    for bio in bios_to_show:
                        dose_info = bio.get('dose_per_liter', bio.get('dosage', 'Standard application'))
                        tank_info = bio.get('dose_per_15l_pump', '')
                        acre_info = bio.get('dose_per_acre', '')
                        tank_line = f"  \n  *15L Tank:* `{tank_info}` | *Acre:* `{acre_info}`" if tank_info else ""
                        st.markdown(f"- **{bio['name']}**  \n  *Application:* `{dose_info}`{tank_line}")

                # 4. Consumer Toxicology, MRL & Residue Mitigation Desk
                st.markdown("---")
                st.subheader("🛡️ Consumer Safety, Chemical Toxicity & Food Safety Standards")
                
                primary_chem = "Unspecified"
                chem_opts = matrix.get('management_alternatives', {}).get('chemical_options', [])
                if chem_opts:
                    primary_chem = chem_opts[0]['name']

                consumer_data = get_consumer_safety_profile(primary_chem)
                tox_c1, tox_c2 = st.columns(2)

                with tox_c1:
                    st.markdown(f"**Target Chemical Compound:** `{primary_chem}`")
                    st.markdown(f"**Toxicological Class:** `{consumer_data.get('class', 'Agricultural Chemical')}`")
                    st.markdown(f"**Mammalian Toxicity Rating:** **{consumer_data.get('human_toxicity_level', 'Moderate')}**")
                    st.error(f"⚠️ **Acute Symptoms (If Consumed Exceeding Limits):**\n\n{consumer_data.get('acute_symptoms', 'Gastrointestinal discomfort')}")

                with tox_c2:
                    st.warning(f"🧬 **Long-Term / Chronic Dietary Risks:**\n\n{consumer_data.get('chronic_risks', 'Hepatic and renal metabolic burden')}")
                    st.info(f"👶 **High Vulnerability Demographics:** {consumer_data.get('vulnerable_groups', 'Children, nursing mothers, elderly')}")

                st.markdown("#### 🧼 Post-Harvest Residue Reduction & Consumer Washing Protocols")
                wash_1, wash_2 = st.columns(2)
                with wash_1:
                    st.markdown(f"""
                    * **Pre-Harvest Interval (PHI):** Farmers must strictly adhere to the mandatory waiting period before harvest to allow chemical photolysis and breakdown.
                    * **Household Decontamination:** {consumer_data.get('decontamination_method', 'Rinse under running water for 60 seconds.')}
                    """)
                with wash_2:
                    st.markdown("""
                    * **2% Salt-Water Soak:** Soaking harvested vegetables/produce in a 2% salt solution for 10–15 minutes eliminates up to 70% of surface contact residues.
                    * **Peeling & Discarding:** Always peel waxy outer surfaces and discard outer wrapper leaves of treated crops.
                    """)

                # 5. Critical Farmer Lifelines & Emergency Contacts
                st.markdown("---")
                st.subheader(t["resources"])
                r1, r2, r3, r4 = st.columns(4)
                res_dict = matrix.get("farmer_resources", {})
                r1.metric("📞 Kisan Call Center", "1800-180-1551", "National Toll-Free")
                r2.metric(f"🌾 {t['pmfby_label']}", "14447", "Crop Loss Intimation")
                r3.info(f"🏛️ **{t['ncipm_label']}:**\nICAR-NCIPM National IPM Reference & Technical Verification Desk, New Delhi")
                r4.info(f"🧪 **Diagnostic/Soil Clinic & KVK:**\n{res_dict.get('soil_testing_lab', 'District KVK Soil Testing Lab')}")

            # --- LIFECYCLE & EPIDEMIOLOGICAL DEGREE-DAY MODEL ---
            lifecycle_data = LIFECYCLE_PROFILES.get(raw_disease, None)

            if lifecycle_data and raw_disease != "healthy":
                st.markdown("---")
                st.subheader("🧬 Epidemiological Lifecycle & Degree-Day Vulnerability Model")
                st.caption(f"Target Biological Profile: **{lifecycle_data.get('organism_type')}**")

                stages = lifecycle_data.get("stages", [])
                for idx, stage in enumerate(stages, 1):
                    with st.expander(
                        f"Phase {idx}: {stage['stage_name']} ({stage['duration_days']} | {stage['thermal_requirement']})",
                        expanded=(idx == 1)
                    ):
                        c1, c2 = st.columns([3, 2])
                        with c1:
                            st.markdown(f"**Biological Progression:**\n{stage['biological_process']}")
                            st.markdown(f"**Susceptible Crop Window:** `{stage['vulnerability_window']}`")
                        with c2:
                            st.info(f"🎯 **Targeted Precision Action:**\n{stage['targeted_intervention']}")

            # --- FEATURE A: PRINTABLE INSTITUTIONAL ADVISORY REPORT GENERATOR ---
            st.markdown("---")
            st.subheader(t["report_header"])
            st.caption("Generate an official, printable bilingual/multilingual institutional field report with visual specimen evidence, heatmap analysis, biological stages, CIBRC chemical dosages, and emergency lifelines.")

            advisory_html = generate_advisory_html(
                diagnosis=res,
                weather=weather,
                location_name=resolved_label,
                lat=lat,
                lon=lon,
                original_img=img,
                heatmap_img=res.get("visual_overlay") or res.get("heatmap_annotated"),
                language=lang
            )

            rep_c1, rep_c2 = st.columns([1, 2])
            with rep_c1:
                filename_ts = datetime.now().strftime('%Y%m%d_%H%M%S')
                st.download_button(
                    label=t["report_download_btn"],
                    data=advisory_html,
                    file_name=f"KrishiRakshak_Advisory_{filename_ts}.html",
                    mime="text/html",
                    type="primary",
                    use_container_width=True
                )
            with rep_c2:
                st.info("💡 **Print / PDF Instructions:** Download the HTML report above and open in your browser, then press `Ctrl+P` (or `Cmd+P` on Mac) to print or save as an official PDF.")

            with st.expander("👁️ Preview Official Advisory Report / अहवाल पूर्वावलोकन", expanded=False):
                components.html(advisory_html, height=750, scrolling=True)

# --- TAB 2: MULTILINGUAL AI CHATBOX / ASSISTANT ---
with tab_chat:
    st.subheader(t["tab_chat_title"])
    st.caption("Ask questions about your uploaded leaf diagnosis, exact pump dosages, organic bio-remedies, and weather in your preferred language.")

    # --- FEATURE B: MANDATORY INSTITUTIONAL AI DISCLAIMER GATE ---
    if not st.session_state.get("ai_disclaimer_accepted", False):
        st.markdown(f"### {t['disclaimer_header']}")
        st.warning(t["disclaimer_text"])
        st.info(f"""
        🏛️ **Institutional Regulatory Framework & Official Lifelines:**
        * **Kisan Call Center (National Toll-Free):** `1800-180-1551`
        * **{t['pmfby_label']}:** `14447`
        * **{t['ncipm_label']}:** ICAR - National Centre for Integrated Pest Management, New Delhi
        * **Regulatory Authority:** CIBRC Approved Label Claims & FSSAI Residue Mitigation Protocols
        """)
        
        disc_c1, disc_c2 = st.columns([3, 1])
        with disc_c1:
            disc_agree = st.checkbox(t["disclaimer_checkbox"], key="chk_ai_disclaimer")
        with disc_c2:
            if st.button(t["disclaimer_accept_btn"], type="primary", disabled=not disc_agree, use_container_width=True):
                st.session_state.ai_disclaimer_accepted = True
                st.rerun()
    else:
        # Engine Status Banner & Acceptance Pill
        col_eng, col_reset = st.columns([3, 1])
        with col_eng:
            if gemini_key and gemini_key.strip():
                st.success("✨ **Chat Engine Active:** Google Gemini AI (Multimodal Multilingual)")
            else:
                st.info("💻 **Chat Engine Active:** Built-in Multilingual Agronomist Knowledge Engine")
        with col_reset:
            st.caption("🛡️ AI Disclaimer Accepted")
            if st.button("🔄 Review Terms", key="reset_ai_disclaimer", help="Revisit institutional AI disclaimer terms"):
                st.session_state.ai_disclaimer_accepted = False
                st.rerun()

        # Show active diagnosis context pill if available
        active_diag = st.session_state.get("current_diagnosis")
        if active_diag and active_diag.get("status") in ["CONFIRMED", "EARLY_INCUBATION"]:
            diag_name = active_diag.get("disease_label", "").replace("_", " ").title()
            st_title = active_diag.get("leaf_stage", {}).get("title", "Stage 1")
            st.info(f"🔍 **Active Diagnosis Context:** `{diag_name}` | **Leaf Stage:** `{st_title}` | **Weather:** `{weather.get('temperature', 30)}°C, {weather.get('humidity', 70)}% RH`")
        else:
            st.info("💡 *Tip: Upload an infected leaf in Tab 1 to give the chatbot instant context of your exact crop disease and stage.*")

        # Quick Suggestion Chips
        chips = QUICK_CHIPS.get(lang, QUICK_CHIPS["English"])
        st.markdown("**⚡ Quick One-Click Questions / त्वरीत प्रश्न:**")
        chip_cols = st.columns(len(chips))
        clicked_chip = None
        for idx, chip in enumerate(chips):
            with chip_cols[idx]:
                if st.button(chip, key=f"chip_{idx}"):
                    clicked_chip = chip

        st.markdown("---")

        # In-page Question Input Form
        st.markdown("#### ✍️ Ask a Question:")
        with st.form("chat_query_form", clear_on_submit=True):
            c_in1, c_in2 = st.columns([5, 1])
            with c_in1:
                form_query = st.text_input(
                    "Question",
                    placeholder=t["chat_placeholder"],
                    label_visibility="collapsed"
                )
            with c_in2:
                form_submit = st.form_submit_button("📨 Ask", type="primary", use_container_width=True)

        # Display Chat History
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Determine user query from any input method
        user_query = None
        if clicked_chip:
            user_query = clicked_chip
        elif form_submit and form_query.strip():
            user_query = form_query.strip()
        
        # Bottom floating chat input as additional option
        bottom_query = st.chat_input(t["chat_placeholder"])
        if bottom_query:
            user_query = bottom_query

        if user_query:
            # Add user message to history
            st.session_state.chat_messages.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)

            # Generate response: try Gemini if key provided, else built-in multilingual agronomist
            with st.chat_message("assistant"):
                with st.spinner("AI Agronomist is analyzing..."):
                    response_text = None
                    if gemini_key and gemini_key.strip():
                        response_text = chat_with_gemini(
                            query=user_query,
                            api_key=gemini_key.strip(),
                            lang=lang,
                            diagnosis_context=st.session_state.get("current_diagnosis"),
                            weather_context=weather,
                            chat_history=st.session_state.chat_messages
                        )
                    
                    if not response_text:
                        response_text = generate_chat_response(
                            query=user_query,
                            language=lang,
                            diagnosis_context=st.session_state.get("current_diagnosis"),
                            weather_context=weather
                        )
                    st.markdown(response_text)
                    st.session_state.chat_messages.append({"role": "assistant", "content": response_text})

        # Clear chat button
        if st.session_state.chat_messages:
            if st.button("🧹 Clear Chat History / संवाद साफ करा", key="clear_chat_history"):
                st.session_state.chat_messages = []
                st.rerun()

# --- TAB 3: REGISTERED FARMERS REGISTRY ---
with tab2:
    st.subheader("👥 Registered Farmers Database")
    st.caption("Registered farmers in this cluster who receive automated SMS broadcasts during active outbreaks.")
    
    df_farmers = pd.DataFrame(st.session_state.farmers_registry)
    st.dataframe(df_farmers, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("#### ➕ Register New Farmer")
    with st.form("add_farmer_form", clear_on_submit=True):
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        name = f_col1.text_input("Farmer Name")
        phone = f_col2.text_input("Mobile Number (+91...)")
        village = f_col3.text_input("Village / Circle")
        crop = f_col4.selectbox("Cultivated Crop", ["Cotton", "Paddy", "Multi-Crop"])
        
        submitted = st.form_submit_button("Add Farmer Entry")
        if submitted:
            if name.strip() and phone.strip():
                st.session_state.farmers_registry.append({
                    "Name": name.strip(),
                    "Phone": phone.strip(),
                    "Village": village.strip() if village else "General",
                    "Crop": crop
                })
                st.success(f"Farmer '{name}' registered successfully.")
                st.rerun()
            else:
                st.error("Please enter both Farmer Name and Mobile Number.")