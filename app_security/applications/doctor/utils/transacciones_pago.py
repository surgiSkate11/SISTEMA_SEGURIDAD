from django.db import transaction
from applications.doctor.models import Pago, DetallePago
from applications.doctor.utils.auditorias import registrar_auditoria

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
