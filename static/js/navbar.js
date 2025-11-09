const hamburger = document.querySelector(".hamburger");

document.addEventListener("DOMContentLoaded", () => {
    // Hamburger
  hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
  });
});
