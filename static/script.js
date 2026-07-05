// =============================
// EduGenie Common JavaScript
// =============================

// Smooth scroll to top
window.addEventListener("load", () => {
    window.scrollTo(0, 0);
});

// Highlight active navigation link
document.addEventListener("DOMContentLoaded", () => {

    const current = window.location.pathname;

    document.querySelectorAll(".nav-links a").forEach(link => {

        if (link.getAttribute("href") === current) {
            link.classList.add("active");
        }

    });

});

// Future common functions can be added here.