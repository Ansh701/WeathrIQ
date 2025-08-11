document.addEventListener('DOMContentLoaded', () => {
    initChart();
    initMagicMouse();
    updateDynamicBackground();
});

function initChart() {
    if (typeof forecastData !== 'undefined' && document.getElementById('forecastChart')) {
        const ctx = document.getElementById('forecastChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: forecastData.labels,
                datasets: [{
                    label: 'Temperature (°C)', data: forecastData.temps, borderColor: 'rgba(255, 159, 64, 1)', backgroundColor: 'rgba(255, 159, 64, 0.2)', yAxisID: 'y', tension: 0.3, fill: true
                }, {
                    label: 'Humidity (%)', data: forecastData.hums, borderColor: 'rgba(54, 162, 235, 1)', backgroundColor: 'rgba(54, 162, 235, 0.2)', yAxisID: 'y1', tension: 0.3, fill: true
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false }, stacked: false,
                plugins: { legend: { labels: { color: 'white', font: { size: 14 } } } },
                scales: {
                    x: { ticks: { color: 'rgba(255, 255, 255, 0.8)' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
                    y: { type: 'linear', display: true, position: 'left', ticks: { color: 'rgba(255, 159, 64, 1)', callback: (v) => v + '°C' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
                    y1: { type: 'linear', display: true, position: 'right', ticks: { color: 'rgba(54, 162, 235, 1)', callback: (v) => v + '%' }, grid: { drawOnChartArea: false } }
                }
            }
        });
    }
}

function initMagicMouse() {
    const spotlight = document.getElementById('mouse-spotlight');
    if (!spotlight) return;
    window.addEventListener('mousemove', e => {
        spotlight.style.left = e.clientX + 'px';
        spotlight.style.top = e.clientY + 'px';
    });
    document.querySelectorAll('.forecast-item, .search-button, .geo-input').forEach(elem => {
        elem.addEventListener('mouseenter', () => {
            spotlight.style.width = '500px';
            spotlight.style.height = '500px';
            spotlight.style.background = 'radial-gradient(circle, rgba(255, 150, 0, 0.2), transparent 70%)';
        });
        elem.addEventListener('mouseleave', () => {
            spotlight.style.width = '400px';
            spotlight.style.height = '400px';
            spotlight.style.background = 'radial-gradient(circle, rgba(40, 90, 200, 0.2), transparent 70%)';
        });
    });
}

function updateDynamicBackground() {
    const card = document.getElementById('weather-card');
    const bg1 = document.getElementById('bg-image-1');
    const bg2 = document.getElementById('bg-image-2');
    if (!card || !bg1 || !bg2) return;
    const description = card.dataset.description;
    const imageMap = { 'thunder': 'thunder.jpeg', 'rain': 'rain.jpeg', 'drizzle': 'drizzle.jpeg', 'snow': 'snow.jpeg', 'sleet': 'sleet.jpeg', 'blizzard': 'blizzard.jpeg', 'mist': 'mist.jpeg', 'fog': 'fog.jpeg', 'haze': 'mist.jpeg', 'smoke': 'mist.jpeg', 'ice': 'ice.jpeg', 'cloud': 'cloudy.jpeg', 'overcast': 'overcast.jpeg', 'sun': 'sunny.jpeg', 'clear': 'clear.jpeg' };
    let imageName = 'clear.jpeg';
    for (const key in imageMap) {
        if (description.includes(key)) {
            imageName = imageMap[key];
            break;
        }
    }
    const newImageUrl = `url(/static/img/${imageName})`;
    if (bg1.style.opacity === '1' || bg1.style.opacity === '') {
        bg2.style.backgroundImage = newImageUrl;
        bg1.style.opacity = '0';
        bg2.style.opacity = '1';
    } else {
        bg1.style.backgroundImage = newImageUrl;
        bg2.style.opacity = '0';
        bg1.style.opacity = '1';
    }
}