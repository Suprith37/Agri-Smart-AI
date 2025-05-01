const inputBox = document.querySelector('.input-box');
const searchBtn = document.getElementById('searchBtn');
const weather_img = document.getElementById('weather-img');

const temperature = document.querySelector('.temperature');
const description = document.querySelector('.description');
const humidity = document.getElementById('humidity');
const wind_speed = document.getElementById('wind-speed');

const location_not_found = document.querySelector('.location-not-found');

const weather_body = document.querySelector('.weather-body');


// const api_key = "4c4286de4f6a3794841e570fd8bc4a0b";
async function checkWeather(city){
    const api_key = "4c4286de4f6a3794841e570fd8bc4a0b";
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${api_key}`;

    const weather_data = await fetch(`${url}`).then(response => response.json());


    if(weather_data.cod === `404`){
        location_not_found.style.display = "flex";
        weather_body.style.display = "none";
        console.log("error");
        return;
    }

    console.log("run");
    location_not_found.style.display = "none";
    weather_body.style.display = "flex";
    temperature.innerHTML = `${Math.round(weather_data.main.temp - 273.15)}°C`;
    description.innerHTML = `${weather_data.weather[0].description}`;

    humidity.innerHTML = `${weather_data.main.humidity}%`;
    wind_speed.innerHTML = `${weather_data.wind.speed}Km/H`;


    console.log("status "+ weather_data.weather[0].main);
    switch (weather_data.weather[0].main) {
        case 'Clouds':
            weather_img.src = weather_img.dataset.cloud;
            break;
        case 'Clear':
            weather_img.src = weather_img.dataset.clear;
            break;
        case 'Rain':
            weather_img.src = weather_img.dataset.rain;
            break;
        case 'Haze':
            weather_img.src = weather_img.dataset.haze;
            break;
        case 'Lightning':
            weather_img.src = weather_img.dataset.lightning;
            break;
        case 'Snow':
            weather_img.src = weather_img.dataset.snow;
            break;
        case 'Storm':
            weather_img.src = weather_img.dataset.storm;
            break;
        case 'Thunderstorm':
            weather_img.src = weather_img.dataset.thunderstorm;
            break;
        case 'Mist':
            weather_img.src = weather_img.dataset.mist;
            break;
        default:
            console.error('Unknown weather condition:', weather_data.weather[0].main);
    }
    
    console.log(weather_data);
}


// searchBtn.addEventListener('click', ()=>{
//     console.log("search clicked");
//     checkWeather(inputBox.value);
// });

searchBtn.addEventListener('click', () => {
    console.log("Search button clicked");
    const city = inputBox.value.trim();
    if (city) {
        checkWeather(city);
    } else {
        alert("Please enter a location!");
    }
});
