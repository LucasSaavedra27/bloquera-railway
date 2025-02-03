document.addEventListener('DOMContentLoaded', function() {
    var inputElement1 = document.getElementById('id_precioDeVenta');
    var inputElement2 = document.getElementById('id_precioDeCosto');

    inputElement1.addEventListener('input', function(event) {
        event.target.value = event.target.value.replace(/[^0-9]/g, '');
    });
    inputElement2.addEventListener('input', function(event) {
        event.target.value = event.target.value.replace(/[^0-9]/g, '');
    });
});
