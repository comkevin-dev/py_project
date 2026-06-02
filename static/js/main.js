const WEATHER_ICONS = {
    'Sunny': '☀️',
    'Clear': '🌙',
    'Partly cloudy': '⛅',
    'Cloudy': '☁️',
    'Overcast': '☁️',
    'Mist': '🌫️',
    'Fog': '🌫️',
    'Light rain': '🌦️',
    'Moderate rain': '🌧️',
    'Heavy rain': '🌧️',
    'Light snow': '🌨️',
    'Moderate snow': '❄️',
    'Heavy snow': '❄️',
    'Thunderstorm': '⛈️',
    'Blizzard': '🌨️',
};

function getIcon(desc) {
    for (const [key, icon] of Object.entries(WEATHER_ICONS)) {
        if (desc.toLowerCase().includes(key.toLowerCase())) return icon;
    }
    return '🌡️';
}

async function fetchWeather(city = 'Seoul') {
    try {
        const res = await fetch(`/api/weather?city=${city}`);
        const data = await res.json();

        if (data.error) throw new Error(data.error);

        document.getElementById('weather-icon').textContent = getIcon(data.desc);
        document.getElementById('weather-temp').textContent = `${data.temp_c}°C`;
        document.getElementById('weather-desc').textContent = data.desc;
        document.getElementById('weather-widget').title =
            `체감 ${data.feels_like}°C · 습도 ${data.humidity}%`;
    } catch {
        document.getElementById('weather-desc').textContent = '날씨 정보 없음';
    }
}

document.addEventListener('DOMContentLoaded', () => fetchWeather('Seoul'));
