const state = {
  desks: [],
  weatherImages: [],
  weatherIndex: 0,
};

const DESK_STORAGE_KEY = "eliminacode-desks";

const desksGrid = document.querySelector("#desks-grid");
const deskList = document.querySelector("#desk-list");
const deskForm = document.querySelector("#desk-form");
const weatherImageEl = document.querySelector("#weather-image");
const weatherCaptionEl = document.querySelector("#weather-caption");
const nextWeatherBtn = document.querySelector("#next-weather");
const exportConfigBtn = document.querySelector("#export-config");
const resetDefaultBtn = document.querySelector("#reset-default");

async function loadJson(path, fallback) {
  try {
    const response = await fetch(path);
    if (!response.ok) {
      throw new Error(`Impossibile leggere ${path}`);
    }
    return await response.json();
  } catch (error) {
    console.warn(error);
    return fallback;
  }
}

function getDefaultWeather() {
  return {
    items: [
      { title: "Sole", url: "https://picsum.photos/seed/sunny/1200/700" },
      { title: "Nuvoloso", url: "https://picsum.photos/seed/cloud/1200/700" },
      { title: "Pioggia", url: "https://picsum.photos/seed/rainy/1200/700" },
    ],
  };
}

function saveDesks() {
  localStorage.setItem(DESK_STORAGE_KEY, JSON.stringify(state.desks));
}

function loadStoredDesks() {
  const raw = localStorage.getItem(DESK_STORAGE_KEY);
  if (!raw) {
    return null;
  }

  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : null;
  } catch {
    return null;
  }
}

function ensureSingleMain(targetId) {
  state.desks = state.desks.map((desk) => ({
    ...desk,
    isMain: desk.id === targetId,
  }));
}

function changeDeskValue(id, direction) {
  state.desks = state.desks.map((desk) => {
    if (desk.id !== id) {
      return desk;
    }
    const nextValue = desk.value + direction * desk.step;
    return {
      ...desk,
      value: Math.max(0, nextValue),
    };
  });

  saveDesks();
  renderDesks();
  renderDeskList();
}

function toggleVisibility(id) {
  state.desks = state.desks.map((desk) => (desk.id === id ? { ...desk, visible: !desk.visible } : desk));
  saveDesks();
  renderDesks();
  renderDeskList();
}

function removeDesk(id) {
  const removedWasMain = state.desks.find((desk) => desk.id === id)?.isMain;
  state.desks = state.desks.filter((desk) => desk.id !== id);

  if (removedWasMain && state.desks.length > 0) {
    state.desks[0].isMain = true;
  }

  saveDesks();
  renderDesks();
  renderDeskList();
}

function setMainDesk(id) {
  ensureSingleMain(id);
  saveDesks();
  renderDesks();
  renderDeskList();
}

function renderDesks() {
  desksGrid.innerHTML = "";

  state.desks
    .filter((desk) => desk.visible)
    .forEach((desk) => {
      const template = document.querySelector("#desk-card-template").content.cloneNode(true);
      const card = template.querySelector(".desk-card");
      const title = template.querySelector(".desk-title");
      const number = template.querySelector(".desk-number");
      const plusBtn = template.querySelector(".plus");
      const minusBtn = template.querySelector(".minus");

      card.style.setProperty("--desk-color", desk.color);
      if (desk.isMain) {
        card.classList.add("main");
      }

      title.textContent = `${desk.name} (step ${desk.step})`;
      number.textContent = String(desk.value);
      plusBtn.addEventListener("click", () => changeDeskValue(desk.id, 1));
      minusBtn.addEventListener("click", () => changeDeskValue(desk.id, -1));

      desksGrid.appendChild(template);
    });

  if (!state.desks.some((desk) => desk.visible)) {
    const empty = document.createElement("p");
    empty.textContent = "Nessun banco visibile. Attiva almeno un banco dal configuratore.";
    empty.className = "hidden-label";
    desksGrid.appendChild(empty);
  }
}

function renderDeskList() {
  deskList.innerHTML = "";

  state.desks.forEach((desk) => {
    const item = document.createElement("li");
    item.className = "desk-item";

    const info = document.createElement("div");
    info.innerHTML = `<strong>${desk.name}</strong> <small>#${desk.value} | ${desk.visible ? "visibile" : "nascosto"}</small>`;

    const actions = document.createElement("div");
    actions.className = "item-actions";

    const toggleBtn = document.createElement("button");
    toggleBtn.className = "small-btn";
    toggleBtn.textContent = desk.visible ? "Nascondi" : "Mostra";
    toggleBtn.addEventListener("click", () => toggleVisibility(desk.id));

    const mainBtn = document.createElement("button");
    mainBtn.className = "small-btn";
    mainBtn.textContent = desk.isMain ? "Principale ✔" : "Rendi principale";
    mainBtn.addEventListener("click", () => setMainDesk(desk.id));

    const deleteBtn = document.createElement("button");
    deleteBtn.className = "danger-btn";
    deleteBtn.textContent = "Elimina";
    deleteBtn.addEventListener("click", () => removeDesk(desk.id));

    actions.append(toggleBtn, mainBtn, deleteBtn);
    item.append(info, actions);
    deskList.appendChild(item);
  });
}

function renderWeather() {
  if (!state.weatherImages.length) {
    weatherCaptionEl.textContent = "Nessuna immagine meteo disponibile.";
    weatherImageEl.removeAttribute("src");
    return;
  }

  const item = state.weatherImages[state.weatherIndex % state.weatherImages.length];
  weatherImageEl.src = item.url;
  weatherImageEl.alt = item.title;
  weatherCaptionEl.textContent = item.title;
}

function nextWeather() {
  state.weatherIndex = Math.floor(Math.random() * state.weatherImages.length);
  renderWeather();
}

function exportConfig() {
  const payload = JSON.stringify({ desks: state.desks }, null, 2);
  const blob = new Blob([payload], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "eliminacode-config.json";
  a.click();
  URL.revokeObjectURL(url);
}

async function resetToDefault() {
  const defaultLayout = await loadJson("./config/default-layout.json", { desks: [] });
  state.desks = defaultLayout.desks;
  saveDesks();
  renderDesks();
  renderDeskList();
}

deskForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = new FormData(deskForm);

  const newDesk = {
    id: `desk-${crypto.randomUUID()}`,
    name: String(formData.get("name") || "Banco").trim(),
    color: String(formData.get("color") || "#0d9488"),
    value: Number(formData.get("value") || 0),
    step: Math.max(1, Number(formData.get("step") || 1)),
    visible: formData.get("visible") === "on",
    isMain: formData.get("isMain") === "on",
  };

  if (newDesk.isMain) {
    ensureSingleMain(newDesk.id);
  }

  state.desks.push(newDesk);

  if (!state.desks.some((desk) => desk.isMain)) {
    state.desks[0].isMain = true;
  }

  saveDesks();
  renderDesks();
  renderDeskList();
  deskForm.reset();
  deskForm.elements.color.value = "#0d9488";
  deskForm.elements.visible.checked = true;
});

nextWeatherBtn.addEventListener("click", nextWeather);
exportConfigBtn.addEventListener("click", exportConfig);
resetDefaultBtn.addEventListener("click", resetToDefault);

async function init() {
  const [defaultLayout, weatherPayload] = await Promise.all([
    loadJson("./config/default-layout.json", { desks: [] }),
    loadJson("./data/weather-images.json", getDefaultWeather()),
  ]);

  state.weatherImages = weatherPayload.items || [];
  const stored = loadStoredDesks();
  state.desks = stored?.length ? stored : defaultLayout.desks || [];

  if (!state.desks.some((desk) => desk.isMain) && state.desks.length) {
    state.desks[0].isMain = true;
  }

  renderDesks();
  renderDeskList();
  nextWeather();
}

init();
