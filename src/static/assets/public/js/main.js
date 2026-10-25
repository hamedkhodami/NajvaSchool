document.addEventListener("DOMContentLoaded", () => {
    // منوی موبایل
    const menuButton = document.getElementById("mobileMenuBtn");
    const mobileMenu = document.getElementById("mobileMenu");
    const openIcon = document.getElementById("mobileMenuOpenIcon");
    const closeIcon = document.getElementById("mobileMenuCloseIcon");

    if (menuButton && mobileMenu) {
        const closeMenu = () => {
            mobileMenu.classList.add("hidden");
            menuButton.setAttribute("aria-expanded", "false");
            menuButton.setAttribute("aria-label", "باز کردن منو");

            openIcon?.classList.remove("hidden");
            closeIcon?.classList.add("hidden");
        };

        const toggleMenu = () => {
            const isOpen = !mobileMenu.classList.contains("hidden");

            if (isOpen) {
                closeMenu();
            } else {
                mobileMenu.classList.remove("hidden");
                menuButton.setAttribute("aria-expanded", "true");
                menuButton.setAttribute("aria-label", "بستن منو");

                openIcon?.classList.add("hidden");
                closeIcon?.classList.remove("hidden");
            }
        };

        menuButton.addEventListener("click", toggleMenu);

        mobileMenu.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", closeMenu);
        });

        document.addEventListener("click", (event) => {
            if (
                !mobileMenu.contains(event.target) &&
                !menuButton.contains(event.target)
            ) {
                closeMenu();
            }
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                closeMenu();
            }
        });

        window.addEventListener("resize", () => {
            if (window.innerWidth >= 768) {
                closeMenu();
            }
        });
    }

    // نمایش تدریجی بخش‌ها هنگام اسکرول
    const revealElements = document.querySelectorAll("[data-reveal]");

    const prefersReducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    if ("IntersectionObserver" in window && !prefersReducedMotion) {
        revealElements.forEach((element) => {
            element.style.opacity = "0";
            element.style.transform = "translateY(18px)";
            element.style.transition =
                "opacity 600ms ease, transform 600ms ease";
        });

        const observer = new IntersectionObserver(
            (entries, currentObserver) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = "1";
                        entry.target.style.transform = "translateY(0)";
                        currentObserver.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.12 }
        );

        revealElements.forEach((element) => observer.observe(element));
    }

    // بازگشت به بالای صفحه
    const backToTop = document.getElementById("backToTop");

    if (backToTop) {
        const updateBackToTop = () => {
            if (window.scrollY > 450) {
                backToTop.classList.remove("hidden");
                backToTop.classList.add("flex");
            } else {
                backToTop.classList.add("hidden");
                backToTop.classList.remove("flex");
            }
        };

        window.addEventListener("scroll", updateBackToTop, {
            passive: true,
        });

        updateBackToTop();

        backToTop.addEventListener("click", () => {
            window.scrollTo({
                top: 0,
                behavior: prefersReducedMotion ? "auto" : "smooth",
            });
        });
    }
});
