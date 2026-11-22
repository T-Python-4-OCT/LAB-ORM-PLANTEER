document.addEventListener("DOMContentLoaded", function () {

    const currentPath = window.location.pathname;

    const navLinks = document.querySelectorAll(
        ".navbar a[href]"
    );

    navLinks.forEach(link => {

        if (link.pathname === currentPath) {

            link.classList.add("active");

            link.setAttribute(
                "aria-current",
                "page"
            );

        }

    });

});