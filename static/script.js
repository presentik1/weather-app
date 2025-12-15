async function getWeather() {
    const city = document.getElementById("cityInput").value.trim();
    if (!city) {
        alert("Введите город!");
        return;
    }

    const response = await fetch(`/weather?city=${encodeURIComponent(city)}`);
    const data = await response.json();

    const result = document.getElementById("result");

    if (data.error) {
        result.classList.add("visible");
        result.innerHTML = `<p style="color:red;"><b>Ошибка:</b> ${data.error}</p>`;
        return;
    }

    document.getElementById("cityName").innerText = data.city;
    document.getElementById("temp").innerText = data.temperature;
    document.getElementById("feels").innerText = data.feels_like;
    document.getElementById("humidity").innerText = data.humidity;
    document.getElementById("desc").innerText = data.description;

    result.classList.add("visible");
}
