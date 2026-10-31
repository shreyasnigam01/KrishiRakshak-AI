"""
backend/gemini_service.py
Multimodal Gemini Vision & Chatbot Service for KrishiRakshak
Integrates Google Gemini API for high-precision leaf and pest stage diagnosis and chat.
Supports both legacy 'AIza' keys and the new 2026 'AQ.' authentication keys via x-goog-api-key header.
"""

import io
import os
import json
import base64
import requests
from PIL import Image
from typing import Dict, Any, Optional, List, Tuple

# Standard Google AI Studio model names in priority order
GEMINI_MODELS = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-2.0-flash",
    "gemini-1.5-pro",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-002",
    "gemini-pro"
]

def get_auth_headers(api_key: str) -> Dict[str, str]:
    """
    Returns required HTTP headers.
    Crucial: Google's new 2026 'AQ.' keys require the 'x-goog-api-key' header.
    """
    clean_key = api_key.strip()
    return {
        "x-goog-api-key": clean_key,
        "Content-Type": "application/json"
    }

def encode_image_to_base64(image: Image.Image) -> str:
    """
    Resizes image to max 1024px and encodes to base64 JPEG for fast network transmission.
    """
    img_copy = image.copy().convert("RGB")
    img_copy.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
    buffered = io.BytesIO()
    img_copy.save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Robust JSON extractor that handles markdown code fences, leading text, or raw JSON.
    """
    if not text:
        return None
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except Exception:
        # Fallback: slice from first { to last }
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(cleaned[start:end+1])
            except Exception:
                pass
    return None

def get_available_models(api_key: str) -> List[str]:
    """
    Fetches the exact list of available models for this specific API key from Google.
    """
    if not api_key:
        return []
    clean_key = api_key.strip()
    headers = get_auth_headers(clean_key)
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={clean_key}"
    try:
        resp = requests.get(url, headers=headers, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            return [
                m["name"].replace("models/", "")
                for m in data.get("models", [])
                if "generateContent" in m.get("supportedGenerationMethods", [])
            ]
    except Exception:
        pass
    return []

def get_candidate_models(api_key: str) -> List[str]:
    """
    Returns prioritized list of candidate models guaranteed to never be empty.
    """
    available = get_available_models(api_key)
    candidates = []
    
    preferred = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-2.0-flash",
        "gemini-1.5-pro",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-002",
        "gemini-pro"
    ]
    for pref in preferred:
        if pref in available and pref not in candidates:
            candidates.append(pref)
            
    for m in available:
        if ("flash" in m or "vision" in m or "pro" in m) and m not in candidates:
            if not any(skip in m for skip in ["embedding", "aqa", "imagen"]):
                candidates.append(m)
                
    if not candidates:
        candidates = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-flash-latest", "gemini-1.5-pro"]
        
    return candidates

def test_gemini_connection(api_key: str) -> Dict[str, Any]:
    """
    Verifies that the Gemini API key is valid and working by testing against Google AI Studio.
    Returns exact error feedback if invalid.
    """
    if not api_key or not api_key.strip():
        return {"success": False, "message": "API Key is empty. Please paste your key."}
        
    clean_key = api_key.strip()
    headers = get_auth_headers(clean_key)
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={clean_key}"
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            candidates = get_candidate_models(clean_key)
            chosen = candidates[0] if candidates else "gemini-1.5-flash"
            return {
                "success": True,
                "model": chosen,
                "message": f"Connected successfully with Google AI Studio! Model: {chosen}"
            }
        else:
            try:
                err_data = resp.json()
                raw_msg = err_data.get("error", {}).get("message", f"HTTP {resp.status_code}")
            except Exception:
                raw_msg = f"HTTP Error {resp.status_code}"
                
            if "API_KEY_INVALID" in raw_msg or "API key not valid" in raw_msg:
                return {
                    "success": False,
                    "message": "Invalid API Key. Please verify in Google AI Studio (https://aistudio.google.com/app/apikey)."
                }
            elif "not been used in project" in raw_msg or "it is disabled" in raw_msg:
                return {
                    "success": False,
                    "message": "Generative Language API is disabled in your Google Cloud project."
                }
            elif "RESOURCE_EXHAUSTED" in raw_msg or resp.status_code == 429:
                return {
                    "success": False,
                    "message": "Quota limit reached (HTTP 429). Please wait a moment or check your AI Studio quota."
                }
            else:
                return {
                    "success": False,
                    "message": f"Google API Error: {raw_msg}"
                }
    except requests.exceptions.Timeout:
        return {"success": False, "message": "Connection timed out. Check your internet connection."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "Network connection error. Check if your Wi-Fi or firewall blocks Google APIs."}
    except Exception as e:
        return {"success": False, "message": f"Connection error: {str(e)}"}

def diagnose_with_gemini(image: Image.Image, api_key: str, lang: str = "English") -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Calls Gemini Vision API to perform precision foliar pathology,
    leaf damage stage analysis, and pest lifecycle stage determination.
    Returns (result_dict, error_message).
    """
    if not api_key or not api_key.strip():
        return None, "No API key provided"

    clean_key = api_key.strip()
    headers = get_auth_headers(clean_key)

    try:
        img_b64 = encode_image_to_base64(image)
    except Exception as e:
        return None, f"Image encoding failed: {str(e)}"

    system_prompt = (
        "You are an expert Chief Plant Pathologist and Agricultural Entomologist (ICAR-CICR / NRRI). "
        "Analyze this crop leaf image carefully. "
        "1. Identify whether the plant is Cotton, Rice/Paddy, or another crop.\n"
        "2. Diagnose the exact pest, disease, or healthy state.\n"
        "3. Determine the Leaf Damage Stage: "
        "   - Stage 1: Initial / Incubation Phase (< 10% foliar lesions, mild micro-spots)\n"
        "   - Stage 2: Medium / Active Expansion Phase (10% - 30% foliar lesions, angular necrosis, curl)\n"
        "   - Stage 3: Advanced / Severe Blight & Breakdown (> 30% foliar lesions, severe scorch/hopper burn)\n"
        "4. Determine the Pest Biological Lifecycle Stage (e.g. egg, 1st instar pre-boring, 2nd-3rd instar larva, nymph aggregation, pupation, or adult).\n"
        "5. Recommend exact chemical pesticide dosages (per liter, per 15L pump, per acre), pre-harvest interval (PHI), and certified organic bio-alternatives.\n"
        "6. Specimen Validity & Anomaly Detection: Check if the uploaded image is actually an agricultural crop leaf. If it is a non-plant object, person, tool, vehicle, or animal, set is_valid_crop_leaf to false and provide anomaly_warning.\n"
        "Return ONLY a clean JSON object with this exact schema (no markdown, no extra commentary):\n"
        "{\n"
        '  "is_valid_crop_leaf": true,\n'
        '  "anomaly_warning": null,\n'
        '  "disease_label": "bacterial_blight" | "bollworm" | "brown_planthopper" | "curl_virus" | "leaf_folder" | "stem_borer" | "healthy" | string,\n'
        '  "common_name": "Pink Bollworm / Yellow Stem Borer / Bacterial Blight",\n'
        '  "crop": "Cotton / Paddy",\n'
        '  "confidence": 96.5,\n'
        '  "leaf_stage": {\n'
        '    "stage_num": 1,\n'
        '    "title": "Stage 1: Initial / Incubation Phase",\n'
        '    "description": "Visual evidence of early micro-lesions...",\n'
        '    "lesion_percentage": 6.5,\n'
        '    "photosynthetic_health": 90.0,\n'
        '    "severity_label": "Low / Early"\n'
        '  },\n'
        '  "pest_stage": {\n'
        '    "stage_name": "Stage 1: Egg / Oviposition & 1st Instar Pre-Boring",\n'
        '    "biological_process": "Biological process description...",\n'
        '    "etl_status": "Below ETL — Biocontrol Peak Window",\n'
        '    "vulnerability_window": "Squaring to early flowering"\n'
        '  },\n'
        '  "preventive_measures": [\n'
        '    "Install pheromone traps @ 5 traps/acre",\n'
        '    "Release Trichogramma egg parasitoids @ 60,000/acre"\n'
        '  ],\n'
        '  "chemical_options": [\n'
        '    {\n'
        '      "name": "Chlorantraniliprole 18.5% SC",\n'
        '      "dose_per_liter": "0.3 ml / Liter water",\n'
        '      "dose_per_15l_pump": "4.5 ml per 15L tank",\n'
        '      "dose_per_acre": "60 ml in 200 L water / acre",\n'
        '      "phi_days": 14,\n'
        '      "timing": "Spray late afternoon"\n'
        '    }\n'
        '  ],\n'
        '  "bio_options": [\n'
        '    {\n'
        '      "name": "Neem Oil 10,000 ppm",\n'
        '      "dose_per_liter": "2.5 ml / Liter water",\n'
        '      "dose_per_15l_pump": "37.5 ml per 15L tank",\n'
        '      "dose_per_acre": "500 ml in 200 L water / acre",\n'
        '      "instructions": "Anti-feedant and repellent"\n'
        '    }\n'
        '  ],\n'
        '  "details": {\n'
        '    "pathogen_agent": "Scientific organism name",\n'
        '    "trophic_type": "Trophic mode",\n'
        '    "entry_route": "Foliar route",\n'
        '    "key_r_genes": "Host defense genes",\n'
        '    "susceptible_stage": "Susceptible stage",\n'
        '    "resistant_cultivars": ["Cultivar 1", "Cultivar 2"]\n'
        '  }\n'
        "}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": system_prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_b64
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2
        },
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }

    candidates = get_candidate_models(clean_key)
    last_err = "No response from Gemini API"
    
    for model_name in candidates:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={clean_key}"
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=25)
            if resp.status_code == 200:
                data = resp.json()
                candidates_resp = data.get("candidates", [])
                if candidates_resp:
                    cand0 = candidates_resp[0]
                    content = cand0.get("content", {})
                    parts = content.get("parts", [])
                    if parts:
                        text = parts[0].get("text", "")
                        parsed = extract_json_from_text(text)
                        if parsed:
                            parsed["source"] = f"Gemini Multimodal AI ({model_name})"
                            return parsed, None
                        else:
                            last_err = f"Could not parse pathology JSON from {model_name}."
                    else:
                        finish_reason = cand0.get("finishReason", "EMPTY")
                        last_err = f"{model_name} response finished with: {finish_reason}"
                else:
                    last_err = f"{model_name} returned empty candidates."
            else:
                try:
                    err_msg = resp.json().get("error", {}).get("message", f"HTTP {resp.status_code}")
                except Exception:
                    err_msg = f"HTTP {resp.status_code}"
                last_err = f"{model_name}: {err_msg}"
        except requests.exceptions.Timeout:
            last_err = f"{model_name} timed out after 25s."
            continue
        except Exception as e:
            last_err = f"{model_name}: {str(e)}"
            continue

    return None, last_err

def chat_with_gemini(
    query: str,
    api_key: str,
    lang: str = "English",
    diagnosis_context: Optional[Dict[str, Any]] = None,
    weather_context: Optional[Dict[str, Any]] = None,
    chat_history: Optional[List[Dict[str, str]]] = None
) -> Optional[str]:
    """
    Sends conversational agronomist query to Gemini API in the chosen language.
    """
    if not api_key or not api_key.strip():
        return None

    clean_key = api_key.strip()
    headers = get_auth_headers(clean_key)
    
    context_str = ""
    if diagnosis_context and diagnosis_context.get("status") in ["CONFIRMED", "EARLY_INCUBATION"]:
        diag_name = diagnosis_context.get("disease_label", "Crop").replace("_", " ").title()
        lf_stg = diagnosis_context.get("leaf_stage", {}).get("title", "Stage 1")
        pst_stg = diagnosis_context.get("pest_stage", {}).get("stage_name", "Initial")
        chems = diagnosis_context.get("chemical_options", [])
        chem_info = ", ".join([f"{c['name']} ({c.get('dose_per_liter', '')})" for c in chems[:2]])
        context_str = (
            f"CURRENT DIAGNOSED FIELD CONTEXT:\n"
            f"- Disease / Pest: {diag_name}\n"
            f"- Leaf Damage Stage: {lf_stg}\n"
            f"- Pest Biological Stage: {pst_stg}\n"
            f"- Recommended Prescriptions: {chem_info}\n"
        )
    if weather_context:
        context_str += f"- Local Weather: Temp {weather_context.get('temperature', 30)}°C, Humidity {weather_context.get('humidity', 70)}%, GDD: {weather_context.get('gdd', 15)}\n"
    if diagnosis_context and "anomaly" in diagnosis_context:
        anom = diagnosis_context["anomaly"]
        context_str += (
            f"- Foliar Specimen Validity: {anom.get('badge_label', 'Verified')} "
            f"(Foliar tissue: {anom.get('foliar_percentage', 100)}%, Anomaly Score: {anom.get('anomaly_score', 0)}%, Status: {anom.get('anomaly_status', 'IN_DISTRIBUTION')})\n"
            f"- Specimen Advisory: {anom.get('explanation', '')}\n"
        )

    system_msg = (
        f"You are KrishiRakshak AI, an expert agricultural scientist advising an Indian farmer. "
        f"Respond FLUENTLY AND DIRECTLY in {lang}. Use clear bullet points and simple farmer-friendly language. "
        f"Always provide exact pesticide dosages (per liter, per 15L sprayer pump, and per acre), organic/bio alternatives, and spraying safety rules. "
        f"{context_str}"
    )

    contents = [{"parts": [{"text": system_msg}]}]
    if chat_history:
        for m in chat_history[-6:]:
            role = "user" if m.get("role") == "user" else "model"
            contents.append({"parts": [{"text": m.get("content", "")}]})
            
    contents.append({"parts": [{"text": query}]})

    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 800
        },
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }

    candidates = get_candidate_models(clean_key)

    for model_name in candidates:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={clean_key}"
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                cand_list = data.get("candidates", [])
                if cand_list:
                    parts = cand_list[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
        except Exception:
            continue

    return None
