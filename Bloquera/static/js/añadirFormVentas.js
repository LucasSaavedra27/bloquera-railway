document.addEventListener('DOMContentLoaded', function() {
    if (window.scriptLoaded) {
        return;
    }
    window.scriptLoaded = true;
    
    const formsetContainer = document.getElementById('detalleVentaContainer');
    const totalForms = document.getElementById('id_detalleVenta-TOTAL_FORMS');
    const ElementoTotal = document.getElementById('id_total_ventas');

    document.getElementById('btn-add').addEventListener('click', function() {
        if (totalForms && formsetContainer) {
            const contadorForm = parseInt(totalForms.value);
        
            // Clonamos el primer formulario (base)
            const nuevoForm = formsetContainer.children[0].cloneNode(true);

            // Limpiar valores de los inputs en el nuevo formulario
            nuevoForm.querySelectorAll('input, select').forEach((element) => {
                if (element.tagName === 'SELECT') {
                    element.selectedIndex = 0;
                } else {
                    element.value = '';
                }
            });

            // Actualizar los nombres y IDs de los campos del nuevo formulario
            nuevoForm.querySelectorAll('input, select, label, span').forEach((element) => {
                ['name', 'for', 'id'].forEach(attr => {
                    if (element.getAttribute(attr)) {
                        element.setAttribute(attr, element.getAttribute(attr).replace(/-\d+-/, `-${contadorForm}-`));
                    }
                });
            });

            // Incrementar el contador de formularios
            totalForms.value = contadorForm + 1;

            // Añadir el nuevo formulario al contenedor
            formsetContainer.appendChild(nuevoForm);

            // Agregar eventos al nuevo formulario
            agregarEventosFormulario(contadorForm);

            //console.log(`Formulario ${contadorForm} añadido`); // Para depuración
        } else {
            console.error('El elemento TOTAL_FORMS o detalleVentaContainer no se encuentra en el DOM.');
        }
    });

    function agregarEventosFormulario(formIndex) {
        const blockSelect = document.getElementById(`id_detalleVenta-${formIndex}-block`);
        const cantidadBlock = document.getElementById(`id_detalleVenta-${formIndex}-cantidad`);
        const blockPrecio = document.getElementById(`id_block-${formIndex}-precio`);

        if (blockSelect && cantidadBlock && blockPrecio) {
            blockSelect.addEventListener('change', actualizarSubtotal);
            cantidadBlock.addEventListener('input', actualizarSubtotal);

            function actualizarSubtotal() {
                const blockId = blockSelect.value;
                const cantidad = parseFloat(cantidadBlock.value) || 0;

                if (blockId) {
                    fetch(`/ventas/obtener-precio-block/${blockId}/`)
                        .then(response => response.json())
                        .then(data => {
                            if (data.precio) {
                                let subtotal = data.precio * cantidad;
                                blockPrecio.textContent = subtotal.toFixed(2);
                                actualizarTotal();
                            } else {
                                blockPrecio.textContent = '0';
                                actualizarTotal();
                                alert(data.error || 'Error al obtener el precio');
                            }
                        })
                        .catch(error => console.error('Error:', error));
                } else {
                    blockPrecio.textContent = '';
                    actualizarTotal();
                }
            }
        }
    }

    function actualizarTotal() {
        let totalVenta = 0;

        document.querySelectorAll('h5.subtotal span[id^="id_block-"][id$="-precio"]').forEach((span) => {
            const subtotal = parseFloat(span.textContent) || 0;
            totalVenta += subtotal;
        });

        if (ElementoTotal) {
            ElementoTotal.textContent = totalVenta.toFixed(2);
        } else {
            console.error('Elemento de total no encontrado en el DOM.');
        }
    }

    // Inicializar eventos para formularios existentes
    if (totalForms) {
        for (let i = 0; i < parseInt(totalForms.value); i++) {
            agregarEventosFormulario(i);
        }
    } else {
        console.error('Elemento TOTAL_FORMS no encontrado en el DOM.');
    }
});

