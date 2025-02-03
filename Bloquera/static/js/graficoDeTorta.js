fetch('/estadisticas/productos-mas-vendidos/')
  .then((response) => response.json())
  .then((data) => {
    const ctx = document.getElementById('productosMasVendidos').getContext('2d');
    if (window.graficoProductosMasVendidos) {
      window.graficoProductosMasVendidos.destroy();
    }
    window.graficoProductosMasVendidos = new Chart(ctx, {
      type: 'pie', 
      data: {
        labels: data.labels, 
        datasets: [
          {
            label: 'Productos más vendidos (%)',
            data: data.data, 
            backgroundColor: [
              'rgba(255, 99, 132)',
              'rgba(54, 162, 235)',
              'rgba(255, 205, 86)',
              'rgba(89, 86, 214)',
              'rgba(153, 102, 255)',
            ],
            borderWidth: 1,
          },
        ],
      },
    });
  })
  .catch((error) => console.error('Error al obtener datos:', error));
