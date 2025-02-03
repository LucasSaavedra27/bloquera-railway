from django.urls import path
from . import views
from .views import EmpleadoUpdateView, ProveedorUpdateView

app_name = 'personal'

urlpatterns = [
    path('regEmpleados/', views.regEmpleados, name='regEmpleados'),
    path('agregarEmpleado/', views.agregarEmpleado, name='agregarEmpleado'),
    path('editarEmpleado/<int:pk>/', EmpleadoUpdateView.as_view(), name='editarEmpleado'),
    path('regProveedores/', views.regProveedores, name='regProveedores'),  
    path('agregarProveedor/', views.agregarProveedor, name='agregarProveedor'),
    path('editarProveedor/<int:pk>/', ProveedorUpdateView.as_view(), name='editarProveedor'),# Ajusta esto según tus vistas
]
