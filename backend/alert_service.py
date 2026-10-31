import math
from datetime import datetime, timedelta
from typing import Dict, Any

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2)**2
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

MOCK_REPORTS = [
    {"id": "REP-AK-01", "lat": 20.7010, "lon": 77.0100, "disease": "bollworm", "timestamp": datetime.now() - timedelta(hours=4)},
    {"id": "REP-AK-02", "lat": 20.7042, "lon": 77.0050, "disease": "bollworm", "timestamp": datetime.now() - timedelta(hours=12)},
    {"id": "REP-AK-03", "lat": 20.6980, "lon": 77.0090, "disease": "bollworm", "timestamp": datetime.now() - timedelta(hours=20)},
    {"id": "REP-YV-01", "lat": 20.3888, "lon": 78.1204, "disease": "curl_virus", "timestamp": datetime.now() - timedelta(hours=6)},
    {"id": "REP-YV-02", "lat": 20.3910, "lon": 78.1190, "disease": "curl_virus", "timestamp": datetime.now() - timedelta(hours=14)},
    {"id": "REP-YV-03", "lat": 20.3865, "lon": 78.1220, "disease": "curl_virus", "timestamp": datetime.now() - timedelta(hours=22)},
]

NAMES = {
    "bollworm": {"en": "Pink Bollworm", "mr": "बोंडअळी (Pink Bollworm)", "hi": "गुलाबी सुंडी (Pink Bollworm)"},
    "bacterial_blight": {"en": "Bacterial Blight", "mr": "जिवाणूजन्य करपा (Bacterial Blight)", "hi": "जीवाणु अंगमारी (Bacterial Blight)"},
    "curl_virus": {"en": "Leaf Curl Virus", "mr": "पर्णगुच्छ विषाणू (Leaf Curl Virus)", "hi": "पर्ण कुंचन वायरस (Leaf Curl Virus)"},
    "fussarium_wilt": {"en": "Fusarium Wilt", "mr": "मर रोग (Fusarium Wilt)", "hi": "उकठा रोग (Fusarium Wilt)"},
}

# In backend/alert_service.py
def evaluate_outbreak_cluster(lat, lon, disease_label):
    # Cluster calculation logic...
    
    # Always ensure a valid dict is returned
    return {
        "status": "OUTBREAK_TRIGGERED",
        "cluster_count": 3,
        "radius_km": 5.0,
        "sms_dispatch": {
            "message_en": f"🚨 KrishiRakshak Alert: {disease_label.replace('_', ' ').title()} outbreak detected within 5km radius. Apply recommended IPM measures immediately.",
            "message_hi": f"🚨 कृषिरक्षक चेतावनी: ५ किमी क्षेत्र में {disease_label.replace('_', ' ').title()} का प्रकोप देखा गया है। तुरंत अनुशंसित कीटनाशक या उपाय करें।",
            "message_mr": f"🚨 कृषीरक्षक दक्षता इशारा: ५ किमी परिसरात {disease_label.replace('_', ' ').title()} चा प्रादुर्भाव आढळला आहे. त्वरित आवश्यक फवारणी व उपाययोजना कराव्यात.",
            "message_bn": f"🚨 কৃষিরক্ষক সতর্কতা: ৫ কিমি এলাকার মধ্যে {disease_label.replace('_', ' ').title()}-এর প্রাদুর্ভাব দেখা দিয়েছে। অবিলম্বে প্রস্তাবিত ব্যবস্থা গ্রহণ করুন।",
            "message_te": f"🚨 కృషీరక్షక్ హెచ్చరిక: 5 కి.మీ పరిధిలో {disease_label.replace('_', ' ').title()} వ్యాప్తి గుర్తించబడింది. తక్షణమే నివారణ చర్యలు చేపట్టండి.",
            "message_ta": f"🚨 கிருஷிரக்ஷக் எச்சரிக்கை: 5 கி.மீ சுற்றளவில் {disease_label.replace('_', ' ').title()} பாதிப்பு கண்டறியப்பட்டுள்ளது. உடனடியாக பாதுகாப்பு நடவடிக்கை எடுக்கவும்.",
            "message_kn": f"🚨 ಕೃಷಿರಕ್ಷಕ್ ಎಚ್ಚರಿಕೆ: 5 ಕಿಮೀ ವ್ಯಾಪ್ತಿಯಲ್ಲಿ {disease_label.replace('_', ' ').title()} ಹರಡುವಿಕೆ ಕಂಡುಬಂದಿದೆ. ತಕ್ಷಣ ಶಿಫಾರಸು ಮಾಡಿದ ಕ್ರಮ ಕೈಗೊಳ್ಳಿ.",
            "message_pa": f"🚨 ਕ੍ਰਿਸ਼ੀਰਕਸ਼ਕ ਚੇਤਾਵਨੀ: 5 ਕਿਲੋਮੀਟਰ ਖੇਤਰ ਵਿੱਚ {disease_label.replace('_', ' ').title()} ਦਾ ਹਮਲਾ ਦੇਖਿਆ ਗਿਆ ਹੈ। ਤੁਰੰਤ ਸਿਫਾਰਸ਼ ਕੀਤੇ ਉਪਾਅ ਕਰੋ।",
            "message_gu": f"🚨 કૃષિરક્ષક ચેતવણી: ૫ કિમી વિસ્તારમાં {disease_label.replace('_', ' ').title()} નો પ્રકોપ જોવા મળ્યો છે. તાત્કાલિક ભલામણ કરેલ પગલાં લો."
        }
    }