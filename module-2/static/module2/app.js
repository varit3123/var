(function () {
  "use strict";

  function initSlider() {
    const track = document.getElementById("sliderTrack");
    if (!track) return;
    const slides = Array.from(track.children);
    const dots = document.getElementById("sliderDots");
    let index = 0;
    let timer;

    dots.innerHTML = slides.map(() => "<span></span>").join("");
    const dotItems = Array.from(dots.children);

    function show(nextIndex) {
      index = (nextIndex + slides.length) % slides.length;
      track.style.transform = `translateX(-${index * 100}%)`;
      dotItems.forEach((dot, itemIndex) => dot.classList.toggle("active", itemIndex === index));
    }

    function start() {
      clearInterval(timer);
      timer = setInterval(() => show(index + 1), 3000);
    }

    document.getElementById("sliderPrev")?.addEventListener("click", () => {
      show(index - 1);
      start();
    });
    document.getElementById("sliderNext")?.addEventListener("click", () => {
      show(index + 1);
      start();
    });
    show(0);
    start();
  }

  function initDateMask() {
    const input = document.querySelector('input[name="start_date"]');
    if (!input || input.type === "date") return;
    input.addEventListener("input", () => {
      let value = input.value.replace(/\D/g, "").slice(0, 8);
      if (value.length > 4) value = `${value.slice(0, 2)}.${value.slice(2, 4)}.${value.slice(4)}`;
      else if (value.length > 2) value = `${value.slice(0, 2)}.${value.slice(2)}`;
      input.value = value;
    });
  }

  function initAdminStatus() {
    document.querySelectorAll("[data-status-select]").forEach((select) => {
      select.dataset.previous = select.value;
      select.addEventListener("change", () => {
        const ok = window.confirm(`Изменить статус заявки на "${select.value}"?`);
        if (!ok) {
          select.value = select.dataset.previous;
          return;
        }
        select.form.submit();
      });
    });
  }

  function hideToasts() {
    setTimeout(() => {
      document.querySelectorAll(".toast.show").forEach((toast) => toast.classList.remove("show"));
    }, 2600);
  }

  document.addEventListener("DOMContentLoaded", () => {
    initSlider();
    initDateMask();
    initAdminStatus();
    hideToasts();
  });
})();
