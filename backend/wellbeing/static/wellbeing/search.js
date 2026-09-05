const searchInput = document.getElementById("strategy-search");
const listDiv = document.getElementById("strategy-list");

searchInput.addEventListener("input", function () {
    fetch(searchInput.dataset.searchUrl + "?q=" + encodeURIComponent(searchInput.value))
        .then((response) => response.text())
        .then((html) => {
            listDiv.innerHTML = html;
        });
});