from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from apps.gastos.models import Gasto, DetallesGastosMateriales
from apps.gastos.forms import GastoForm, DetalleGastoFormSet
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa # type: ignore
from io import BytesIO
from datetime import datetime
from apps.productos.models import Materiales
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def regGastos(request):
    gastos = Gasto.objects.all().order_by('-fecha')  # Ordenar por fecha descendente
    paginator = Paginator(gastos, 10)  
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request,'gastos/regGastos.html',{'page_obj':page_obj})

@login_required
def agregarGastos(request):
    if request.method == 'POST':
        gastoForm = GastoForm(request.POST)
        detalleGastoFormSet = DetalleGastoFormSet(request.POST)
        total = 0
        if gastoForm.is_valid() and detalleGastoFormSet.is_valid():
            gasto = gastoForm.save()
            if gasto.tipo == 'Material':  # Solo guarda detalles si es un gasto de materiales
                detalles = detalleGastoFormSet.save(commit=False)
                for detalle in detalles:
                    detalle.gasto = gasto
                    detalle.subTotal = detalle.cantidad * detalle.materiales.precioDeCosto
                    total += detalle.subTotal
                    material = detalle.materiales
                    material.cantidadDisponible += detalle.cantidad
                    material.save()
                    detalle.save()
                gasto.monto = total
                gasto.save()
            return redirect('gastos:regGastos')
    else:
        gastoForm = GastoForm()
        detalleGastoFormSet = DetalleGastoFormSet()

    return render(request, 'gastos/agregarGastos.html', {'gastoForm': gastoForm, 'detalleGastoFormSet': detalleGastoFormSet})

@login_required
def buscarGastos(request):
    gastos = Gasto.objects.all()
    fecha_inicio = request.GET.get('busqueda_inicio')
    fecha_fin = request.GET.get('busqueda_fin')
    if fecha_inicio and fecha_fin:
        gastos = gastos.filter(fecha__range=[fecha_inicio, fecha_fin])
    elif fecha_inicio:
        gastos = gastos.filter(fecha=fecha_inicio)
    elif fecha_fin:
        gastos = gastos.filter(fecha=fecha_fin)
    else:
        redirect("/gastos/regGastos")
   
    return render(request, 'gastos/regGastos.html', {'page_obj': gastos, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin})

@login_required
def generarPDFGastos(request):
    gastos = Gasto.objects.prefetch_related('detalleGasto').all()

    # Obtener los valores de las fechas desde la solicitud GET
    fecha_inicio = request.GET.get('busqueda_inicio_PDF')
    fecha_fin = request.GET.get('busqueda_fin_PDF')
    
    # Filtrar las ventas si se pasan las fechas
    if fecha_inicio and fecha_fin:
        gastos = gastos.filter(fechaa__range=[fecha_inicio, fecha_fin])
    elif fecha_inicio:
        gastos = gastos.filter(fecha=fecha_inicio)
    elif fecha_fin:
        gastos = gastos.filter(fecha=fecha_fin)
        
    template = get_template('gastos/tabla.html')
    
    html = template.render({'gastos': gastos, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin})
    
    fecha_hora_actual = datetime.now().strftime("%d-%m-%Y - %H:%M")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Registro de Gastos - {fecha_hora_actual} hs.pdf"'

    pisa_status = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    
    return response

@login_required
def obtener_precio_material(request, material_id):
    try:
        material = Materiales.objects.get(pk=material_id)
        return JsonResponse({'precio': material.precioDeCosto})
    except Materiales.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    
@login_required
def obtener_detalles_gastos(request, gasto_id):
    try:
        # Obtener la venta y sus detalles
        gasto = Gasto.objects.get(id=gasto_id)
        detalles_gasto = DetallesGastosMateriales.objects.filter(gasto_id=gasto_id)

        # Convertir los detalles de la venta a una lista
        detalles = [
            {
                'material': detalle.materiales.nombre,
                'cantidad': detalle.cantidad,
                'precioDeCosto': detalle.materiales.precioDeCosto,
                'subtotal': detalle.subTotal,
            }
            for detalle in detalles_gasto
        ]

        # Devolver los datos como JSON
        return JsonResponse({
            'id': gasto.id,
            'fecha': gasto.fecha.strftime('%d/%m/%Y'),
            'total': gasto.monto,
            'detalles': detalles,
        })
    except Gasto.DoesNotExist:
        return JsonResponse({'error': 'Gasto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)