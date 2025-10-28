from django.urls import path
from . import views
from .views import weather_current

urlpatterns = [
    path("health/", views.health, name="api-health"),
    path("search/", views.search, name="api-search"),
    path("weather/current", views.weather_current, name="api-weather-current"),
    path("weather/forecast", views.weather_forecast),
]
