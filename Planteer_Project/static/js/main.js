document.addEventListener("DOMContentLoaded", function () {

    const currentPath = window.location.pathname;

    document.querySelectorAll(".navbar .nav-link").forEach(link => {

        if (link.pathname === currentPath) {

            link.classList.add("active");
            link.setAttribute("aria-current", "page");

        }

    });

});