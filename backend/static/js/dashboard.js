document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".task-tick").forEach(function (tick) {
        tick.addEventListener("click", function (event) {
            event.preventDefault();
            const row = tick.closest(".dashboard-task-row");
            const taskId = row.dataset.taskId;

            fetch(tick.href).then(function (response) {
                if (response.ok) {
                    document.querySelectorAll('.dashboard-task-row[data-task-id="' + taskId + '"]').forEach(function (matchingRow) {
                        matchingRow.style.transition = "opacity 0.3s ease";
                        matchingRow.style.opacity = "0";
                        setTimeout(function () {
                            matchingRow.remove();
                        }, 300);
                    });
                }
            });
        });
    });
});