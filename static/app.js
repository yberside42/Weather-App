
(function () {
  const form = document.getElementById("search-form");
  const input = document.getElementById("search-input");
  const resultsList = document.getElementById("search-results");
  const statusEl = document.getElementById("search-status");

  if (!form || !input) return;

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const q = (input.value || "").trim();
    if (!q) return;

    if (statusEl) {
      statusEl.textContent = "Buscando...";
    }
    if (resultsList) {
      resultsList.innerHTML = "";
    }

    try {
      const r = await fetch(`/api/search/?q=${encodeURIComponent(q)}`);
      if (!r.ok) {
        throw new Error(`Error ${r.status}`);
      }
      const data = await r.json();

      if (!Array.isArray(data) || data.length === 0) {
        if (statusEl) statusEl.textContent = "No encontramos esa ciudad. Prueba con otra.";
        return;
      }

      // Results
      if (resultsList) {
        resultsList.innerHTML = "";
        for (const item of data) {
          const li = document.createElement("li");
          const name = [item.name, item.state, item.country].filter(Boolean).join(", ");
          const url = `/city/?lat=${encodeURIComponent(item.lat)}&lon=${encodeURIComponent(item.lon)}&name=${encodeURIComponent(name)}`;
          li.innerHTML = `<a href="${url}">${name}</a>`;
          resultsList.appendChild(li);
        }
      }

      if (statusEl) statusEl.textContent = "";
    } catch (err) {
      console.error(err);
      if (statusEl) statusEl.textContent = "No se pudo obtener resultados. Intenta de nuevo.";
    }
  });
})();
