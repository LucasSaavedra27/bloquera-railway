from django.forms.models import inlineformset_factory
from django import forms
from .models import Venta,DetalleVenta

class FormularioVenta(forms.ModelForm):
    class Meta:
        model = Venta
        fields = [
            'fechaDeVenta', 
            'formaDePago',
            'lugarVenta', 
        ]
        labels = {
            'fechaDeVenta': 'Fecha de venta',
            'formaDePago': 'Forma de pago',
            'lugarVenta': 'Lugar de entrega',
        }  
        widgets = {
            'fechaDeVenta': forms.TextInput(attrs={'type': 'date','class': 'form-control'}),
            'formaDePago': forms.Select(attrs={'class': 'form-control'}),
            'lugarVenta': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['block', 'cantidad']
        labels = {
            'block': 'Block',
            'cantidad': 'Cantidad',
        }
        widgets = {
            'block': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        block = self.cleaned_data.get('block')
        
        if cantidad > block.cantidadDisponible:
            raise forms.ValidationError(f"Solo hay {block.cantidadDisponible} unidades disponibles de {block.nombre}.")
        
        return cantidad

DetalleVentaFormSet = inlineformset_factory(
    Venta, 
    DetalleVenta,  # Venta y DetalleVenta son los modelos relacionados
    form=DetalleVentaForm,
    extra=1,  # comienza mostrando 1 formulario
    can_delete=True  # permite borrar el formulario
)