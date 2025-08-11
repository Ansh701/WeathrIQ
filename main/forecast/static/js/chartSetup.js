document.addEventListener('DOMContentLoaded', () => {
    // Check if the forecastData object and the canvas element exist
    if (typeof forecastData !== 'undefined' && document.getElementById('forecastChart')) {
        const ctx = document.getElementById('forecastChart').getContext('2d');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: forecastData.labels,
                datasets: [
                    {
                        label: 'Temperature (°C)',
                        data: forecastData.temps,
                        borderColor: 'rgba(255, 159, 64, 1)',
                        backgroundColor: 'rgba(255, 159, 64, 0.2)',
                        yAxisID: 'y', // Assign to the first Y-axis
                        tension: 0.3,
                        fill: true
                    },
                    {
                        label: 'Humidity (%)',
                        data: forecastData.hums,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        yAxisID: 'y1', // Assign to the second Y-axis
                        tension: 0.3,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                stacked: false,
                plugins: {
                    tooltip: {
                        titleFont: { size: 14 },
                        bodyFont: { size: 12 },
                        footerFont: { size: 10 }
                    },
                    legend: {
                        labels: {
                            color: 'white', // Legend text color
                            font: {
                                size: 14
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.8)', // X-axis labels color
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)' // X-axis grid lines color
                        }
                    },
                    y: { // First Y-axis (Temperature)
                        type: 'linear',
                        display: true,
                        position: 'left',
                        ticks: {
                            color: 'rgba(255, 159, 64, 1)',
                            callback: function(value) {
                                return value + '°C';
                            }
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    y1: { // Second Y-axis (Humidity)
                        type: 'linear',
                        display: true,
                        position: 'right',
                        ticks: {
                            color: 'rgba(54, 162, 235, 1)',
                            callback: function(value) {
                                return value + '%';
                            }
                        },
                        grid: {
                            drawOnChartArea: false, // only draw grid for first Y-axis
                        },
                    }
                }
            },
        });
    }
});