const scene = document.querySelector(".scene");
const toggle = document.querySelector("[data-motion-toggle]");
const label = document.querySelector("[data-motion-label]");

toggle.addEventListener("click", () => {
  const isPaused = scene.classList.toggle("is-paused");

  toggle.setAttribute("aria-pressed", String(isPaused));
  label.textContent = isPaused
    ? "Продовжити обертання"
    : "Зупинити обертання";
});
