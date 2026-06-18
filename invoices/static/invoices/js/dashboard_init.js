$(document).ready(function() {
    console.log("Smart Blue Fusion Dashboard Initialized.");
    
    // Vendor initializations like Chart.js
    var ctx = document.getElementById('perfOverviewChart');
    var chartDataEl = document.getElementById('chart-data');
    if (ctx && chartDataEl) {
        try {
            var rawData = JSON.parse(chartDataEl.textContent);
            new Chart(ctx.getContext('2d'), {
                type: 'line',
                data: {
                    labels: rawData.labels.length ? rawData.labels : ['No Data'],
                    datasets: [{
                        label: 'Revenue (PKR)',
                        data: rawData.revenue.length ? rawData.revenue : [0],
                        borderColor: '#0057D9',
                        backgroundColor: 'rgba(0, 87, 217, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }, {
                        label: 'Invoices Count',
                        data: rawData.invoices.length ? rawData.invoices : [0],
                        borderColor: '#00C6FF',
                        backgroundColor: 'transparent',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        fill: false,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        } catch(e) {
            console.error("Failed to parse chart data", e);
        }
    }
});
