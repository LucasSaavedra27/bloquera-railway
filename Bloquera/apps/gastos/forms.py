from django import forms
from django.forms import inlineformset_factory
from .models import Gasto


class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['tipo', 'fecha', 'monto', 'formaDePago', 'proveedor', 'empleado']
        labels = {
            'tipo': 'Tipo de gasto',
            'fecha': 'Fecha',
            'monto': 'Monto',
            'formaDePago': 'Forma de pago',
            'proveedor': 'Proveedor',
            'empleado': 'Empleado',
        }
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control', 'id': 'tipo-gasto'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'formaDePago': forms.Select(attrs={'class': 'form-control'}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'empleado': forms.Select(attrs={'class': 'form-control'}),
        }


from django import forms
from django.forms import inlineformset_factory
from .models import Gasto, DetallesGastosMateriales

class DetalleGastoMaterialForm(forms.ModelForm):
    class Meta:
        model = DetallesGastosMateriales
        fields = ['materiales', 'cantidad']
        labels = {
            'materiales': 'Material',
            'cantidad': 'Cantidad',
        }
        widgets = {
            'materiales': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

DetalleGastoFormSet = inlineformset_factory(
    Gasto, 
    DetallesGastosMateriales, 
    form=DetalleGastoMaterialForm,
    extra=1,
    can_delete=True
)

