fetch('/estadisticas/ventas-mensuales/') 
  .then((response) => response.json())
  .then((data) => {
    const ctx = document.getElementById('ventasMensuales').getContext('2d');
    if (window.graficoVentasMensuales) {
      window.graficoVentasMensuales.destroy();
    }
    window.graficoVentasMensuales = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.labels, 
        datasets: [
          {
            label: 'Ventas Diarias ($)',
            data: data.data,
            backgroundColor: 'rgb(255, 205, 86)',
            borderColor: 'rgb(240, 168, 0)',
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  })
  .catch((error) => console.error('Error al obtener datos:', error));
