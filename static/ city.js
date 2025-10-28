function initCityWeather() {
  const container = document.getElementById('city');
  if (!container) return; 

  const lat = container.dataset.lat;
  const lon = container.dataset.lon;

  const statusBox = document.getElementById('weather-status');
  const contentBox = document.getElementById('weather-content');

  const descEl   = document.getElementById('weather-desc');
  const iconEl   = document.getElementById('weather-icon');
  const tempEl   = document.getElementById('w-temp');
  const feelsEl  = document.getElementById('w-feels');
  const humEl    = document.getElementById('w-hum');
  const windEl   = document.getElementById('w-wind');
  const precipEl = document.getElementById('w-precip');

  console.log("City script loaded");
  console.log("Dataset:", container.dataset);

  if (!lat || !lon) {
    statusBox.textContent = 'No hay coordenadas para esta ciudad.';
    return;
  }

  (async () => {
    try {
      const url = `/api/weather/current?lat=${lat}&lon=${lon}`;
      console.log("URL final:", url);
      const res = await fetch(url);
      const payload = await res.json();
      console.log("Payload:", payload);

      if (!res.ok || !payload.ok) {
        statusBox.textContent = payload?.error || `Sin datos (HTTP ${res.status})`;
        return;
      }

      const d = payload.data;
      descEl.textContent   = d.description || d.condition || '—';
      tempEl.textContent  = `${Number(temp).toFixed(1)} °C`;      
      feelsEl.textContent  = `${(d.feels_like ?? 0).toFixed(1)}`;
      humEl.textContent    = d.humidity ?? 0;
      windEl.textContent   = (d.wind_speed ?? 0).toFixed(1);
      precipEl.textContent = (d.precip_mm ?? 0).toFixed(1);

      if (d.icon) {
        iconEl.src = `https://openweathermap.org/img/wn/${d.icon}@2x.png`;
        iconEl.style.display = 'inline';
      }
      statusBox.style.display = 'none';
      contentBox.style.display = 'block';
    } catch (err) {
      console.error(err);
      statusBox.textContent = 'Error de red. Intenta más tarde.';
    }
  })();
}

document.addEventListener('DOMContentLoaded', initCityWeather);

document.addEventListener('htmx:afterSettle', initCityWeather);
document.addEventListener('turbo:load', initCityWeather);
