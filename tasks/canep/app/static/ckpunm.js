const onScroll = e => {
    let maxHeight = document.documentElement.scrollHeight - window.innerHeight;
    let maxWidth = document.documentElement.scrollWidth - window.innerWidth;
    let scrollX = Math.max(0, Math.min(1, window.scrollX / maxWidth));
    let scrollY = Math.max(0, Math.min(1, window.scrollY / maxHeight));

    let layers = document.querySelectorAll(".layer");
    let threshold = Math.floor((1 - scrollY) * layers.length);
    layers.forEach(layer => {
        let id = parseInt(layer.id.match(/\d+/));
        if (id > threshold) { 
            layer.classList.add("inactive");
        } else {
            layer.classList.remove("inactive");
        }
    });

    document.getElementById("inner-wrapper").style.transform = `translateZ(${(scrollY - 0.5) * 45}px) rotateY(${(scrollX - 0.5) * 20}deg)`;
};


document.addEventListener("scroll", onScroll);
onScroll();


const socket = new WebSocket(`${window.location.href.replace('http', 'ws')}/ws`);

const err = (text, win) => {
    let errorElement = document.getElementById("error");
    if (errorElement.classList.contains("error")) {
        return;
    }
    document.getElementById("game").classList.add("game-over");
    errorElement.className = "error";
    if (win) {
        errorElement.className = "error win";
    }
    errorElement.innerText = text;
};

const onClose = e => {
    err("Hem coeg.");
};

const onError = e => {
    err("He cygb6a");
};

let elements = []; // [z][y][x]

const onMessage = e => {
    let data;
    try {
        data = JSON.parse(e.data);
    } catch (_) {
        err("Invalid data received from server");
        return;
    }

    if (data.error) {
        err(data.error);
        return;
    }

    if (data.start) {
        let wrapperElement = document.getElementById("inner-wrapper");
        for (let z = 0; z < data.z; ++z) {
            let layer = [];
            let layerElement = document.createElement("div");
            layerElement.className = "layer";
            layerElement.id = `layer-${z}`;
            layerElement.style.transform = `translateZ(${z * 4}px)`;
            for (let y = 0; y < data.y; ++y) {
                let row = [];
                let rowElement = document.createElement("div");
                rowElement.className = "row";
                for (let x = 0; x < data.x; ++x) {
                    let cell = document.createElement("a");
                    cell.className = "cell hoverable";
                    cell.href = "#";
                    cell.onclick = e => {
                        e.preventDefault();

                        socket.send(JSON.stringify({"event": "click", "x": x, "y": y, "z": z}));
                    }
                    cell.oncontextmenu = e => {
                        e.preventDefault();

                        socket.send(JSON.stringify({"event": "flag", "x": x, "y": y, "z": z}));
                        return false;
                    }
                    let subcell = document.createElement("span");
                    subcell.className = "cell-inner";
                    cell.appendChild(subcell);
                    row.push(cell);
                    rowElement.appendChild(cell);
                }
                layer.push(row);
                layerElement.appendChild(rowElement);
            }
            elements.push(layer);
            wrapperElement.appendChild(layerElement);
        }
        onScroll();
    } else if (data.update) {
        data.update.forEach(upd => {
            let el = elements[upd.z][upd.y][upd.x];
            if (upd.state == "open") {
                el.classList.add("open");
                el.classList.remove("hoverable");
                el.classList.add(`open-${upd.count}`);
                if (upd.count > 0) {
                    el.childNodes[0].innerHTML = `${upd.count}`;
                }
            } else if (upd.state == "bomb") {
                el.classList.add("bomb");
                el.classList.remove("hoverable");
                // el.childNodes[0].innerHTML = "💥";
            } else if (upd.state == "flag") {
                el.classList.add("flag");
                el.classList.remove("hoverable");
                // el.childNodes[0].innerHTML = "🚩";
            } else if (upd.state == "noflag") {
                el.classList.remove("flag");
                el.classList.add("hoverable");
                el.childNodes[0].innerHTML = "";
            }
        });
    } else if (data.win) {
        err("Oro u ypa — no6ega!", true);
    }
};

socket.onclose = onClose;
socket.onerror = onError;
socket.onmessage = onMessage;
