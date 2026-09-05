
const searchInput = document.getElementById("strategy-search");
const listDiv = document.getElementById("strategy-list");

searchInput.addEventListener("input", function () {
    const url = searchInput.dataset.searchUrl + "?q=" + encodeURIComponent(searchInput.value);

    fetch(url)
        .then(response => response.json())
        .then(data => {
            listDiv.innerHTML = "";

            if (data.strategies.length === 0) {
                listDiv.innerHTML = "<p>No strategies match your search.</p>";
                return;
            }

            data.strategies.forEach(s => {
                const card = document.createElement("article");
                card.className = "strategy-card";

                const title = document.createElement("h3");
                title.textContent = s.title;

                const meta = document.createElement("p");
                meta.className = "strategy-meta";
                meta.textContent = s.meta;

                const desc = document.createElement("p");
                desc.textContent = s.description;

                card.append(title, meta, desc);

                if (s.resource_url) {
                    const link = document.createElement("a");
                    link.href = s.resource_url;
                    link.target = "_blank";
                    link.rel = "noopener";
                    link.textContent = "Watch / read more";
                    const linkP = document.createElement("p");
                    linkP.append(link);
                    card.append(linkP);
                }

                listDiv.append(card);
            });
        });
});
