from django.db import models
from apps.productos.models import Materiales
from apps.personal.models import Proveedor, Empleado

class Gasto(models.Model):
    TIPO_GASTO = [
        ('Material', 'Compra de Material'),
        ('Salario', 'Pago de Salario'),
        ('Servicios', 'Servicios'),
        ('Flete', 'Flete'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_GASTO, null=False, blank=False)
    fecha = models.DateField(null=False, blank=False)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    FORMA_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
        ('Débito', 'Débito'),
        ('Crédito', 'Crédito'),
    ]
    formaDePago = models.CharField(max_length=15, choices=FORMA_PAGO, blank=False, null=False)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='gastoProveedor', null=True, blank=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='gastoSalario', null=True, blank=True)

    def __str__(self):
        if self.tipo == 'Material':
            return f"Gasto Material - Proveedor: {self.proveedor} - Monto: ${self.monto}"
        elif self.tipo == 'Salario':
            return f"Gasto Salario - Empleado: {self.empleado} - Monto: ${self.monto}"
        return f"Gasto: {self.tipo} - Monto: ${self.monto}"


class DetallesGastosMateriales(models.Model):
    materiales = models.ForeignKey(Materiales,on_delete=models.CASCADE,related_name='detalleMateriales')
    gasto = models.ForeignKey(Gasto,on_delete=models.CASCADE,related_name='detalleGasto')
    cantidad = models.PositiveIntegerField(blank=False, null=False)
    subTotal = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    
    def save(self, *args, **kwargs):
        self.subTotal = self.cantidad * self.materiales.precioDeCosto
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.materiales.nombre} {self.cantidad} {self.subTotal}"