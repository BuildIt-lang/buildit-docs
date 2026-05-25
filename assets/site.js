(function () {
  const input = document.querySelector(".search input");
  const links = Array.from(document.querySelectorAll(".side-nav a"));
  const groups = Array.from(document.querySelectorAll(".side-nav .nav-group"));
  let searchEntries = new Map();

  if (!input || links.length === 0) {
    return;
  }

  function normalizeUrl(url) {
    return new URL(url, document.baseURI).href;
  }

  function makeFallbackEntry(link) {
    return {
      text: (link.dataset.search || link.textContent).toLowerCase(),
    };
  }

  function entryMatches(link, query) {
    const entry = searchEntries.get(normalizeUrl(link.getAttribute("href"))) || makeFallbackEntry(link);
    return entry.text.includes(query);
  }

  groups.forEach(function (group) {
    group.dataset.defaultOpen = group.open ? "true" : "false";
  });

  function runSearch() {
    const query = input.value.trim().toLowerCase();
    const searching = query !== "";

    links.forEach(function (link) {
      const item = link.closest("li");
      if (!item) {
        return;
      }
      item.hidden = searching && !entryMatches(link, query);
    });

    groups.forEach(function (group) {
      if (!searching) {
        group.open = group.dataset.defaultOpen === "true";
        group.hidden = false;
        return;
      }

      const hasVisibleLink = Array.from(group.querySelectorAll("li")).some(function (item) {
        return !item.hidden;
      });
      group.open = hasVisibleLink;
      group.hidden = !hasVisibleLink;
    });
  }

  input.addEventListener("input", runSearch);

  const indexUrl = input.dataset.searchIndex;
  if (indexUrl) {
    fetch(indexUrl)
      .then(function (response) {
        if (!response.ok) {
          throw new Error("search index request failed");
        }
        return response.json();
      })
      .then(function (entries) {
        const indexRoot = new URL("..", new URL(indexUrl, document.baseURI));
        searchEntries = new Map(
          entries.map(function (entry) {
            const text = [
              entry.title,
              entry.kind,
              entry.namespace,
              entry.header,
              ...(entry.keywords || []),
            ].join(" ").toLowerCase();
            return [new URL(entry.url, indexRoot).href, { text: text }];
          })
        );
        runSearch();
      })
      .catch(function () {
        searchEntries = new Map();
      });
  }
})();
