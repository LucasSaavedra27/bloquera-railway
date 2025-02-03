from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from apps.ventas.forms import FormularioVenta,DetalleVentaFormSet
from django.http import JsonResponse
from .models import Block, Venta, DetalleVenta
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa # type: ignore
from io import BytesIO
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required
def regVentas(request):
    ventas = Venta.objects.all().order_by('-fechaDeVenta')
    paginator = Paginator(ventas, 10)  
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'ventas/regVentas.html', {'page_obj': page_obj})

@login_required
def agregarVenta(request):
    if request.method == 'POST':
        ventaForm = FormularioVenta(request.POST)
        detalleVentaFormset = DetalleVentaFormSet(request.POST)
        
        if ventaForm.is_valid() and detalleVentaFormset.is_valid():
            venta = ventaForm.save(commit=False)  # No guardar todavía la venta
            venta.save()  
            totalVenta = 0
            detalles = detalleVentaFormset.save(commit=False) # No guardar todavía los detalles
            
            for detalle in detalles: 
                detalle.venta = venta
                detalle.subTotal = detalle.cantidad * detalle.block.precioDeVenta
                totalVenta += detalle.subTotal
                block = detalle.block
                block.cantidadDisponible -= detalle.cantidad
                block.save() #acá vamos a actualizar la cantidad disponible de cada producto cuando se realice una venta
                detalle.save()  #acá guardamos cada detalle de venta
            
            venta.total = totalVenta
            venta.save() #acá se actualiza la venta con todos los detalles de venta y se actualiza el precio total de la venta
            return redirect('/ventas/regVentas')
    else:
        ventaForm = FormularioVenta()
        detalleVentaFormset = DetalleVentaFormSet()

    return render(request, 'ventas/agregarVentas.html', {'ventaForm': ventaForm,'detalleVentaFormset': detalleVentaFormset,})



@login_required
def obtener_precio_block(request, block_id):
    try:
        block = Block.objects.get(pk=block_id)
        return JsonResponse({'precio': block.precioDeVenta})
    except Block.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

@login_required
def obtener_detalles_venta(request, venta_id):
    try:
        # Obtener la venta y sus detalles
        venta = Venta.objects.get(id=venta_id)
        detalles_venta = DetalleVenta.objects.filter(venta_id=venta_id)

        # Convertir los detalles de la venta a una lista
        detalles = [
            {
                'producto': detalle.block.nombre,
                'cantidad': detalle.cantidad,
                'precioVenta': detalle.block.precioDeVenta,
                'subtotal': detalle.subTotal,
            }
            for detalle in detalles_venta
        ]

        # Devolver los datos como JSON
        return JsonResponse({
            'id': venta.id,
            'fecha': venta.fechaDeVenta.strftime('%d/%m/%Y'),
            'total': venta.total,
            'detalles': detalles,
        })
    except Venta.DoesNotExist:
        return JsonResponse({'error': 'Venta no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@login_required  
def buscarVentas(request):
    ventas = Venta.objects.all()
    fecha_inicio = request.GET.get('busqueda_inicio')
    fecha_fin = request.GET.get('busqueda_fin')
    if fecha_inicio and fecha_fin:
        ventas = ventas.filter(fechaDeVenta__range=[fecha_inicio, fecha_fin])
    elif fecha_inicio:
        ventas = ventas.filter(fechaDeVenta=fecha_inicio)
    elif fecha_fin:
        ventas = ventas.filter(fechaDeVenta=fecha_fin)
    else:
        redirect("/ventas/regGastos")
   
    return render(request, 'ventas/regVentas.html', {'page_obj': ventas, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin})


@login_required
def generarPDFVentas(request):
#ventas = Venta.objects.all()  # Obtener todas las ventas
    ventas = Venta.objects.prefetch_related('detalleVenta').all()

    # Obtener los valores de las fechas desde la solicitud GET
    fecha_inicio = request.GET.get('busqueda_inicio_PDF')
    fecha_fin = request.GET.get('busqueda_fin_PDF')
    
    # Filtrar las ventas si se pasan las fechas
    if fecha_inicio and fecha_fin:
        ventas = ventas.filter(fechaDeVenta__range=[fecha_inicio, fecha_fin])
    elif fecha_inicio:
        ventas = ventas.filter(fechaDeVenta=fecha_inicio)
    elif fecha_fin:
        ventas = ventas.filter(fechaDeVenta=fecha_fin)
        
    template = get_template('ventas/tabla.html')
    
    html = template.render({'ventas': ventas, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin})
    
    fecha_hora_actual = datetime.now().strftime("%d-%m-%Y - %H:%M")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Registro de ventas - {fecha_hora_actual} hs.pdf"'

    pisa_status = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    
    return response
