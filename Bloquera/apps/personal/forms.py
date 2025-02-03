from django import forms
from .models import Empleado, Proveedor

class FormularioEmpleado(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            'nombre', 
            'direccion', 
            'telefono', 
            'estado',  
        ]
        labels = {
            'nombre': 'Nombre',
            'direccion': 'Dirección',
            'telefono': 'Número de teléfono',
            'estado': 'Estado del empleado',
        }
        ESTADO_CHOICES = [
            ('activo', 'Activo'),
            ('inactivo', 'Inactivo'),
        ]   
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
        

class FormularioProveedor(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            'nombre', 
            'direccion', 
            'telefono', 
            'tipo',  
        ]
        labels = {
            'nombre': 'Nombre',
            'direccion': 'Dirección',
            'telefono': 'Número de teléfono',
            'tipo': 'Tipo de proveedor',
        }
        TIPO_CHOICES = [
            ('empresa', 'Empresa'),
            ('individuo', 'Individuo'),
        ]   
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }