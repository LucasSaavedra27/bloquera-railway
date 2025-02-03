const inputCantidadM2 = document.getElementById('metrosCuadrados');
const inputResultado = document.getElementById('resultado');
const botonCalcular = document.getElementById('btnCalcular');
const botonReiniciar = document.getElementById('btnReiniciar');
const labelResultado = document.getElementById('resultadoLabel');


botonCalcular.addEventListener('click', () => {
    const valorCantidad = parseFloat(inputCantidadM2.value); 
    if (!isNaN(valorCantidad)) { 
    inputResultado.value = valorCantidad * 13;
    inputResultado.style.display= 'block';
    botonReiniciar.style.display='block';
    labelResultado.style.display='block';
    } else {
    inputResultado.value = '';
    alert('Por favor, introduce un número válido en el primer campo.');
    }
});

botonReiniciar.addEventListener('click', () => {
    if (inputResultado.style.display==='block') { 
    inputResultado.style.display= 'none';
    inputCantidadM2.value=''
    botonReiniciar.style.display='none'
    labelResultado.style.display='none';
    }
});