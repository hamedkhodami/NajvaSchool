document.addEventListener("DOMContentLoaded", () => {
    // پیام‌های Django
    const messageContainer = document.getElementById("dashboardMessages");

    if (messageContainer) {
        messageContainer.querySelectorAll("[data-dashboard-message]").forEach((message) => {
            let removed = false;
            let timer;

            const dismiss = () => {
                if (removed) return;
                removed = true;

                window.clearTimeout(timer);
                message.classList.add("is-leaving");

                window.setTimeout(() => {
                    message.remove();

                    if (messageContainer.isConnected &&
                        messageContainer.children.length === 0) {
                        messageContainer.remove();
                    }
                }, 260);
            };

            message.querySelector("[data-dismiss-message]")
                ?.addEventListener("click", dismiss);

            timer = window.setTimeout(dismiss, 5000);
        });
    }

    // تعامل ظریف کارت‌ها با صفحه‌کلید و اشاره‌گر
    document.querySelectorAll(".dashboard-card").forEach((card) => {
        card.addEventListener("pointerdown", () => {
            card.classList.add("scale-[0.99]");
        });

        const releaseCard = () => {
            card.classList.remove("scale-[0.99]");
        };

        card.addEventListener("pointerup", releaseCard);
        card.addEventListener("pointercancel", releaseCard);
        card.addEventListener("pointerleave", releaseCard);
    });
});
