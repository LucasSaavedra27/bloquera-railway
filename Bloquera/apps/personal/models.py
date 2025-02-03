from django.db import models

class Datosbase(models.Model):
    nombre = models.CharField(max_length=30,null=False,blank=False)
    direccion = models.CharField(max_length=50,null=False,blank=False)
    telefono = models.CharField(max_length=10,null=False,blank=False)
    
    def __str__(self):
        return self.nombre
    
class Proveedor(Datosbase):
    TIPO = [
        ('Empresa','Empresa'),
        ('Individuo','Individuo'),
    ]
    tipo = models.CharField(max_length=10,choices=TIPO, blank=False, null=False)
    
class Empleado(Datosbase):
    ESTADO = [
        ('Activo','Activo'),
        ('Inactivo','Inactivo'),
    ]
    estado = models.CharField(max_length=10,choices=ESTADO, blank=False, null=False)
