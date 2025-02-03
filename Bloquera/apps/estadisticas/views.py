from django.shortcuts import render
from apps.ventas.models import DetalleVenta, Venta
from apps.gastos.models import Gasto
from datetime import date
from django.db.models import Sum
from django.http import JsonResponse
from calendar import monthrange
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required


@login_required
def estadisticas(request):
    fecha_diaria = date.today()
    ventas_diarias = Venta.objects.filter(fechaDeVenta=fecha_diaria)
    total_diarias = ventas_diarias.aggregate(total_sum=Sum('total'))['total_sum'] or 0

    inicio_semana = fecha_diaria - timedelta(days=fecha_diaria.weekday())  # Lunes de la semana
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana
    ventas_semanales = Venta.objects.filter(fechaDeVenta__range=[inicio_semana, fin_semana])
    total_ventas_semanales = ventas_semanales.aggregate(total_sum=Sum('total'))['total_sum'] or 0

    year = fecha_diaria.year
    month = fecha_diaria.month
    inicio_mes = date(year, month, 1)  # Primer día del mes
    fin_mes = date(year, month, monthrange(year, month)[1])  # Último día del mes
    ventas_mensuales = Venta.objects.filter(fechaDeVenta__range=[inicio_mes, fin_mes])
    total_ventas_mensuales = ventas_mensuales.aggregate(total_sum=Sum('total'))['total_sum'] or 0
    
    gastos_mensuales = Gasto.objects.filter(fecha__range=[inicio_mes, fin_mes])
    total_gastos_mensuales = gastos_mensuales.aggregate(monto_sum=Sum('monto'))['monto_sum'] or 0
    
    contexto = {
        'totalVentas': total_diarias,
        'totalVentasSemanales': total_ventas_semanales,
        'totalVentasMensuales': total_ventas_mensuales,
        'totalGastosMensuales':total_gastos_mensuales,
    }

    return render(request, 'estadisticas/estadisticas.html', contexto)

@login_required
def ventas_mensuales(request):
    # Fecha actual
    hoy = date.today()
    year = hoy.year
    month = hoy.month

    # Número de días en el mes actual
    num_days = monthrange(year, month)[1]
    # Inicializa un diccionario para almacenar ventas por día
    ventas_dias = [0] * num_days

    # Filtrar las ventas del mes actual
    ventas = Venta.objects.filter(
        fechaDeVenta__year=year,
        fechaDeVenta__month=month
    ).values('fechaDeVenta').annotate(total_dia=Sum('total'))

    # Procesa las ventas y llena el diccionario por día
    for venta in ventas:
        day = venta['fechaDeVenta'].day - 1
        ventas_dias[day] = venta['total_dia']

    # Devuelve los datos como JSON
    return JsonResponse({'labels': list(range(1, num_days + 1)), 'data': ventas_dias})

from django.db.models import Sum

def productos_mas_vendidos(request):
    productos = (
        DetalleVenta.objects.values('block__nombre')  # Agrupa por nombre del producto
        .annotate(total_cantidad=Sum('cantidad'))  # Calcula la cantidad total de cada producto
        .order_by('-total_cantidad')  # Ordena por cantidad descendente
    )

    # Calcula el total vendido
    total_cantidad = sum([p['total_cantidad'] for p in productos])

    # Calcula el porcentaje para cada producto
    datos = {
        'labels': [p['block__nombre'] for p in productos],
        'data': [
            round((p['total_cantidad'] / total_cantidad) * 100, 2) for p in productos
        ],
    }

    return JsonResponse(datos)
