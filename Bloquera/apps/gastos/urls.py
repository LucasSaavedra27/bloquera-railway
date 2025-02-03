from django.urls import path
from . import views

app_name = 'gastos'

urlpatterns = [
    path('regGastos/', views.regGastos, name='regGastos'),  
    path('agregarGastos/', views.agregarGastos, name='agregarGastos'), 
    path('buscarGastos/', views.buscarGastos, name='buscarGastos'),
    path('generarPDFGastos/',views.generarPDFGastos,name='generarPDFGastos'),
    path('obtener-precio-material/<int:material_id>/', views.obtener_precio_material, name='obtener-precio-material'),
    path('detallesGasto/<int:gasto_id>/', views.obtener_detalles_gastos, name='obtener_detalles_gastos'),

   
]
