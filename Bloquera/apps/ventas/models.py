from django.db import models
from apps.productos.models import Block

class Venta(models.Model):
    FORMA_PAGO = [
        ('Efectivo','Efectivo'),
        ('Transferencia','Transferencia'),
        ('Débito','Débito'),
        ('Crédito','Crédito'),
    ]
    fechaDeVenta = models.DateField(blank=False, null=False)
    formaDePago = models.CharField(max_length=15, choices=FORMA_PAGO,blank=False, null=False)
    total = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    lugarVenta = models.CharField(max_length=30,blank=False, null=False, default="Capital")
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda primero la instancia
    
    def calcular_total(self):
        # Calcula el total de todos los detalles de la venta
        self.total = sum(detalle.subTotal for detalle in self.detalleVenta.all())
        self.save(update_fields=['total'])  # Guarda solo el campo total
   

class DetalleVenta(models.Model):
    block = models.ForeignKey(Block,on_delete=models.CASCADE,related_name='detalleBlock',default=1)
    venta = models.ForeignKey(Venta,on_delete=models.CASCADE,related_name='detalleVenta')
    cantidad = models.PositiveIntegerField(blank=False, null=False)
    subTotal = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    
    def save(self, *args, **kwargs):
        self.subTotal = self.cantidad * self.block.precioDeVenta
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.block.nombre} {self.cantidad} {self.subTotal}"


