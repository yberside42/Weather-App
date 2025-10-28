# api/services/forecast.py
from __future__ import annotations
import os
from typing import Any, Dict, List
import requests
from datetime import datetime, timezone
from django.conf import settings

# --- OpenWeather One Call config
OW_API_KEY = getattr(settings, "OPENWEATHER_API_KEY", os.getenv("OPENWEATHER_API_KEY", ""))
OW_ONECALL_URL = getattr(settings, "OPENWEATHER_ONECALL_URL", "https://api.openweathermap.org/data/2.5/onecall")

class ForecastProviderError(RuntimeError): ...

def _ow_onecall_daily(lat: float, lon: float) -> List[Dict[str, Any]]:
    """Intenta obtener daily (8 días) desde OpenWeather One Call."""
    if not OW_API_KEY:
        raise ForecastProviderError("OPENWEATHER_API_KEY no configurada.")
    params = {
        "lat": lat, "lon": lon, "appid": OW_API_KEY,
        "units": "metric", "lang": "es",
        "exclude": "minutely,hourly,alerts,current",
    }
    r = requests.get(OW_ONECALL_URL, params=params, timeout=10)
    if not r.ok:
        # 401 es el caso típico sin plan/permiso
        try:
            j = r.json()
            msg = j.get("message")
        except Exception:
            msg = r.text[:200]
        raise ForecastProviderError(f"OpenWeather One Call HTTP {r.status_code}: {msg}")
    j = r.json()
    daily = (j.get("daily") or [])[:8]
    if not daily:
        raise ForecastProviderError("OpenWeather no devolvió 'daily'.")
    # Normaliza a (date, min, max, icon)
    out: List[Dict[str, Any]] = []
    for d in daily:
        icon = ((d.get("weather") or [{}])[0] or {}).get("icon")
        out.append({
            "date": datetime.fromtimestamp(d["dt"], tz=timezone.utc).date().isoformat(),
            "min": float(d["temp"]["min"]),
            "max": float(d["temp"]["max"]),
            "icon": icon,
        })
    return out

def _open_meteo_daily(lat: float, lon: float) -> List[Dict[str, Any]]:
    """Fallback gratuito usando Open-Meteo (7 días + hoy)."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "timezone": "UTC",
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    j = r.json()
    dates = j["daily"]["time"]
    tmin = j["daily"]["temperature_2m_min"]
    tmax = j["daily"]["temperature_2m_max"]
    codes = j["daily"]["weathercode"]
    # Mapea weathercode -> pseudo-icono OWM aproximado (suficiente para tarjetas)
    def code_to_icon(code: int) -> str:
        # tabla muy básica (puedes refinar luego)
        if code in (0,): return "01d"    # despejado
        if code in (1,2): return "02d"   # algo nublado
        if code in (3,):  return "04d"   # nublado
        if code in (45,48): return "50d" # niebla
        if code in (51,53,55,56,57): return "09d" # llovizna
        if code in (61,63,65): return "10d"      # lluvia
        if code in (66,67): return "10d"
        if code in (71,73,75,77): return "13d"   # nieve
        if code in (80,81,82): return "09d"      # chubascos
        if code in (95,96,99): return "11d"      # tormenta
        return "03d"
    out: List[Dict[str, Any]] = []
    for i in range(min(8, len(dates))):  # hoy + 7
        out.append({
            "date": dates[i],
            "min": float(tmin[i]),
            "max": float(tmax[i]),
            "icon": code_to_icon(int(codes[i])),
        })
    return out

def get_weekly_forecast(lat: float, lon: float) -> List[Dict[str, Any]]:
    """
    Devuelve lista de 8 dicts: {date (YYYY-MM-DD), min, max, icon}.
    Intenta OpenWeather One Call; si 401/errores de permiso, usa Open-Meteo.
    """
    try:
        return _ow_onecall_daily(lat, lon)
    except ForecastProviderError as e:
        # Si el error es por permisos/401, caemos a Open-Meteo.
        # (Para depurar: print(str(e)) o usa tu logger)
        return _open_meteo_daily(lat, lon)
