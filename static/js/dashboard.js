const setActiveFromLocation = () => {
    const path = window.location.pathname.replace(/\/+$/,'');
    document.querySelectorAll('.side-item').forEach(i => i.classList.remove('active'));
    document.querySelectorAll('.side-item').forEach(i => {
        try {
            const hrefPath = new URL(i.getAttribute('href'), window.location.origin).pathname.replace(/\/+$/,'');
            if (hrefPath === path) i.classList.add('active');
        } catch(e){}
    });
};

// Set on load
setActiveFromLocation();

// Update after HTMX swaps
document.body.addEventListener('htmx:afterSwap', setActiveFromLocation);

// Update on back/forward
window.addEventListener('popstate', setActiveFromLocation);

document.addEventListener("DOMContentLoaded", () => {
    const fa_bars = document.querySelector(".fa-bars");
    const sideBar = document.querySelector(".side-bar-items");

    fa_bars.addEventListener("click", () => {
        fa_bars.classList.toggle("active");
        sideBar.classList.toggle("active");
    });
});