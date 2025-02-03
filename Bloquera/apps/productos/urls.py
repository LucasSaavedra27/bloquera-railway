from django.urls import path
from . import views
from .views import ProductoUpdateView, MaterialesUpdateView

app_name = 'productos'

urlpatterns = [
    path('regProductos/', views.regProductos, name='regProductos'),  # Ajusta esto según tus vistas
    path('agregarProducto/',views.agregarProducto,name='agregarProducto'),
    path('editarProducto/<int:pk>/', ProductoUpdateView.as_view(), name='editarProducto'),
    path('regMateriales/', views.regMateriales, name='regMateriales'),  # Ajusta esto según tus vistas
    path('agregarMateriales/',views.agregarMateriales,name='agregarMateriales'),
    path('editarMateriales/<int:pk>/', MaterialesUpdateView.as_view(), name='editarMateriales'),

]
