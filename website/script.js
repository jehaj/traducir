function createBox(post) {
    let box = document.createElement("div");
    box.className = "box";
    let term = document.createElement("p");
    term.textContent = post[0];
    box.appendChild(term);
    let begreb = document.createElement("p");
    begreb.textContent = post[1];
    box.appendChild(begreb);
    let kilde = document.createElement("p");
    kilde.textContent = post[2];
    box.appendChild(kilde);
    let id = document.createElement("p");
    id.textContent = post[3];
    box.appendChild(id);

    return box;
}

const inputSearch = document.querySelector("#search-field");
const boxesDiv = document.querySelector("#boxes")

let timer;

inputSearch.addEventListener("input", () => {
    boxesDiv.innerHTML = "";
    clearTimeout(timer);
    const ms = 250;
    timer = setTimeout(() => {
        let value = inputSearch.value;
        if (value.length > 1) {
            fetch("/api", {
                method: "POST",
                body: value
            }).then(res => res.json())
              .then(posts => {
                if (posts.length == 0) {
                    let p = document.createElement("p");
                    p.textContent = "Intet resultat.";
                    boxesDiv.appendChild(p);
                }

                for (let i = 0; i < posts.length; i++) {
                    const post = posts[i];
                    box = createBox(post);     
                    boxesDiv.appendChild(box);               
                }
            });
        }
    }, ms);
});
