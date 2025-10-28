from datetime import datetime

def _precip_mm(payload):
    """Busca precipitación (lluvia/nieve) en mm/h (prioriza 1h)."""
    rain = payload.get("rain", {}) or {}
    snow = payload.get("snow", {}) or {}
    return float(rain.get("1h") or rain.get("3h") or snow.get("1h") or snow.get("3h") or 0.0)

def normalize_current(payload):
    """Normaliza el clima actual de OpenWeather a un esquema interno sencillo."""
    main = payload.get("main", {}) or {}
    wind = payload.get("wind", {}) or {}
    weather_list = payload.get("weather", []) or []
    first = weather_list[0] if weather_list else {}

    return {
        "temp": float(main.get("temp", 0.0)),
        "feels_like": float(main.get("feels_like", 0.0)),
        "humidity": int(main.get("humidity", 0)),
        "wind_speed": float(wind.get("speed", 0.0)),
        "precip_mm": _precip_mm(payload),
        "condition": str(first.get("main") or ""),
        "description": str(first.get("description") or "").capitalize(),
        "icon": str(first.get("icon") or ""),  
        "dt": int(payload.get("dt", 0)),       
        "name": payload.get("name") or "",
        "coord": payload.get("coord") or {},
    }