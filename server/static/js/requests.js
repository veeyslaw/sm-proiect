function makeRequest(address, resource, callback) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            callback(xhttp.responseText);
        }
    };

    xhttp.open("POST", `http://${address}/${resource}`, true);
    xhttp.send();
}

function startCamera(address) {
    makeRequest(address, "start-camera", (response) => {
        document.getElementById("status").innerHTML = response;
    });
}


function stopCamera(address) {
    makeRequest(address, "stop-camera", (response) => {
        document.getElementById("status").innerHTML = response;
    });
}

