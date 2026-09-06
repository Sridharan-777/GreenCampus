// GreenCampus - Interactive Sustainability Dashboard Charts (Chart.js)

document.addEventListener('DOMContentLoaded', async () => {
  const categoryCanvas = document.getElementById('categoryChart');
  const trendCanvas = document.getElementById('trendChart');
  const hotspotCanvas = document.getElementById('hotspotChart');
  const statusCanvas = document.getElementById('statusChart');

  if (!categoryCanvas && !trendCanvas && !hotspotCanvas && !statusCanvas) {
    return; // Not on dashboard page
  }

  try {
    const response = await fetch('/analytics/api/chart-data/');
    const data = await response.json();

    // Chart.js Global Config
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";

    // 1. Waste Category Breakdown (Doughnut)
    if (categoryCanvas) {
      new Chart(categoryCanvas, {
        type: 'doughnut',
        data: {
          labels: data.categories.labels,
          datasets: [{
            data: data.categories.data,
            backgroundColor: data.categories.colors,
            borderWidth: 2,
            borderColor: '#111e21',
            hoverOffset: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: { boxWidth: 12, padding: 15, color: '#f1f5f9' }
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return ` ${context.label}: ${context.raw} kg`;
                }
              }
            }
          },
          cutout: '68%'
        }
      });
    }

    // 2. Monthly Trend (Cleaned vs Reported)
    if (trendCanvas) {
      new Chart(trendCanvas, {
        type: 'line',
        data: {
          labels: data.trends.labels,
          datasets: [
            {
              label: 'Reported Waste (kg)',
              data: data.trends.reported,
              borderColor: '#f59e0b',
              backgroundColor: 'rgba(245, 158, 11, 0.1)',
              tension: 0.4,
              fill: true,
              borderWidth: 2,
              pointRadius: 4,
            },
            {
              label: 'Recycled / Cleaned (kg)',
              data: data.trends.recycled,
              borderColor: '#10b981',
              backgroundColor: 'rgba(16, 185, 129, 0.15)',
              tension: 0.4,
              fill: true,
              borderWidth: 2,
              pointRadius: 4,
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              labels: { color: '#f1f5f9', boxWidth: 12 }
            }
          },
          scales: {
            x: { grid: { color: 'rgba(255, 255, 255, 0.05)' } },
            y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, title: { display: true, text: 'Weight (kg)', color: '#94a3b8' } }
          }
        }
      });
    }

    // 3. Hotspot Campus Locations (Bar Chart)
    if (hotspotCanvas) {
      new Chart(hotspotCanvas, {
        type: 'bar',
        data: {
          labels: data.hotspots.labels,
          datasets: [{
            label: 'Incidents Reported',
            data: data.hotspots.data,
            backgroundColor: 'rgba(6, 182, 212, 0.75)',
            borderColor: '#06b6d4',
            borderWidth: 1,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            x: { grid: { display: false } },
            y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, beginAtZero: true, ticks: { precision: 0 } }
          }
        }
      });
    }

    // 4. Status Breakdown (Pie)
    if (statusCanvas) {
      new Chart(statusCanvas, {
        type: 'pie',
        data: {
          labels: data.statuses.labels,
          datasets: [{
            data: data.statuses.data,
            backgroundColor: data.statuses.colors,
            borderColor: '#111e21',
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: { boxWidth: 12, padding: 12, color: '#f1f5f9' }
            }
          }
        }
      });
    }

  } catch (error) {
    console.error('Error fetching chart data:', error);
  }
});
