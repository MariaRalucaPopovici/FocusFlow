const searchInput = document.getElementById("task-search");
const listDiv = document.getElementById("task-list");

searchInput.addEventListener("input", function () {
    fetch(searchInput.dataset.searchUrl + "?q=" + encodeURIComponent(searchInput.value))
        .then((response) => response.text())
        .then((html) => {
            listDiv.innerHTML = html;
        });
});