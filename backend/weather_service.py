import requests

def fetch_current_weather(lat: float, lon: float):
    """
    Fetches real-time temperature, humidity, and min/max temperatures
    for the provided latitude and longitude using Open-Meteo.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"current=temperature_2m,relative_humidity_2m,weather_code&"
        f"daily=temperature_2m_max,temperature_2m_min&timezone=auto"
    )
    
    try:
        response = requests.get(url, timeout=5).json()
        current = response.get("current", {})
        daily = response.get("daily", {})
        
        t_max = daily.get("temperature_2m_max", [32.0])[0]
        t_min = daily.get("temperature_2m_min", [24.0])[0]
        
        return {
            "temperature": current.get("temperature_2m", 30.0),
            "humidity": current.get("relative_humidity_2m", 70),
            "condition": "Normal",
            "temp_max": t_max,
            "temp_min": t_min,
            "source": "Open-Meteo Live API"
        }
    except Exception:
        # Fallback values if offline
        return {
            "temperature": 30.0,
            "humidity": 70,
            "condition": "Normal",
            "temp_max": 32.0,
            "temp_min": 24.0,
            "source": "Fallback Offline Model"
        }

def calculate_daily_gdd(temp_max: float, temp_min: float, base_temp: float = 12.0) -> float:
    """
    Calculates Daily Growing Degree Days (GDD).
    Formula: ((T_max + T_min) / 2) - T_base
    """
    mean_temp = (float(temp_max) + float(temp_min)) / 2.0
    gdd = mean_temp - base_temp
    return round(max(0.0, gdd), 2)