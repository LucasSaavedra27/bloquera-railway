document.addEventListener('DOMContentLoaded', function() {
    const botonesVerDetalles = document.querySelectorAll('.btnVerDetalles');

    botonesVerDetalles.forEach(button => {
      button.addEventListener('click', function() {
        const ventaId = button.getAttribute('data-venta-id');
        // Hacer la solicitud para obtener los detalles de la venta
        fetch(`/ventas/detallesVenta/${ventaId}/`)
          .then(response => response.json())
          .then(data => {
            if (data.error) {
              alert(data.error);
              return;
            }

            // Llenar los datos del modal con los detalles de la venta
            document.getElementById('modal-venta-id').textContent = data.id;
            document.getElementById('modal-venta-fecha').textContent = data.fecha;
            document.getElementById('modal-venta-total').textContent = `$${data.total}`;

            const productosList = document.getElementById('modal-detalles-productos');
            productosList.innerHTML = ''; // Limpiar la lista antes de agregar los productos

            data.detalles.forEach(detalle => {
              const li = document.createElement('li');
              li.textContent = `${detalle.producto} - ${detalle.cantidad} u x $${detalle.precioVenta} c/u = $${detalle.subtotal}`;
              productosList.appendChild(li);
            });
          })
          .catch(error => console.error('Error al cargar los detalles:', error));
      });
    });
  });