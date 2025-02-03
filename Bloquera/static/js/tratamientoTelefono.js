document.addEventListener('DOMContentLoaded', function() {
    var inputElement1 = document.getElementById('id_telefono');
    inputElement1.addEventListener('input', function(event) {
        event.target.value = event.target.value.replace(/[^0-9]/g, '');
    });
});
