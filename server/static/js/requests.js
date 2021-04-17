function makeRequest(resource, callback) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            callback(xhttp.responseText);
        }
    };

    xhttp.open("POST", `http://127.0.0.1:6969/${resource}`, true);
    xhttp.send();
}

function startCamera() {
    makeRequest("start-camera", (response) => {
        document.getElementById("status").innerHTML = response;
    });
}


function stopCamera() {
    makeRequest("stop-camera", (response) => {
        document.getElementById("status").innerHTML = response;
    });
}

