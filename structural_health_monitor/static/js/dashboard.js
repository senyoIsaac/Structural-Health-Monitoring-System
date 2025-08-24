document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts for each structure
    document.querySelectorAll('.structure-chart').forEach(chartElement => {
        const structureId = chartElement.dataset.structureId;
        initializeStructureChart(structureId);
    });
    
    // Refresh data every 30 seconds
    setInterval(refreshAllCharts, 30000);
});

function initializeStructureChart(structureId) {
    const ctx = document.getElementById(`chart-${structureId}`).getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: { datasets: [] },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'hour'
                    }
                },
                y: {
                    beginAtZero: false
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
    
    // Store chart reference
    window.structureCharts = window.structureCharts || {};
    window.structureCharts[structureId] = chart;
    
    // Load initial data
    updateChartData(structureId);
}

function updateChartData(structureId) {
    fetch(`/api/data/${structureId}/`)
        .then(response => response.json())
        .then(data => {
            const chart = window.structureCharts[structureId];
            chart.data.datasets = data.datasets;
            chart.update();
        });
}

function refreshAllCharts() {
    Object.keys(window.structureCharts || {}).forEach(structureId => {
        updateChartData(structureId);
    });
    
    // Optionally refresh event log
    fetch('/api/events/')
        .then(response => response.json())
        .then(events => {
            // Update event log UI
        });
}