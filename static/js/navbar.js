document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.querySelector(".hamburger");
  const navbarUl = document.querySelector(".navbars");
  const formErrors = document.querySelectorAll(".error-messages");

  // Hamburger toggle
  hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navbarUl.classList.toggle("active");
  });

  // Remove form errors after 3 seconds
  if (formErrors.length > 0) {
    setTimeout(() => {
      formErrors.forEach((el) => el.remove());
    }, 5000);
  }
  
  document.body.addEventListener("htmx:configRequest", (event) => {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value;
    if (csrfToken) {
      event.detail.headers["X-CSRFToken"] = csrfToken;
    }
  });
});
