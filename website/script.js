const inputSearch = document.querySelector("#search-field");
const boxDiv = document.querySelector("#box");

let timer;
inputSearch.addEventListener("input", () => {
    clearTimeout(timer);
    const ms = 250;
    timer = setTimeout(() => {
        let value = inputSearch.value;
        if (value.length > 1) {
            fetch("/api", {
                method: "POST",
                body: value
            }).then(res => res.json())
              .then(data => {
                let posts = data.posts;
                for (let post in posts) {

                }
            });
        }
    }, ms);
});
