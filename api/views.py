from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.cache import cache

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.cache import cache_page

from .services.openweather import geocode, OpenWeatherError, fetch_current_by_coords, ProviderError
from .services.normalizer import normalize_current
from .services.forecast import get_weekly_forecast

# Create your views here.

def health(request):
    return JsonResponse({"status": "ok"})

@require_GET
def search(request): 
    # Read query string (?q=...) and call geocoding
    q = request.GET.get("q", "")
    try:
        results = geocode(q, limit=6)
        return JsonResponse(results, safe=False, status = 200)
    except OpenWeatherError as e:
        return JsonResponse({"detail": str(e)}, status=503)
    
    
def _cache_key(lat: float, lon: float) -> str:
    return f"weather:current:{round(lat, 4)},{round(lon, 4)}"

@require_GET
def weather_current(request):
    # Validate and parse lat/lon query params
    try:
        lat = float(request.GET.get("lat", ""))
        lon = float(request.GET.get("lon", ""))
    except ValueError:
        return JsonResponse({"detail": "lat/lon inválidos"}, status=400)

    try:
        # Openweather
        raw = fetch_current_by_coords(lat=lat, lon=lon) 
        # Normalize
        data = normalize_current(raw)               
        return JsonResponse(data, status=200)
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=503)
    

@api_view(["GET"])
@permission_classes([AllowAny])
@cache_page(60 * 60, cache="locmem")  # 1 hora por URL (lat/lon)
def weather_forecast(request):
    # Read and coerce lat/lon from query
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError):
        return Response({"ok": False, "error": "Parámetros lat/lon inválidos."},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        days = get_weekly_forecast(lat, lon)
        return Response({"ok": True, "data": {"days": days}}, status=200)
    except Exception as e:
        return Response({"ok": False, "error": str(e)}, status=502)
    