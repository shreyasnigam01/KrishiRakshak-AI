"""
backend/chatbot_engine.py
Multilingual Agronomic AI Chatbot Engine for KrishiRakshak
Supports English, Marathi, Hindi, Telugu, Tamil, Kannada, Punjabi, and Gujarati.
Provides context-aware answers regarding crop diseases, leaf and pest stages,
tank dosages, organic remedies, spraying safety, and weather suitability.
"""

import os
import re
import json
from typing import Dict, Any, List, Optional

# Supported language codes and names
LANG_MAP = {
    "English": "en",
    "मराठी": "mr",
    "हिंदी": "hi",
    "తెలుగు": "te",
    "தமிழ்": "ta",
    "ಕನ್ನಡ": "kn",
    "ਪੰਜਾਬੀ": "pa",
    "ગુજરાતી": "gu",
    "বাংলা": "bn"
}

# Quick suggestion prompt chips in all 9 languages
QUICK_CHIPS = {
    "English": [
        "How much pesticide to put in a 16-liter pump?",
        "What are the best organic / bio-control remedies?",
        "Can I spray today given the current weather?",
        "How to prevent this pest next season?",
        "Is this chemical safe for cattle and food?"
    ],
    "मराठी": [
        "१६ लिटर पंपासाठी किती औषध टाकावे?",
        "सेंद्रिय किंवा जैविक उपाय कोणते आहेत?",
        "आजच्या हवामानात फवारणी करावी का?",
        "पुढील हंगामात हा प्रादुर्भाव कसा रोखावा?",
        "हे औषध जनावरांसाठी व खाण्यासाठी सुरक्षित आहे का?"
    ],
    "हिंदी": [
        "१६ लीटर के पंप में कितनी दवा डालें?",
        "जैविक एवं प्राकृतिक उपचार क्या हैं?",
        "आज के मौसम में छिड़काव करना सही रहेगा?",
        "अगले मौसम में इस कीट से कैसे बचें?",
        "क्या यह रसायन मवेशियों और भोजन के लिए सुरक्षित है?"
    ],
    "বাংলা": [
        "১৬ লিটার স্প্রেয়ার পাম্পে কতটা কীটনাশক মেশাতে হবে?",
        "সেরা জৈব ও প্রাকৃতিক প্রতিকারগুলি কী কী?",
        "আজকের আবহাওয়ায় কি স্প্রে করা নিরাপদ?",
        "পরের মরসুমে এই পোকার আক্রমণ কীভাবে রোধ করবেন?",
        "এই কীটনাশক কি গবাদি পশু ও খাদ্যের জন্য নিরাপদ?"
    ],
    "తెలుగు": [
        "16 లీటర్ల పంపులో ఎంత మందు కలపాలి?",
        "సేంద్రీయ మరియు సహజ నివారణలు ఏమిటి?",
        "నేటి వాతావరణంలో మందు పిచికారీ చేయవచ్చా?",
        "వచ్చే సీజన్‌లో ఈ తెగులు రాకుండా ఎలా నివారించాలి?",
        "ఈ రసాయనం పశువులకు మరియు ఆహారానికి సురక్షితమేనా?"
    ],
    "தமிழ்": [
        "16 லிட்டர் தெளிப்பானில் எவ்வளவு மருந்து கலக்க வேண்டும்?",
        "இயற்கை மற்றும் உயிரியல் முறைகள் என்ன?",
        "இன்றைய வானிலையில் மருந்து தெளிக்கலாமா?",
        "அடுத்த பருவத்தில் இந்த பூச்சியைக் கட்டுப்படுத்துவது எப்படி?",
        "இந்த மருந்து கால்நடைகளுக்கும் உணவுக்கும் பாதுகாப்பானதா?"
    ],
    "ಕನ್ನಡ": [
        "16 ಲೀಟರ್ ಪಂಪಿಗೆ ಎಷ್ಟು ಔಷಧ ಹಾಕಬೇಕು?",
        "ಸಾವಯವ ಮತ್ತು ಜೈವಿಕ ನಿಯಂತ್ರಣ ಕ್ರಮಗಳು ಯಾವುವು?",
        "ಇಂದಿನ ಹವಾಮಾನದಲ್ಲಿ ಸಿಂಪರಣೆ ಮಾಡಬಹುದೇ?",
        "ಮುಂದಿನ ಋತುವಿನಲ್ಲಿ ಈ ಕೀಟವನ್ನು ಹೇಗೆ ತಡೆಗಟ್ಟುವುದು?",
        "ಈ ಕೀಟನಾಶಕವು ಜಾನುವಾರುಗಳಿಗೆ ಮತ್ತು ಆಹಾರಕ್ಕೆ ಸುರಕ್ಷಿತವೇ?"
    ],
    "ਪੰਜਾਬੀ": [
        "16 ਲੀਟਰ ਦੇ ਪੰਪ ਵਿੱਚ ਕਿੰਨੀ ਦਵਾਈ ਪਾਈਏ?",
        "ਜੈਵਿਕ ਅਤੇ ਕੁਦਰਤੀ ਰੋਕਥਾਮ ਦੇ ਤਰੀਕੇ ਕੀ ਹਨ?",
        "ਕੀ ਅੱਜ ਦੇ ਮੌਸਮ ਵਿੱਚ ਸਪਰੇਅ ਕਰਨੀ ਠੀਕ ਰਹੇਗੀ?",
        "ਅਗਲੇ ਸੀਜ਼ਨ ਵਿੱਚ ਇਸ ਕੀੜੇ ਤੋਂ ਕਿਵੇਂ ਬਚੀਏ?",
        "ਕੀ ਇਹ ਕੀਟਨਾਸ਼ਕ ਪਸ਼ੂਆਂ ਅਤੇ ਖਾਣ ਲਈ ਸੁਰੱਖਿਅਤ ਹੈ?"
    ],
    "ગુજરાતી": [
        "૧૬ લિટર પંપમાં કેટલી દવા નાખવી?",
        "કુદરતી અને જૈવિક ઉપાયો કયા છે?",
        "આજના હવામાનમાં દવાનો છંટકાવ કરી શકાય?",
        "આવતી સિઝનમાં આ જીવાતથી કેવી રીતે બચવું?",
        "શું આ રસાયણ પશુઓ અને ખોરાક માટે સલામત છે?"
    ]
}

def extract_tank_capacity(query: str) -> Optional[float]:
    """
    Extracts custom sprayer tank capacity in Liters from user prompt if mentioned.
    e.g. '16 liter', '20L', '15 ltr', '100 litre', '200 L barrel'
    """
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:l|liter|liters|litre|litres|लिटर|लीटर|లీటర్|லிட்டர்|ಲೀಟರ್|ਲਿਟਰ|લિટર)", query, re.IGNORECASE)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            pass
    return None

def generate_chat_response(
    query: str,
    language: str,
    diagnosis_context: Optional[Dict[str, Any]] = None,
    weather_context: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generates a context-aware agronomist response in the selected language.
    """
    lang = language if language in LANG_MAP else "English"
    q_lower = query.lower()
    
    # 1. Check if an image diagnosis is currently active
    has_diag = diagnosis_context is not None and diagnosis_context.get("status") in ["CONFIRMED", "EARLY_INCUBATION"]
    disease = diagnosis_context.get("disease_label", "Crop") if has_diag else None
    disease_clean = disease.replace("_", " ").title() if disease else "Crop"
    leaf_stage = diagnosis_context.get("leaf_stage", {}) if has_diag else {}
    pest_stage = diagnosis_context.get("pest_stage", {}) if has_diag else {}
    chems = diagnosis_context.get("chemical_options", []) if has_diag else []
    bios = diagnosis_context.get("bio_options", []) if has_diag else []
    preventives = diagnosis_context.get("preventive_measures", []) if has_diag else []
    
    # Check for custom tank capacity request
    tank_liters = extract_tank_capacity(query)
    
    # 2. Check question categories: Dosage / Tank Calculation
    is_dosage_q = any(w in q_lower for w in ["dose", "dosage", "amount", "pump", "tank", "liter", "litre", "ml", "gram", "kitna", "kiti", "praman", "मात्रा", "प्रमाण", "औषध", "दवा", "మోతాదు", "அளவு", "ಪ್ರಮಾಣ", "ਮਾਤਰਾ", "માપ"])
    
    if is_dosage_q and has_diag and chems:
        vol = tank_liters if tank_liters else 16.0
        chem_name = chems[0].get("name", "Recommended Formulation")
        dose_lit = chems[0].get("dose_per_liter", "2.0 ml / L")
        dose_15 = chems[0].get("dose_per_15l_pump", "30 ml / 15L")
        dose_acre = chems[0].get("dose_per_acre", "400 ml in 200L / acre")
        phi = chems[0].get("phi_days", 14)
        
        # Calculate scaled dosage for tank
        # Try to extract base rate per liter
        num_match = re.search(r"(\d+(?:\.\d+)?)", dose_lit)
        base_rate = float(num_match.group(1)) if num_match else 2.0
        calculated_dose = round(base_rate * vol, 1)
        unit = "ml" if "ml" in dose_lit.lower() else "grams"
        
        if lang == "मराठी":
            return f"""### 🧪 **{vol} लिटर पंपासाठी अचूक औषध प्रमाण ({disease_clean})**
- **शिफारस केलेले औषध:** `{chem_name}`
- **प्रति लिटर प्रमाण:** `{dose_lit}`
- **तुमच्या {vol} लिटर पंपासाठी:** **`{calculated_dose} {unit}`** औषध टाकावे.
- **१ एकर क्षेत्रासाठी प्रमाण:** `{dose_acre}`
- **प्रतीक्षा कालावधी (PHI):** `{phi} दिवस` (फवारणीनंतर काढणीपूर्वी पाळायचा कालावधी)

💡 **फवारणीची महत्त्वाची टीप:**
औषध थेट पंपात टाकण्यापूर्वी एका बादलीत २ लिटर पाण्यात चांगले ढवळून द्रावण तयार करा, नंतर ते पंपातील पाण्यात मिसळा. फवारणी सकाळी १० पूर्वी किंवा दुपारी ४ नंतर करावी."""
        elif lang == "हिंदी":
            return f"""### 🧪 **{vol} लीटर पंप के लिए सही दवा की मात्रा ({disease_clean})**
- **अनुशंसित दवा:** `{chem_name}`
- **प्रति लीटर मात्रा:** `{dose_lit}`
- **आपके {vol} लीटर पंप के लिए:** **`{calculated_dose} {unit}`** दवा मिलाएं।
- **१ एकड़ क्षेत्र के लिए:** `{dose_acre}`
- **प्रतीक्षा अवधि (PHI):** `{phi} दिन` (छिड़काव के बाद फसल तुड़ाई से पहले)

💡 **विशेष सलाह:**
दवा को सीधे टंकी में न डालें; पहले बाल्टी में थोड़े पानी में घोल बनाकर फिर टंकी में पूरा पानी भरें। हवा तेज होने पर छिड़काव न करें।"""
        elif lang == "తెలుగు":
            return f"""### 🧪 **{vol} లీటర్ల పంపు కోసం ఖచ్చితమైన మందు మోతాదు ({disease_clean})**
- **సిఫార్సు చేసిన మందు:** `{chem_name}`
- **లీటరు నీటికి:** `{dose_lit}`
- **మీ {vol} లీటర్ల ట్యాంకుకు:** **`{calculated_dose} {unit}`** కలపండి.
- **ఎకరానికి మొత్తం మోతాదు:** `{dose_acre}`
- **వేచి ఉండే వ్యవధి (PHI):** `{phi} రోజులు`

💡 **ముఖ్య సూచన:**
మందును ముందుగా చిన్న బకెట్‌లో బాగా కలిపి, ఆపై స్ప్రేయర్ ట్యాంకులో పోయండి."""
        elif lang == "தமிழ்":
            return f"""### 🧪 **{vol} லிட்டர் தெளிப்பானுக்கான துல்லியமான மருந்து அளவு ({disease_clean})**
- **பரிந்துரைக்கப்பட்ட மருந்து:** `{chem_name}`
- **ஒரு லிட்டர் நீருக்கு:** `{dose_lit}`
- **உங்கள் {vol} லிட்டர் டேங்கிற்கு:** **`{calculated_dose} {unit}`** கலக்கவும்.
- **ஒரு ஏக்கருக்கு:** `{dose_acre}`
- **பறிப்புக்கு முந்தைய இடைவெளி (PHI):** `{phi} நாட்கள்`

💡 **பாதுகாப்பு குறிப்பு:**
காலையில் வெயில் ஏறுவதற்கு முன் அல்லது மாலையில் தெளிக்கவும்."""
        elif lang == "ಕನ್ನಡ":
            return f"""### 🧪 **{vol} ಲೀಟರ್ ಪಂಪ್‌ಗಾಗಿ ನಿಖರವಾದ ಔಷಧ ಪ್ರಮಾಣ ({disease_clean})**
- **ಶಿಫಾರಸು ಮಾಡಿದ ಔಷಧ:** `{chem_name}`
- **ಪ್ರತಿ ಲೀಟರ್ ನೀರಿಗೆ:** `{dose_lit}`
- **ನಿಮ್ಮ {vol} ಲೀಟರ್ ಪಂಪ್‌ಗೆ:** **`{calculated_dose} {unit}`** ಬೆರೆಸಿ.
- **ಒಂದು ಎಕರೆಗೆ ಒಟ್ಟು ಪ್ರಮಾಣ:** `{dose_acre}`
- **ಕಟಾವಿಗೆ ಕಾಯುವ ಅವಧಿ (PHI):** `{phi} ದಿನಗಳು`

💡 **ಸಿಂಪರಣೆ ಸಲಹೆ:**
ಔಷಧವನ್ನು ಮೊದಲು ಸ್ವಲ್ಪ ನೀರಿನಲ್ಲಿ ಕರಗಿಸಿ ನಂತರ ಪೂರ್ಣ ಟ್ಯಾಂಕ್‌ಗೆ ಸುರಿಯಿರಿ."""
        elif lang == "ਪੰਜਾਬੀ":
            return f"""### 🧪 **{vol} ਲੀਟਰ ਪੰਪ ਲਈ ਸਹੀ ਦਵਾਈ ਦੀ ਮਾਤਰਾ ({disease_clean})**
- **ਸਿਫਾਰਸ਼ ਕੀਤੀ ਦਵਾਈ:** `{chem_name}`
- **ਪ੍ਰਤੀ ਲੀਟਰ ਪਾਣੀ:** `{dose_lit}`
- **ਤੁਹਾਡੇ {vol} ਲੀਟਰ ਪੰਪ ਲਈ:** **`{calculated_dose} {unit}`** ਦਵਾਈ ਪਾਓ।
- **ਇੱਕ ਏਕੜ ਲਈ:** `{dose_acre}`
- **ਤੁੜਾਈ ਤੋਂ ਪਹਿਲਾਂ ਇੰਤਜ਼ਾਰ (PHI):** `{phi} ਦਿਨ`

💡 **ਸਾਵਧਾਨੀ:**
ਤੇਜ਼ ਧੁੱਪ ਜਾਂ ਹਵਾ ਚੱਲਣ ਵੇਲੇ ਸਪਰੇਅ ਨਾ ਕਰੋ।"""
        elif lang == "ગુજરાતી":
            return f"""### 🧪 **{vol} લિટર પંપ માટે દવાનું ચોક્કસ પ્રમાણ ({disease_clean})**
- **ભલામણ કરેલ દવા:** `{chem_name}`
- **પ્રતિ લિટર પાણી દીઠ:** `{dose_lit}`
- **તમારા {vol} લિટર પંપ માટે:** **`{calculated_dose} {unit}`** દવા ભેળવવી.
- **૧ એકર માટે:** `{dose_acre}`
- **પ્રતીક્ષા સમયગાળો (PHI):** `{phi} દિવસ`

💡 **મહત્વપૂર્ણ સલાહ:**
સવારે વહેલા અથવા સાંજે ઠંડા વાતાવરણમાં છંટકાવ કરવો."""
        elif lang == "বাংলা":
            return f"""### 🧪 **{vol} লিটার পাম্পের জন্য ওষুধের সঠিক মাত্রা ({disease_clean})**
- **প্রস্তাবিত ওষুধ:** `{chem_name}`
- **প্রতি লিটার পানিতে:** `{dose_lit}`
- **আপনার {vol} লিটার স্প্রেয়ার ট্যাঙ্কের জন্য:** **`{calculated_dose} {unit}`** ওষুধ মেশান।
- **প্রতি একরের জন্য মোট প্রয়োগ:** `{dose_acre}`
- **তোলার পূর্বে অপেক্ষার সময় (PHI):** `{phi} দিন`

💡 **স্প্রে করার সতর্কতা:**
প্রথমে একটি প্লাস্টিকের বালতিতে ২ লিটার পানিতে ওষুধটি ভালো করে গুলে নিন, তারপর স্প্রেয়ার ট্যাঙ্কের চালুনির মধ্য দিয়ে ঢালুন। সকালের ঠান্ডা আবহাওয়ায় (সকাল ৭:০০-১০:০০) বা বিকেলে (৪:০০-৬:৩০) স্প্রে করুন।"""
        else:
            return f"""### 🧪 **Exact Pesticide Dosage for {vol}-Liter Sprayer Pump ({disease_clean})**
- **Recommended Formulation:** `{chem_name}`
- **Dilution Rate per Liter:** `{dose_lit}`
- **Dosage for your {vol}L Sprayer Tank:** **`{calculated_dose} {unit}`**
- **Total Field Application per Acre:** `{dose_acre}`
- **Pre-Harvest Interval (PHI):** `{phi} days` mandatory waiting period before harvest

💡 **Spraying Best Practice:**
Pre-mix the measured chemical in 2 Liters of clean water in a plastic bucket before pouring it through the sprayer strainer. Spray during calm morning (7:00–10:00 AM) or late afternoon (4:00–6:30 PM)."""

    # 3. Check question categories: Organic / Biological Remedies
    is_bio_q = any(w in q_lower for w in ["organic", "bio", "natural", "neem", "jeevamrut", "trichoderma", "सेंद्रिय", "जैविक", "कडुलिंब", "नीम", "जीवामृत", "జీవ", "సేంద్రీయ", "இயற்கை", "சாவಯವ", "ਜੈਵਿਕ", "જૈવિક", "દેશી"])
    if is_bio_q:
        bio_desc = ""
        if bios:
            for b in bios:
                bio_desc += f"- **{b.get('name')}:** `{b.get('dose_per_liter', '2-3 ml/L')}` ({b.get('dose_per_acre', '500 ml/acre')}) — *{b.get('instructions', 'Natural biopesticide')}*\n"
        else:
            bio_desc = "- **Neem Oil (10,000 ppm):** 2.5 ml / Liter water (Repels pests and stops egg hatching)\n- **Pseudomonas / Trichoderma:** 5 g / Liter water (Controls bacterial & fungal blight)\n- **Cow Urine Broth (Jeevamrut):** 50 ml / Liter water (Improves foliar resistance)"

        if lang == "मराठी":
            return f"""### 🌿 **प्रमाणित सेंद्रिय व जैविक उपाय ({disease_clean})**
{bio_desc}
🥣 **घरगुती कडुनिंब अर्क (NSKE 5%) तयार करण्याची पद्धत:**
1. ५ किलो सुक्या कडुनिंबाच्या बियांची पावडर करा.
2. ही पावडर एका सुती कापडात बांधून १० लिटर पाण्यात रात्रभर भिजत ठेवा.
3. सकाळी कापड पिळून अर्क गाळून घ्या व त्यात २०० लिटर पाणी आणि २०० ग्रॅम साबणाचा चुरा मिसळून १ एकरावर फवारा."""
        elif lang == "हिंदी":
            return f"""### 🌿 **प्रमाणित जैविक एवं प्राकृतिक उपचार ({disease_clean})**
{bio_desc}
🥣 **घर पर ५% नीम बीज अर्क (NSKE) तैयार करने की विधि:**
1. ५ किलो सूखे नीम के बीजों की गिरी कूट लें।
2. इसे सूती कपड़े की पोटली में बांधकर रात भर १० लीटर पानी में भिगो दें।
3. सुबह पोटली को निचोड़ लें और इस अर्क को २०० लीटर पानी में घोलकर प्रति एकड़ छिड़कें।"""
        elif lang == "తెలుగు":
            return f"""### 🌿 **సేంద్రీయ మరియు జీవ రక్షణ పద్ధతులు ({disease_clean})**
{bio_desc}
🥣 **వేప కషాయం (NSKE 5%) తయారీ విధానం:**
5 కిలోల వేప గింజల పొడిని 10 లీటర్ల నీటిలో రాత్రంతా నానబెట్టి, ఉదయం వడకట్టి 200 లీటర్ల నీటిలో కలిపి ఎకరానికి పిచికారీ చేయండి."""
        elif lang == "தமிழ்":
            return f"""### 🌿 **இயற்கை மற்றும் உயிரியல் தீர்வுகள் ({disease_clean})**
{bio_desc}
🥣 **வேப்பங்கொட்டை கரைசல் (NSKE 5%) தயாரிக்கும் முறை:**
5 கிலோ வேப்பங்கொட்டை பொடியை 10 லிட்டர் நீரில் இரவு முழுவதும் ஊறவைத்து, வடிகட்டி 200 லிட்டர் நீரில் கலந்து தெளிக்கவும்."""
        elif lang == "ಕನ್ನಡ":
            return f"""### 🌿 **ಪ್ರಾಕೃತಿಕ ಮತ್ತು ಜೈವಿಕ ಪರಿಹಾರಗಳು ({disease_clean})**
{bio_desc}
🥣 **ಬೇವಿನ ಬೀಜದ ಕಷಾಯ (NSKE 5%) ತಯಾರಿಸುವ ವಿಧಾನ:**
5 ಕೆಜಿ ಬೇವಿನ ಬೀಜದ ಪುಡಿಯನ್ನು ರಾತ್ರಿಯಿಡೀ 10 ಲೀಟರ್ ನೀರಿನಲ್ಲಿ ನೆನೆಸಿ, ಬೆಳಿಗ್ಗೆ ಸೋಸಿ 200 ಲೀಟರ್ ನೀರಿನಲ್ಲಿ ಬೆರೆಸಿ ಸಿಂಪಡಿಸಿ."""
        elif lang == "ਪੰਜਾਬੀ":
            return f"""### 🌿 **ਜੈਵਿਕ ਅਤੇ ਕੁਦਰਤੀ ਉਪਚਾਰ ({disease_clean})**
{bio_desc}
🥣 **ਨੀਮ ਦਾ ਅਰਕ (NSKE 5%) ਤਿਆਰ ਕਰਨ ਦਾ ਤਰੀਕਾ:**
5 ਕਿਲੋ ਨੀਮ ਦੀ ਨਿਮੋਲੀ ਪੀਸ ਕੇ 10 ਲੀਟਰ ਪਾਣੀ ਵਿੱਚ ਰਾਤ ਭਰ ਭਿਓਂ ਦਿਓ, ਸਵੇਰੇ ਛਾਣ ਕੇ 200 ਲੀਟਰ ਪਾਣੀ ਵਿੱਚ ਮਿਲਾ ਕੇ ਸਪਰੇਅ ਕਰੋ।"""
        elif lang == "ગુજરાતી":
            return f"""### 🌿 **પ્રમાણિત જૈવિક અને કુદરતી ઉપાયો ({disease_clean})**
{bio_desc}
🥣 **લીંબોળીનો અર્ક (NSKE 5%) બનાવવાની રીત:**
૫ કિલો લીંબોળીનો પાઉડર ૧૦ લિટર પાણીમાં આખી રાત પલાળી, સવારે ગાળીને ૨૦૦ લિટર પાણીમાં ભેળવી છંટકાવ કરવો."""
        elif lang == "বাংলা":
            return f"""### 🌿 **অনুমোদিত জৈব ও প্রাকৃতিক প্রতিকার ({disease_clean})**
{bio_desc}
🥣 **খামারে ৫% নিম বীজ নির্যাস (NSKE) তৈরির পদ্ধতি:**
১. ৫ কেজি শুকনো নিম বীজ গুঁড়ো করে নিন।
২. একটি সুতি কাপড়ের পুটলিতে বেঁধে সারা রাত ১০ লিটার পানিতে ভিজিয়ে রাখুন।
৩. সকালে পুটলিটি ভালো করে নিংড়ে রস বের করুন, ২০০ গ্রাম সাবানের গুঁড়ো মেশান এবং প্রতি একরের জন্য ২০০ লিটার পানিতে মিশিয়ে স্প্রে করুন।"""
        else:
            return f"""### 🌿 **Certified Bio-Organic IPM Alternatives ({disease_clean})**
{bio_desc}
🥣 **How to Prepare 5% Neem Seed Kernel Extract (NSKE) on the Farm:**
1. Pound 5 kg of dried neem seeds into a coarse powder.
2. Tie the powder inside a cotton bag and soak it overnight in 10 Liters of water.
3. Squeeze the bag thoroughly next morning, add 200 g of dissolved neutral soap (as a sticking agent), and dilute with 200 Liters of clean water per acre."""

    # 4. Check question categories: Weather / Spraying suitability
    is_weather_q = any(w in q_lower for w in ["weather", "rain", "wind", "cloud", "spray today", "আবহাওয়া", "বৃষ্টি", "মেঘ", "हवामान", "पाऊस", "वार", "फवारणी", "मौसम", "बारिश", "हवा", "వాతావరణం", "వర్షం", "வானிலை", "மழை", "ಹವಾಮಾನ", "ಮಳೆ", "ਮੌਸਮ", "ਮੀਂਹ", "વરસાદ"])
    if is_weather_q:
        temp = weather_context.get("temperature", 30.0) if weather_context else 30.0
        hum = weather_context.get("humidity", 70) if weather_context else 70
        is_safe_to_spray = (hum < 85 and temp < 36.0)
        
        if lang == "मराठी":
            status_text = "✅ **फवारणीसाठी हवामान अनुकूल आहे.**" if is_safe_to_spray else "⚠️ **सध्या फवारणी करणे टाळा.**"
            return f"""### 🌤️ **हवामान व फवारणी सल्ला**
- **तापमान:** `{temp} °C` | **हवेतील आर्द्रता:** `{hum} %`
- **सद्यस्थिती:** {status_text}

📌 **नियम:**
1. आर्द्रता ८५% पेक्षा जास्त असल्यास किंवा पुढील ४ तासांत पाऊस पडण्याची शक्यता असल्यास फवारणी टाळा.
2. पाने कोरडी झाल्यावरच फवारणी करा, जेणेकरून दवबिंदूंमुळे औषध वाहून जाणार नाही."""
        elif lang == "हिंदी":
            status_text = "✅ **छिड़काव के लिए मौसम उपयुक्त है।**" if is_safe_to_spray else "⚠️ **फिलहाल छिड़काव करने से बचें।**"
            return f"""### 🌤️ **मौसम एवं छिड़काव उपयुक्तता**
- **तापमान:** `{temp} °C` | **आर्द्रता:** `{hum} %`
- **निष्कर्ष:** {status_text}

📌 **महत्वपूर्ण दिशानिर्देश:**
1. तेज धूप (दोपहर १२ से ३ बजे) में छिड़काव न करें।
2. बारिश की संभावना होने पर स्टिकर/स्प्रेडर का उपयोग जरूर करें।"""
        elif lang == "বাংলা":
            status_text = "✅ **স্প্রে করার জন্য বর্তমান আবহাওয়া অনুকূল।**" if is_safe_to_spray else "⚠️ **বৃষ্টি বা অতিরিক্ত আর্দ্রতার কারণে এখন স্প্রে করা এড়িয়ে চলুন।**"
            return f"""### 🌤️ **আবহাওয়া ও স্প্রে পরামর্শ**
- **তাপমাত্রা:** `{temp} °C` | **বাতাসে আর্দ্রতা:** `{hum} %`
- **পরিস্থিতি:** {status_text}

📌 **গুরুত্বপূর্ণ নির্দেশনা:**
১. সকালের ঠান্ডা আবহাওয়া বা বিকেলে স্প্রে করুন; প্রখর রোদে স্প্রে করবেন না।
২. বৃষ্টির সম্ভাবনা থাকলে স্টিকার/স্প্রেডার মিশিয়ে স্প্রে করুন যাতে ধুয়ে না যায়।"""
        elif lang == "తెలుగు":
            status_text = "✅ **మందు పిచికారీ చేయడానికి వాతావరణం అనుకూలంగా ఉంది.**" if is_safe_to_spray else "⚠️ **ప్రస్తుతం పిచికారీ చేయడం ఆపండి.**"
            return f"""### 🌤️ **వాతావరణం మరియు స్ప్రేయింగ్ సలహా**
- **ఉష్ణోగ్రత:** `{temp} °C` | **తేమ:** `{hum} %`
- **నిర్ణయం:** {status_text}"""
        elif lang == "தமிழ்":
            status_text = "✅ **மருந்து தெளிக்க வானிலை சாதகமாக உள்ளது.**" if is_safe_to_spray else "⚠️ **இப்போது தெளிப்பதை தவிர்க்கவும்.**"
            return f"""### 🌤️ **வானிலை மற்றும் தெளிப்பு வழிகாட்டுதல்**
- **வெப்பநிலை:** `{temp} °C` | **ஈரப்பதம்:** `{hum} %`
- **நிலை:** {status_text}"""
        elif lang == "ಕನ್ನಡ":
            status_text = "✅ **ಸಿಂಪರಣೆ ಮಾಡಲು ಹವಾಮಾನ ಸೂಕ್ತವಾಗಿದೆ.**" if is_safe_to_spray else "⚠️ **ಪ್ರಸ್ತುತ ಸಿಂಪರಣೆ ಮಾಡಬೇಡಿ.**"
            return f"""### 🌤️ **ಹವಾಮಾನ ಮತ್ತು ಸಿಂಪರಣೆ ಮಾಹಿತಿ**
- **ತಾಪಮಾನ:** `{temp} °C` | **ತೇವಾಂಶ:** `{hum} %`
- **ಸ್ಥಿತಿ:** {status_text}"""
        elif lang == "ਪੰਜਾਬੀ":
            status_text = "✅ **ਸਪਰੇਅ ਕਰਨ ਲਈ ਮੌਸਮ ਅਨੁਕੂਲ ਹੈ।**" if is_safe_to_spray else "⚠️ **ਫਿਲਹਾਲ ਸਪਰੇਅ ਕਰਨ ਤੋਂ ਬਚੋ।**"
            return f"""### 🌤️ **ਮੌਸਮ ਅਤੇ ਸਪਰੇਅ ਸਲਾਹ**
- **ਤਾਪਮਾਨ:** `{temp} °C` | **ਨਮੀ:** `{hum} %`
- **ਸਥਿਤੀ:** {status_text}"""
        elif lang == "ગુજરાતી":
            status_text = "✅ **છંટકાવ માટે હવામાન અનુકૂળ છે.**" if is_safe_to_spray else "⚠️ **હાલમાં છંટકાવ કરવો ટાળો.**"
            return f"""### 🌤️ **હવામાન અને છંટકાવ સલાહ**
- **તાપમાન:** `{temp} °C` | **ભેજ:** `{hum} %`
- **નિષ્કર્ષ:** {status_text}"""
        else:
            status_text = "✅ **Weather is currently favorable for spraying.**" if is_safe_to_spray else "⚠️ **Advisable to delay spraying due to high humidity/rain risk.**"
            return f"""### 🌤️ **Field Microclimate & Spraying Suitability**
- **Ambient Temperature:** `{temp} °C`
- **Relative Humidity:** `{hum} %`
- **Spray Decision:** {status_text}

📌 **Key Rules for Maximum Chemical Efficiency:**
1. Do not spray during the heat of the day (11:00 AM – 3:00 PM) as droplets rapidly evaporate and cause leaf scorch.
2. Ensure at least a 4-hour rain-free window after application or mix an organosilicone surfactant/spreader sticker."""

    # 5. Check question categories: Preventive Measures / Next season
    is_prev_q = any(w in q_lower for w in ["prevent", "रोकथाम", "प्रतिबंधक", "उपाय", "તકેદારી", "ਰੋਕਥਾਮ", "నివారణ", "தடுப்பு", "ತಡೆಗಟ್ಟುವಿಕೆ"])
    if is_prev_q:
        p_list = ""
        if preventives:
            for p in preventives:
                p_list += f"- {p}\n"
        else:
            p_list = "- Deep summer plowing to expose pupae to birds and sunlight.\n- Seed delinting and treatment with bio-fungicide.\n- Pheromone & yellow sticky traps @ 8 traps/acre."

        if lang == "मराठी":
            return f"""### 🛡️ **पुढील हंगामासाठी प्रतिबंधात्मक उपाय ({disease_clean})**
{p_list}
🚜 **दीर्घकालीन शिफारशी:**
- पीक फेरपालट (Crop Rotation) करा; सलग एकाच पिकाची लागवड टाळा.
- बांधावरील तण (गाजरगवत, पेटारी) वेळोवेळी काढून नष्ट करा."""
        elif lang == "हिंदी":
            return f"""### 🛡️ **अगले मौसम के लिए रोकथाम के उपाय ({disease_clean})**
{p_list}
🚜 **दीर्घकालिक सुझाव:**
- ग्रीष्मकालीन गहरी जुताई करें ताकि मिट्टी में मौजूद कीटों के प्यूपा नष्ट हो जाएं।
- फसल चक्र अपनाएं और प्रमाणित प्रतिरोधी बीजों का ही चयन करें।"""
        elif lang == "తెలుగు":
            return f"""### 🛡️ **నివారణ చర్యలు ({disease_clean})**
{p_list}
- వేసవిలో లోతు దుక్కులు చేయండి.
- నాణ్యమైన మరియు తెగులు నిరోధక విత్తనాలను ఎంచుకోండి."""
        elif lang == "தமிழ்":
            return f"""### 🛡️ **தடுப்பு நடவடிக்கைகள் ({disease_clean})**
{p_list}
- கோடையில் ஆழமாக உழவு செய்யவும்.
- சான்றளிக்கப்பட்ட எதிர்ப்பு திறன் கொண்ட ரகங்களை நடவு செய்யவும்."""
        elif lang == "ಕನ್ನಡ":
            return f"""### 🛡️ **ಮುನ್ನೆಚ್ಚರಿಕೆ ಕ್ರಮಗಳು ({disease_clean})**
{p_list}
- ಬೇಸಿಗೆಯಲ್ಲಿ ಆಳವಾದ ಉಳುಮೆ ಮಾಡಿ.
- ರೋಗ ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಆಯ್ಕೆ ಮಾಡಿ."""
        elif lang == "ਪੰਜਾਬੀ":
            return f"""### 🛡️ **ਰੋਕਥਾਮ ਦੇ ਉਪਾਅ ({disease_clean})**
{p_list}
- ਗਰਮੀਆਂ ਵਿੱਚ ਡੂੰਘੀ ਵਾਹੀ ਕਰੋ ਤਾਂ ਜੋ ਕੀੜੇ ਖਤਮ ਹੋ ਜਾਣ।
- ਰੋਧਕ ਬੀਜਾਂ ਦੀ ਹੀ ਵਰਤੋਂ ਕਰੋ।"""
        elif lang == "ગુજરાતી":
            return f"""### 🛡️ **નિવારક પગલાં ({disease_clean})**
{p_list}
- ઉનાળામાં ઊંડી ખેડ કરવી જેથી જમીનમાં રહેલા પ્યુપા નાશ પામે.
- પાકની ફેરબદલી કરવી અને રોગપ્રતિકારક જાતો વાવવી."""
        elif lang == "বাংলা":
            return f"""### 🛡️ **পরবর্তী মরসুমের জন্য প্রতিরোধমূলক ব্যবস্থা ({disease_clean})**
{p_list}
🚜 **দীর্ঘমেয়াদী প্রাতিষ্ঠানিক সুপারিশ:**
- গ্রীষ্মকালে গভীর চাষ দিন যাতে মাটির গভীরে থাকা কীটের পিউপা ধ্বংস হয়।
- শস্য পর্যায়ক্রম (Crop Rotation) অনুসরণ করুন এবং অনুমোদিত রোগ প্রতিরোধী জাত ব্যবহার করুন।"""
        else:
            return f"""### 🛡️ **Proactive & Preventive IPM Protocol ({disease_clean})**
{p_list}
🚜 **Strategic Long-Term Recommendations:**
- Practice deep summer plowing to invert soil and expose pupating caterpillars to solar heat and predatory birds.
- Adopt crop rotation with non-host legumes or millets to break the pathogen's spore propagation cycle."""

    # 5b. Check question categories: Anomaly / Specimen Integrity
    is_anom_q = any(w in q_lower for w in ["anomaly", "valid", "ood", "specimen", "non-plant", "unknown", "विकृती", "अवैध", "विसंगति", "అనోమలీ", "முரண்பாடு", "ಅಸಹಜತೆ", "ਅਸਧਾਰਨਤਾ", "વિસંગતતા"])
    if is_anom_q:
        anom = diagnosis_context.get("anomaly", {}) if diagnosis_context else {}
        anom_score = anom.get("anomaly_score", 0.0)
        foliar_pct = anom.get("foliar_percentage", 100.0)
        badge = anom.get("badge_label", "🟢 Verified Crop Foliar Specimen")
        explanation = anom.get("explanation", "Specimen conforms to verified agricultural in-distribution patterns.")
        rec = anom.get("recommendation", "Standard IPM protocols apply.")

        if lang == "मराठी":
            return f"""### 🛡️ **नमुना वैधता आणि विकृती विश्लेषण (Anomaly Assessment)**
- **नमुना स्थिती:** {badge}
- **पानाच्या ऊतींची उपस्थिती:** `{foliar_pct}%`
- **विकृती जोखीम निर्देशांक:** `{anom_score}%`
- **तपशील:** {explanation}

💡 **कृषीरक्षक सल्ला:** {rec}"""
        elif lang == "हिंदी":
            return f"""### 🛡️ **नमूना वैधता एवं विसंगति विश्लेषण (Anomaly Assessment)**
- **नमूना स्थिति:** {badge}
- **पत्ती ऊतक प्रतिशत:** `{foliar_pct}%`
- **विसंगति जोखिम सूचकांक:** `{anom_score}%`
- **विवरण:** {explanation}

💡 **कृषिरक्षक सलाह:** {rec}"""
        elif lang == "বাংলা":
            return f"""### 🛡️ **নমুনা বৈধতা ও অসঙ্গতি বিশ্লেষণ (Anomaly Assessment)**
- **নমুনার স্থিতি:** {badge}
- **পাতার টিস্যুর উপস্থিতি:** `{foliar_pct}%`
- **অসঙ্গতি ঝুঁকি সূচক:** `{anom_score}%`
- **বিশ্লেষণ:** {explanation}

💡 **কৃষিরক্ষক পরামর্শ:** {rec}"""
        else:
            return f"""### 🛡️ **Specimen Validity & Anomaly Assessment**
- **Validation Status:** {badge}
- **Foliar Plant Tissue Detected:** `{foliar_pct}%`
- **Anomaly / OOD Risk Index:** `{anom_score}%`
- **Pathological Analysis:** {explanation}

💡 **Agronomic Advisory:** {rec}"""

    # 6. Default Context-Aware Diagnostic Summary & Advice
    if has_diag:
        stg_title = leaf_stage.get("title", "Stage 1")
        pst_title = pest_stage.get("stage_name", "Initial Stage")
        lesion_val = leaf_stage.get("lesion_percentage", 5.0)
        chem_name = chems[0].get("name", "Targeted Formulation") if chems else "Bio-Pesticide"
        chem_dose = chems[0].get("dose_per_15l_pump", "30 ml / 15L") if chems else "30 ml / 15L"

        if lang == "मराठी":
            return f"""### 🌱 **कृषीरक्षक AI तज्ज्ञ सल्ला ({disease_clean})**
- **पानावरील संसर्ग टप्पा:** `{stg_title}` (डागांचे प्रमाण: `{lesion_val}%`)
- **कीड / रोगाची अवस्था:** `{pst_title}`
- **तातडीचा उपाय:** `{chem_name}` — **`{chem_dose}`** प्रमाणात फवारणी करावी.
- **सेंद्रिय पर्याय:** कडुनिंब अर्क (NSKE 5%) किंवा निम ऑईल २.५ मिली/लिटर.

तुम्हाला पंपाचे अचूक प्रमाण, औषधांची सुरक्षितता किंवा हवामानाबद्दल काही विचारायचे असल्यास खाली टाईप करा."""
        elif lang == "हिंदी":
            return f"""### 🌱 **कृषिरक्षक AI विशेषज्ञ सलाह ({disease_clean})**
- **पत्ती पर संक्रमण अवस्था:** `{stg_title}` (घाव विस्तार: `{lesion_val}%`)
- **कीट / रोग का जैविक चरण:** `{pst_title}`
- **तत्काल उपचार:** `{chem_name}` — **`{chem_dose}`** की दर से छिड़कें।
- **जैविक विकल्प:** नीम का तेल १०,००० ppm २.५ मिली/लीटर या ट्राइकोडर्मा ५ ग्राम/लीटर।

पंप के अनुसार दवा की सटीक मात्रा या मौसम की जानकारी के लिए पूछें।"""
        elif lang == "తెలుగు":
            return f"""### 🌱 **కృషీరక్షక్ AI నిపుణుల సలహా ({disease_clean})**
- **ఆకుపై వ్యాధి దశ:** `{stg_title}` ({lesion_val}%)
- **కీటక జీవన దశ:** `{pst_title}`
- **సిఫార్సు:** `{chem_name}` — `{chem_dose}` పిచికారీ చేయండి."""
        elif lang == "தமிழ்":
            return f"""### 🌱 **கிருஷிரக்ஷக் AI நிபுணர் ஆலோசனை ({disease_clean})**
- **இலையின் பாதிப்பு நிலை:** `{stg_title}` ({lesion_val}%)
- **பூச்சியின் நிலை:** `{pst_title}`
- **பரிந்துரை:** `{chem_name}` — `{chem_dose}` தெளிக்கவும்."""
        elif lang == "ಕನ್ನಡ":
            return f"""### 🌱 **ಕೃಷಿರಕ್ಷಕ್ AI ತಜ್ಞರ ಸಲಹೆ ({disease_clean})**
- **ಎಲೆಯ ಸೋಂಕಿನ ಹಂತ:** `{stg_title}` ({lesion_val}%)
- **ಕೀಟದ ಜೀವಿತ ಹಂತ:** `{pst_title}`
- **ಔಷಧ:** `{chem_name}` — `{chem_dose}` ಸಿಂಪಡಿಸಿ."""
        elif lang == "ਪੰਜਾਬੀ":
            return f"""### 🌱 **ਕ੍ਰਿਸ਼ੀਰਕਸ਼ਕ AI ਮਾਹਰ ਸਲਾਹ ({disease_clean})**
- **ਪੱਤੇ ਦਾ ਪੜਾਅ:** `{stg_title}` ({lesion_val}%)
- **ਕੀੜੇ ਦਾ ਪੜਾਅ:** `{pst_title}`
- **ਸਿਫਾਰਸ਼:** `{chem_name}` — `{chem_dose}` ਸਪਰੇਅ ਕਰੋ।"""
        elif lang == "ગુજરાતી":
            return f"""### 🌱 **કૃષિરક્ષક AI સલાહ ({disease_clean})**
- **પાન પર ચેપનો તબક્કો:** `{stg_title}` ({lesion_val}%)
- **જીવાતનો તબક્કો:** `{pst_title}`
- **ઉપાય:** `{chem_name}` — `{chem_dose}` છંટકાવ કરવો."""
        elif lang == "বাংলা":
            return f"""### 🌱 **কৃষিরক্ষক AI বিশেষজ্ঞ পরামর্শ ({disease_clean})**
- **পাতায় ক্ষতির পর্যায়:** `{stg_title}` (আক্রান্ত এলাকা: `{lesion_val}%`)
- **কীট বা রোগের জৈবিক পর্যায়:** `{pst_title}`
- **তাৎক্ষণিক ব্যবস্থা:** `{chem_name}` — **`{chem_dose}`** হারে স্প্রে করুন।
- **জৈব বিকল্প:** নিম তেল ১০,০০০ ppm ২.৫ মিলি/লিটার বা ট্রাইকোডার্মা ৫ গ্রাম/লিটার।

পাম্পের ধারণক্ষমতা অনুযায়ী সঠিক মাত্রা বা আবহাওয়া সম্পর্কে যেকোনো প্রশ্ন নিচে লিখুন।"""
        else:
            return f"""### 🌱 **KrishiRakshak Agronomist Advice ({disease_clean})**
- **Leaf Damage Stage:** `{stg_title}` (Active Lesion Surface: `{lesion_val}%`)
- **Pest Biological Phase:** `{pst_title}`
- **Primary Targeted Spray:** `{chem_name}` @ `{chem_dose}`
- **Certified Organic Remedy:** Neem Oil 10,000 ppm @ 2.5 ml/L or NSKE 5%

Feel free to ask me for exact pump dosage calculations, organic formulations, or weather precautions!"""

    # General Greeting
    if lang == "मराठी":
        return "नमस्कार शेतकरी बंधूंनो! मी कृषीरक्षक AI सहाय्यक आहे. आपण आपल्या पिकावरील कीड, रोगाचे टप्पे, फवारणीचे प्रमाण किंवा सेंद्रिय उपायांबद्दल कोणताही प्रश्न विचारू शकता."
    elif lang == "हिंदी":
        return "नमस्ते किसान भाई! मैं कृषिरक्षक AI सहायक हूँ। आप अपनी फसल के रोग, कीट के चरण, कीटनाशक की मात्रा या जैविक उपायों के बारे में कोई भी प्रश्न पूछ सकते हैं।"
    elif lang == "বাংলা":
        return "নমস্কার কৃষক ভাই ও বোনেরা! আমি কৃষিরক্ষক AI সহকারী। আপনি আপনার ফসলের রোগবালাই, পোকার আক্রমণ পর্যায়, কীটনাশকের সঠিক মাত্রা বা জৈব প্রতিকার সম্পর্কে যেকোনো প্রশ্ন জিজ্ঞাসা করতে পারেন।"
    elif lang == "తెలుగు":
        return "నమస్కారం రైతు సోదరులారా! నేను కృషీరక్షక్ AI సహాయకుడిని. మీరు పంట తెగుళ్లు, మందుల మోతాదు లేదా సేంద్రీయ పద్ధతుల గురించి నన్ను అడగవచ్చు."
    elif lang == "தமிழ்":
        return "வணக்கம் விவசாய நண்பரே! நான் கிருஷிரக்ஷக் AI உதவியாளர். பயிர் நோய்கள், பூச்சி நிலைகள், மருந்து அளவுகள் அல்லது இயற்கை முறைகள் பற்றி நீங்கள் கேட்கலாம்."
    elif lang == "ಕನ್ನಡ":
        return "ನಮಸ್ಕಾರ ರೈತ ಬಾಂಧವರೇ! ನಾನು ಕೃಷಿರಕ್ಷಕ್ AI ಸಹಾಯಕ. ಬೆಳೆ ರೋಗಗಳು, ಕೀಟನಾಶಕ ಪ್ರಮಾಣ ಅಥವಾ ಸಾವಯವ ಪರಿಹಾರಗಳ ಬಗ್ಗೆ ನೀವು ಯಾವುದೇ ಪ್ರಶ್ನೆ ಕೇಳಬಹುದು."
    elif lang == "ਪੰਜਾਬੀ":
        return "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਕਿਸਾਨ ਵੀਰੋ! ਮੈਂ ਕ੍ਰਿਸ਼ੀਰਕਸ਼ਕ AI ਸਹਾਇਕ ਹਾਂ। ਤੁਸੀਂ ਫਸਲਾਂ ਦੇ ਰੋਗ, ਕੀਟਨਾਸ਼ਕ ਦੀ ਮਾਤਰਾ ਜਾਂ ਜੈਵਿਕ ਉਪਚਾਰਾਂ ਬਾਰੇ ਪੁੱਛ ਸਕਦੇ ਹੋ।"
    elif lang == "ગુજરાતી":
        return "નમસ્તે ખેડૂત મિત્રો! હું કૃષિરક્ષક AI સહાયક છું. તમે પાકના રોગ, જંતુનાશકના માપ અથવા જૈવિક ઉપાયો વિશે કોઈ પણ પ્રશ્ન પૂછી શકો છો."
    else:
        return "Hello Farmer! I am KrishiRakshak AI Agronomist. Upload any infected leaf image to get stage diagnosis, precise pesticide calculations, and preventive organic measures."
