from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('regVentas/', views.regVentas, name='regVentas'),  
    path('agregarVenta/', views.agregarVenta, name='agregarVenta'),
    path('obtener-precio-block/<int:block_id>/', views.obtener_precio_block, name='obtener_precio_block'),
    path('detallesVenta/<int:venta_id>/', views.obtener_detalles_venta, name='obtener_detalles_venta'),
    path('buscarVentas/', views.buscarVentas, name='buscarVentas'),
    path('generarPDFVentas/', views.generarPDFVentas, name='generarPDFVentas'),
    
]
