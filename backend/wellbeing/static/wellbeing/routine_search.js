const searchInput = document.getElementById("routine-search");
const listDiv = document.getElementById("routine-list");

searchInput.addEventListener("input", function () {
    fetch(searchInput.dataset.searchUrl + "?q=" + encodeURIComponent(searchInput.value))
        .then((response) => response.text())
        .then((html) => {
            listDiv.innerHTML = html;
        });
});