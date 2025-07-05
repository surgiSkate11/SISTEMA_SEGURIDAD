from django.db import transaction
from applications.doctor.models import Pago, DetallePago
from applications.doctor.utils.auditorias import registrar_auditoria
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from applications.doctor.utils.paypal_api import PayPalAPI

def crear_pago_con_detalles(request, data_pago, detalles_data):
    """
    Crea un Pago y sus DetallePago de forma atómica y registra auditoría.
    data_pago: dict con los campos del modelo Pago (excepto monto_total).
    detalles_data: lista de dicts, cada uno con los campos de DetallePago.
    Retorna el objeto Pago creado.
    Lanza excepción si algo falla.
    """
    with transaction.atomic():
        pago = Pago.objects.create(**data_pago)
        total = 0
        for detalle in detalles_data:
            detalle['pago'] = pago
            detalle_pago = DetallePago.objects.create(**detalle)
            total += float(detalle_pago.subtotal)
        pago.monto_total = total
        pago.save()
        registrar_auditoria(request, 'Pago', pago.id, 'CREAR')
        return pago

def actualizar_pago_con_detalles(request, pago_id, data_pago, detalles_data):
    """
    Actualiza un Pago y sus DetallePago de forma atómica y registra auditoría.
    Borra los detalles antiguos y crea los nuevos.
    """
    with transaction.atomic():
        pago = Pago.objects.get(id=pago_id)
        for attr, value in data_pago.items():
            setattr(pago, attr, value)
        pago.save()
        # Eliminar detalles antiguos
        pago.detalles.all().delete()
        total = 0
        for detalle in detalles_data:
            detalle['pago'] = pago
            detalle_pago = DetallePago.objects.create(**detalle)
            total += float(detalle_pago.subtotal)
        pago.monto_total = total
        pago.save()
        registrar_auditoria(request, 'Pago', pago.id, 'EDITAR')
        return pago

def crear_orden_paypal(request):
    """
    Endpoint AJAX para crear una orden PayPal y devolver el orderID.
    Espera POST con 'monto' (float o str) y opcional 'currency'.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        monto = request.POST.get('monto')
        try:
            monto = float(monto)
        except (TypeError, ValueError):
            monto = 0
        currency = request.POST.get('currency', None)
        if monto <= 0:
            return JsonResponse({'error': 'Monto inválido'}, status=400)
        paypal = PayPalAPI()
        # URLs de retorno/cancelación
        from django.urls import reverse
        return_url = request.build_absolute_uri(reverse('doctor:pago_paypal_return'))
        cancel_url = request.build_absolute_uri(reverse('doctor:pago_list'))
        order = paypal.create_order(monto, currency, return_url, cancel_url)
        return JsonResponse({'orderID': order['id']})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
