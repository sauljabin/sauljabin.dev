function save(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch (e) {}
}

// Remember the language picked, so the redirect in <head> respects it.
function initLang() {
  document.querySelectorAll("[data-lang]").forEach((link) => {
    link.addEventListener("click", () => save("lang", link.dataset.lang));
  });
}

function initTheme() {
  const root = document.documentElement;
  const meta = document.querySelectorAll('meta[name="theme-color"]');
  document.querySelector(".theme-toggle").addEventListener("click", () => {
    const current = root.dataset.theme || (matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark");
    const next = current === "light" ? "dark" : "light";
    root.dataset.theme = next;
    save("theme", next);
    meta.forEach((m) => m.setAttribute("content", next === "light" ? "#f6f3ea" : "#0e0f13"));
  });
}

function compact(n) {
  return n >= 1000 ? `${(n / 1000).toFixed(1).replace(/\.0$/, "")}k` : String(n);
}

// Refresh the star counts; the values in the HTML are the fallback.
function loadStars() {
  document.querySelectorAll(".card[data-repo]").forEach(async (card) => {
    try {
      const res = await fetch(`https://api.github.com/repos/${card.dataset.repo}`);
      if (!res.ok) return;
      const { stargazers_count: stars } = await res.json();
      card.querySelector(".stars-count").textContent = compact(stars);
    } catch (e) {}
  });
}

document.querySelector(".year").textContent = new Date().getFullYear();
initLang();
initTheme();
loadStars();
