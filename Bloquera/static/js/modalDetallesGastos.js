document.addEventListener('DOMContentLoaded', function() {
    const botonesVerDetalles = document.querySelectorAll('.btnVerDetalles');

    botonesVerDetalles.forEach(button => {
      button.addEventListener('click', function() {
        const gastoId = button.getAttribute('data-gasto-id');
        // Hacer la solicitud para obtener los detalles de la venta
        fetch(`/gastos/detallesGasto/${gastoId}/`)
          .then(response => response.json())
          .then(data => {
            if (data.error) {
              alert(data.error);
              return;
            }

            // Llenar los datos del modal con los detalles de la venta
            document.getElementById('modal-gasto-id').textContent = data.id;
            document.getElementById('modal-gasto-fecha').textContent = data.fecha;
            document.getElementById('modal-gasto-total').textContent = `$${data.total}`;

            const materialesList = document.getElementById('modal-detalles-materiales');
            materialesList.innerHTML = ''; // Limpiar la lista antes de agregar los productos

            data.detalles.forEach(detalle => {
              const li = document.createElement('li');
              li.textContent = `${detalle.material} - ${detalle.cantidad} u x $${detalle.precioDeCosto} c/u = $${detalle.subtotal}`;
              materialesList.appendChild(li);
            });
          })
          .catch(error => console.error('Error al cargar los detalles:', error));
      });
    });
  });