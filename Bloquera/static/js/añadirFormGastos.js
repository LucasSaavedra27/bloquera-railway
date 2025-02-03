document.addEventListener('DOMContentLoaded', function () {
    if (window.scriptLoaded) return;
    window.scriptLoaded = true;

    const formsetContainer = document.getElementById('detalleGastoContainer');
    const totalForms = document.getElementById('id_detalleGasto-TOTAL_FORMS');
    const ElementoTotal = document.getElementById('id_total_gastos');
    const montoField = document.getElementById('id_monto');
    const tipoGastoField = document.getElementById('tipo-gasto');
    const proveedorField = document.getElementById('id_proveedor');
    const empleadoField = document.getElementById('id_empleado');

    // Botón para agregar un nuevo formulario
    document.getElementById('btn-add').addEventListener('click', function () {
        if (totalForms && formsetContainer) {
            const contadorForm = parseInt(totalForms.value);
            const nuevoForm = formsetContainer.children[1].cloneNode(true);

            // Limpiar valores de los inputs en el nuevo formulario
            nuevoForm.querySelectorAll('input, select').forEach((element) => {
                if (element.tagName === 'SELECT') {
                    element.selectedIndex = 0;
                } else {
                    element.value = '';
                }
            });

            // Actualizar nombres y IDs de los campos
            nuevoForm.querySelectorAll('input, select, label, span').forEach((element) => {
                ['name', 'for', 'id'].forEach(attr => {
                    const currentAttr = element.getAttribute(attr);
                    if (currentAttr) {
                        element.setAttribute(attr, currentAttr.replace(/-\d+-/, `-${contadorForm}-`));
                    }
                });
            });

            // Incrementar el contador de formularios
            totalForms.value = contadorForm + 1;

            // Añadir el nuevo formulario
            formsetContainer.appendChild(nuevoForm);
            agregarEventosFormulario(contadorForm);
        } else {
            console.error('Elemento TOTAL_FORMS o detalleGastoContainer no encontrado en el DOM.');
        }
    });

    // Función para agregar eventos a los formularios
    function agregarEventosFormulario(formIndex) {
        const materialSelect = document.getElementById(`id_detalleGasto-${formIndex}-materiales`);
        const cantidadMateriales = document.getElementById(`id_detalleGasto-${formIndex}-cantidad`);
        const materialPrecio = document.getElementById(`id_material-${formIndex}-precio`);

        if (materialSelect && cantidadMateriales && materialPrecio) {
            materialSelect.addEventListener('change', actualizarSubtotal);
            cantidadMateriales.addEventListener('input', actualizarSubtotal);
        }

        // Actualizar subtotal cuando se cambian los valores
        function actualizarSubtotal() {
            const materialId = materialSelect.value;
            const cantidad = parseFloat(cantidadMateriales.value) || 0;

            if (materialId) {
                fetch(`/gastos/obtener-precio-material/${materialId}/`)
                    .then(response => response.json())
                    .then(data => {
                        const subtotal = data.precio ? data.precio * cantidad : 0;
                        materialPrecio.textContent = subtotal.toFixed(2);
                        actualizarTotal();  // Actualiza el total después de calcular el subtotal
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        materialPrecio.textContent = '0.00';
                        actualizarTotal();
                    });
            } else {
                materialPrecio.textContent = '0.00';
                actualizarTotal();
            }
        }
    }

    // Actualizar el total de todos los formularios
    function actualizarTotal() {
        let totalGasto = 0;
        document.querySelectorAll('h5.subtotal span[id^="id_material-"][id$="-precio"]').forEach((span) => {
            const subtotal = parseFloat(span.textContent) || 0;
            totalGasto += subtotal;
        });

        if (ElementoTotal) {
            ElementoTotal.textContent = totalGasto.toFixed(2);
        } else {
            console.error('Elemento de total no encontrado en el DOM.');
        }

        if (montoField) {
            montoField.value = totalGasto.toFixed(2);
        } else {
            console.error('Campo de monto no encontrado en el DOM.');
        }
    }

    // Inicializar eventos para formularios existentes
    if (totalForms) {
        for (let i = 0; i < parseInt(totalForms.value); i++) {
            agregarEventosFormulario(i);
        }
    }

    // Manejo de campos según el tipo de gasto seleccionado
    const toggleFields = () => {
        const tipoSeleccionado = tipoGastoField.value;

        switch (tipoSeleccionado) {
            case 'Flete':
            case 'Salario':
                montoField.removeAttribute('readonly');
                empleadoField.removeAttribute('disabled');
                proveedorField.setAttribute('disabled', 'disabled');
                formsetContainer.style.display = 'none';
                break;
            case 'Servicios':
                montoField.removeAttribute('readonly');
                proveedorField.removeAttribute('disabled');
                empleadoField.setAttribute('disabled', 'disabled');
                formsetContainer.style.display = 'none';
                break;
            case 'Material':
                proveedorField.removeAttribute('disabled');
                empleadoField.setAttribute('disabled', 'disabled');
                formsetContainer.style.display = 'block';
                montoField.setAttribute('readonly', 'readonly');
                break;
            default:
                formsetContainer.style.display = 'none';
        }
    };

    // Llamada inicial a toggleFields y listener de cambio
    toggleFields();
    tipoGastoField.addEventListener('change', toggleFields);
});
