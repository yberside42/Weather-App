from __future__ import annotations

import os, requests
from django.conf import settings

BASE = getattr(settings, "OPENWEATHER_BASE_URL", "https://api.openweathermap.org").rstrip("/")
API_KEY = getattr(settings, "OPENWEATHER_API_KEY", os.getenv("OPENWEATHER_API_KEY", ""))
LANG = getattr(settings, "OPENWEATHER_LANG", "es")
API_BASE = "https://api.openweathermap.org/data/2.5/weather"
ONECALL_URL = getattr(settings, "OPENWEATHER_ONECALL_URL","https://api.openweathermap.org/data/2.5/onecall",)

class OpenWeatherError(Exception):
    pass

def geocode(q, limit: int = 5):
    if not API_KEY:
        raise OpenWeatherError("Falta OPENWEATHER_API_KEY en .env")
    if not q or not q.strip():
        return []
    
    url = f"{BASE}/geo/1.0/direct"
    params = {"q": q.strip(), "limit": limit, "appid": API_KEY}
    try:
        r = requests.get(url, params = params, timeout=10)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        raise OpenWeatherError(str(e)) from e
    
    results = []
    for d in data: 
        results.append({
            "name": d.get("name"),
            "country": d.get("country"),
            "state": d.get("state"),
            "lat": d.get("lat"),
            "lon": d.get("lon"),
        })
    return results
        
class ProviderError(Exception):
    """Error genérico de proveedor de clima."""

def _build_params(lat, lon):
    return {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",  
        "lang": "en",     
    }

def fetch_current_by_coords(lat, lon, timeout: int = 6):
    """Pide a OpenWeather el clima actual por coordenadas.
    
    Raises:
        ProviderError: ante fallas de red, respuesta inválida o status != 200.
    """
    if not API_KEY:
        raise ProviderError("Falta OPENWEATHER_API_KEY en variables de entorno.")

    try:
        resp = requests.get(API_BASE, params=_build_params(lat, lon), timeout=timeout)
    except requests.RequestException as e:
        raise ProviderError(f"Fallo de red al consultar OpenWeather: {e}") from e

    if resp.status_code != 200:
        try:
            payload = resp.json()
            msg = payload.get("message", "Respuesta no exitosa del proveedor.")
        except Exception:
            msg = "Respuesta no exitosa del proveedor."
        raise ProviderError(f"HTTP {resp.status_code}: {msg}")

    try:
        return resp.json()
    except ValueError as e:
        raise ProviderError("Respuesta del proveedor no es JSON válido.") from e

    