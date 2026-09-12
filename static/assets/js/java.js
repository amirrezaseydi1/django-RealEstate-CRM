/* ===============================
   Base JavaScript for CRM
   Used in _base.html
================================ */

document.addEventListener("DOMContentLoaded", function () {

    /* ===============================
       Active Navbar Link
    ================================ */
    const navLinks = document.querySelectorAll(".nav-links a");
    const currentPath = window.location.pathname;

    navLinks.forEach(link => {
        if (link.getAttribute("href") === currentPath) {
            link.classList.add("active");
        }
    });

    /* ===============================
       Basic Button Feedback (UX)
    ================================ */
    const buttons = document.querySelectorAll("button, .btn-signup a");

    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            btn.classList.add("clicked");

            setTimeout(() => {
                btn.classList.remove("clicked");
            }, 150);
        });
    });

});

