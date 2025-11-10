document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.querySelector(".hamburger");
  const navbarUl = document.querySelector(".navbars");

  hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navbarUl.classList.toggle("active");
  });
});
