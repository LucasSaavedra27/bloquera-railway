from django.shortcuts import redirect, render
from .models import Empleado, Proveedor
from .forms import FormularioEmpleado, FormularioProveedor
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def regEmpleados(request):
    empleados = Empleado.objects.all() 
    return render(request, 'personal/regEmpleados.html', {'empleados': empleados})

@login_required
def agregarEmpleado(request):
    form = FormularioEmpleado() 
    if request.method == 'POST':
        form = FormularioEmpleado(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('/personal/regEmpleados')  
    return render(request, 'personal/agregarEmpleados.html', {'form': form})

class EmpleadoUpdateView(LoginRequiredMixin, UpdateView):
    model = Empleado
    form_class = FormularioEmpleado
    template_name = 'personal/editarEmpleados.html' 
    success_url = reverse_lazy('personal:regEmpleados')  
    
@login_required    
def regProveedores(request):
    proveedores = Proveedor.objects.all() 
    return render(request, 'personal/regProveedores.html', {'proveedores': proveedores})

@login_required
def agregarProveedor(request):
    form = FormularioProveedor() 
    if request.method == 'POST':
        form = FormularioProveedor(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('/personal/regProveedores')  
    return render(request, 'personal/agregarProveedor.html', {'form': form})

class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = FormularioProveedor
    template_name = 'personal/editarProveedor.html' 
    success_url = reverse_lazy('personal:regProveedores')  