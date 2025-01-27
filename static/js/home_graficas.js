document.addEventListener('DOMContentLoaded', () => {
  const ctxGastos = document.getElementById('gastosChart');
  const ctxResumenMensual = document.getElementById('resumenMensualChart').getContext('2d');
  const ctxGastosMes = document.getElementById('gastosMesChart').getContext('2d');

  // Función para generar un color hexadecimal a partir de un texto
  const textToColor = (text) => {
    const hash = Array.from(text).reduce((acc, char) => {
      const charCode = char.charCodeAt(0);
      return ((acc << 5) - acc) + charCode;
    }, 0);

    const color = (hash & 0x00FFFFFF).toString(16).padStart(6, '0');
    return `#${color}`;
  };
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

  const gastosChart = echarts.init(ctxGastos);
  // Cargar y mostrar el gráfico de gastos por categoría
  fetchChartData(urlGastosPorCategoria+"?format=sunburst").then(chartData => {
    if (chartData) {
      const datosSunburst = chartData; // Ya está en el formato correcto
      console.log(datosSunburst);

      const option = {
        title: {
          text: 'Gastos por Categoría y Subcategoría',
          left: 'center',
          textStyle: {
            fontSize: 16,
            color: '#333'
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c} $'
        },
        series: {
          type: 'sunburst',
          data: datosSunburst,
          radius: [0, '80%'], // Ajusta el tamaño del gráfico
          label: {
            show: true,
            fontSize: 12,
            color: '#000',
            rotate: 0 // El texto no rotará
          },
          itemStyle: {
            borderWidth: 1,
            borderColor: '#fff'
          },
          levels: [
            {}, // Nivel base
            {
              r0: '0%',  // Radio interno
              r: '40%',  // Radio externo para este nivel
              label: {
                fontSize: 12
              }
            },
            {
              r0: '40%',
              r: '80%',
              label: {
                fontSize: 12,
                position: 'outside' // Etiquetas fuera del gráfico
              }
            }
          ]
        }
      };

      gastosChart.setOption(option);
    }else {
  console.error('Los datos del gráfico están vacíos o son inválidos.');
}
  });
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

  // Cargar y mostrar el gráfico de ingresos y gastos del mes
  fetchChartData(urlResumenMensual).then(chartData => {
    if (chartData) {
      new Chart(ctxGastosMes, {
        type: 'line',
        data: {
          labels: chartData.labels,
          datasets: [
            {
              label: 'Ingresos del Mes',
              data: chartData.ingresos,
              borderColor: '#36a2eb',
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              fill: true,
            },
            {
              label: 'Gastos del Mes',
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
