document.addEventListener("DOMContentLoaded", function () {
    const tipCard = document.getElementById("daily-tip");
    if (!tipCard) {
        return;
    }

    const today = new Date().toISOString().slice(0, 10);
    const dismissedDate = localStorage.getItem("focusflow-tip-dismissed");

    if (dismissedDate === today) {
        tipCard.style.display = "none";
        return;
    }

    const closeButton = document.getElementById("daily-tip-close");
    closeButton.addEventListener("click", function () {
        tipCard.style.display = "none";
        localStorage.setItem("focusflow-tip-dismissed", today);
    });
});