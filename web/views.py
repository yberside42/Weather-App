from django.shortcuts import render, redirect 

def home(request):
    q = (request.GET.get("q") or "").strip()
    return render(request, "inicio.html", {"q": q})

def city(request):
    # Parameters for the city search
    q = (request.GET.get("q") or "").strip()
    name = (request.GET.get("name") or q or "Selected City").strip()
    state = (request.GET.get("state") or "").strip()
    country = (request.GET.get("country") or "").strip()
    lat_s = request.GET.get("lat")
    lon_s = request.GET.get("lon")
    
    # Error handling related to lattitude and longitude
    try:
        lat = float(lat_s) if lat_s not in (None, "") else None
        lon = float(lon_s) if lon_s not in (None, "") else None
    except ValueError:
        lat = lon = None


    if (lat is None or lon is None) and q:
        return redirect(f"/?q={q}")

    if lat is None or lon is None:
        return render(request, "city.html", {
            "city": {"name": name, "state": state, "country": country, "lat": None, "lon": None},
            "no_coords": True,
        }, status=400)

    # City details
    ctx = {"city": {"name": name, "state": state, "country": country, "lat": lat, "lon": lon}}
    return render(request, "city.html", ctx)

def saved_cities(request):
    return render(request, "saved.html")

