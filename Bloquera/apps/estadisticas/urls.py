from django.urls import path
from . import views

app_name = 'estadisticas'

urlpatterns = [
    path('', views.estadisticas, name='estadisticas'),
    path('ventas-mensuales/', views.ventas_mensuales, name='ventas_mensuales'),
    path('productos-mas-vendidos/', views.productos_mas_vendidos, name='productos_mas_vendidos'),
    # Agregar todas las vistas en una url
]
