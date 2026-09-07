document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".task-tick").forEach(function (tick) {
        tick.addEventListener("click", function (event) {
            event.preventDefault();
            const row = tick.closest(".dashboard-task-row");

            fetch(tick.href).then(function (response) {
                if (response.ok) {
                    row.style.transition = "opacity 0.3s ease";
                    row.style.opacity = "0";
                    setTimeout(function () {
                        row.remove();
                    }, 300);
                }
            });
        });
    });
});