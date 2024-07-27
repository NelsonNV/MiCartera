document.addEventListener('DOMContentLoaded', () => {
  const ctxGastos = document.getElementById('gastosChart').getContext('2d');
  const ctxResumenMensual = document.getElementById('resumenMensualChart').getContext('2d');

  // Función para cargar datos del gráfico desde la API
  const fetchChartData = async (url) => {
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error al cargar datos:', error);
    }
  };

  // Cargar y mostrar el gráfico de gastos por categoría
  fetchChartData(urlGastosPorCategoria).then(chartData => {
    if (chartData) {
      new Chart(ctxGastos, {
        type: 'pie',
        data: {
          labels: chartData.labels,
          datasets: [{
            data: chartData.data,
            backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe', '#ffce56'],
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            tooltip: {
              callbacks: {
                label: function (tooltipItem) {
                  return tooltipItem.label + ': ' + tooltipItem.raw.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ".") + ' $';
                }
              }
            }
          }
        }
      });
    }
  });

  // Cargar y mostrar el gráfico de resumen mensual
  fetchChartData(urlResumenAnual).then(chartData => {
    if (chartData) {
      new Chart(ctxResumenMensual, {
        type: 'line',
        data: {
          labels: chartData.labels,
          datasets: [
            {
              label: 'Ingresos',
              data: chartData.ingresos,
              borderColor: '#36a2eb',
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              fill: true,
            },
            {
              label: 'Gastos',
              data: chartData.gastos,
              borderColor: '#ff6384',
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
              fill: true,
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            tooltip: {
              callbacks: {
                label: function (tooltipItem) {
                  return tooltipItem.dataset.label + ': ' + tooltipItem.raw.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ".") + ' $';
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }
  });
});
