from django import forms
from .models import Block, Materiales

class FormularioProducto(forms.ModelForm):
    class Meta:
        model = Block
        fields = [
            'nombre', 
            'precioDeVenta', 
            'precioDeCosto', 
            'fechaDeElaboracion',  
            'cantidadDisponible', 
            'cantidadMinRequerida',
        ]
        labels = {
            'nombre': 'Nombre del Producto',
            'precioDeVenta': 'Precio de Venta',
            'precioDeCosto': 'Precio de Costo',
            'fechaDeElaboracion': 'Fecha de Elaboración',
            'cantidadDisponible': 'Cantidad Disponible',
            'cantidadMinRequerida': 'Cantidad Mínima Requerida',
        }
        NOMBRE_CHOICES = [
            ('BLOCK DEL 10', 'Block del 10'),
            ('BLOCK DEL 13', 'Block del 13'),
            ('BLOCK DEL 15', 'Block del 15'),
            ('BLOCK DEL 20', 'Block del 20'),
        ]   
        widgets = {
            
            'nombre': forms.Select(attrs={'class': 'form-control'}),
            'precioDeVenta': forms.TextInput(attrs={'class': 'form-control'}),
            'precioDeCosto': forms.TextInput(attrs={'class': 'form-control'}),
            'fechaDeElaboracion': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'cantidadDisponible': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidadMinRequerida': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        

class FormularioMateriales(forms.ModelForm):
    class Meta:
        model = Materiales
        fields = [
            'nombre', 
            'precioDeCosto', 
            'unidadDeMedida',  
            'cantidadDisponible', 
            'cantidadMinRequerida',
        ]
        labels = {
            'nombre': 'Nombre del Producto',
            'precioDeCosto': 'Precio de Costo',
            'unidadDeMedida': 'Unidad de medida',
            'cantidadDisponible': 'Cantidad Disponible',
            'cantidadMinRequerida': 'Cantidad Mínima Requerida',
        }
        UNIDADDEMEDIDA_CHOICES = [
        ('Kg','Kilogramos'),
        ('g','Gramos'),
        ('palet','Palet'),
        ('l','Litros'),
        ('m3','Metro cúbico'),
        ('bolsa','Bolsa'),
        ('u','Unidad'),
        ]
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precioDeCosto': forms.TextInput(attrs={'class': 'form-control'}),
            'unidadDeMedida': forms.Select(attrs={'class': 'form-control'}),
            'cantidadDisponible': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidadMinRequerida': forms.NumberInput(attrs={'class': 'form-control'}),
        }