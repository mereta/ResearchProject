function fetchJSON(url, responseObjectHandler) {
    let req = new XMLHttpRequest();

    req.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(JSON.parse(this.responseText));
            responseObjectHandler(JSON.parse(this.responseText));
        }
    }
    console.log("Fetching remote: ", url);
    req.open("GET", url);
    req.send();
}

function iconSrc(iconName) {
    return "http://openweathermap.org/img/w/" + iconName + ".png";
}

function displayWeather(responseJson) {
    let div = document.getElementById("currentWeather");
    div.innerHTML = "<h3><b>Current Weather</b></h3>";

    let img = document.createElement("img");
    img.src = iconSrc(responseJson.weather[0].icon);
    img.id = "weatherIcon";
    div.appendChild(img);

    div.innerHTML += "<br><b>Condition:  </b>" + responseJson.weather[0].description + "<br><br>";
    div.innerHTML += "<b>Temperature:  </b>" + responseJson.main.temp + " °C <br>";
    div.innerHTML += "<b>Wind Speed:  </b>" + responseJson.wind.speed + " m/s <br>";
    div.innerHTML += "<b>Humidity:  </b>" + responseJson.main.humidity + " %<br>";
}

window.onload = function () {
    const LOCATION = "dublin,ie";
    const API_KEY  = "e672a6c63b5d5f7fe474b254a407a52c";
    const BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q=";
    const UNITS = "metric";
    let url = BASE_URL + LOCATION + "&units=" + UNITS + "&appid=" + API_KEY;
    fetchJSON(url, displayWeather);
}
