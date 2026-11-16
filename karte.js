// Startseite: Ortsteil (Einwohner, Wachstum) oder Satellit unter dem Mauszeiger
(() => {
  const flaeche = document.querySelector(".karte-flaeche");
  const tipp = flaeche.querySelector(".tipp");
  const [name, info] = [document.createElement("strong"), document.createElement("span")];
  tipp.append(name, info);

  flaeche.querySelectorAll(".ortsteile path, .satellit").forEach((p) => {
    p.addEventListener("pointerenter", () => {
      name.textContent = p.dataset.name;
      info.textContent = p.dataset.info;
      tipp.hidden = false;
    });
  });
  flaeche.addEventListener("pointermove", (e) => {
    const r = flaeche.getBoundingClientRect();
    tipp.style.translate = `${e.clientX - r.left + 14}px ${e.clientY - r.top + 14}px`;
  });
  flaeche.addEventListener("pointerleave", () => { tipp.hidden = true; });

  // Wer weniger Bewegung eingestellt hat, sieht den Satelliten still vor der Stadt
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const svg = flaeche.querySelector("svg");
    svg.setCurrentTime(5);
    svg.pauseAnimations();
  }
})();
