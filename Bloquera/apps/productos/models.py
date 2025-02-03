from django.db import models

# Create your models here.
class Block(models.Model):
    TIPO_BLOCK = [
        ('BLOCK DEL 10','BLOCK DEL 10'),
        ('BLOCK DEL 13','BLOCK DEL 13'),
        ('BLOCK DEL 15','BLOCK DEL 15'),
        ('BLOCK DEL 20','BLOCK DEL 20'),
    ]
    nombre = models.CharField(max_length=15,choices=TIPO_BLOCK,null=False)
    precioDeVenta = models.DecimalField(max_digits=10, decimal_places=2,blank=False,null=False)
    precioDeCosto = models.DecimalField(max_digits=10, decimal_places=2,blank=False,null=False)
    fechaDeElaboracion = models.DateField(blank=False,null=False)
    cantidadDisponible = models.PositiveIntegerField(blank=False,null=False)
    cantidadMinRequerida = models.PositiveIntegerField(blank=False,null=False)
    
    def __str__(self):
        return f"{self.nombre} (${self.precioDeVenta} c/u)"
    
    
class Materiales(models.Model):
    UNIDAD_MEDIDA = [
        ('Kg','Kilogramos'),
        ('g','Gramos'),
        ('palet','Palet'),
        ('l','Litros'),
        ('m3','Metro cúbico'),
        ('bolsa','Bolsa'),
        ('u','Unidad'),
    ]
    nombre = models.CharField(max_length=15,null=False, blank=False)
    unidadDeMedida = models.CharField(max_length=15,choices=UNIDAD_MEDIDA,null=False)
    precioDeCosto = models.DecimalField(max_digits=10, decimal_places=2,blank=False,null=False)
    cantidadDisponible = models.PositiveIntegerField(blank=False,null=False)
    cantidadMinRequerida = models.PositiveIntegerField(blank=False,null=False)
    
    def __str__(self):
        return f"{self.nombre} (${self.precioDeCosto})"