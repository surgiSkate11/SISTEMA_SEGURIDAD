from applications.security.models import AuditUser
from datetime import date
from django.utils import timezone

def registrar_auditoria(request, tabla, registroid, accion, estacion="Desconocida"):
    """
    Registra una acción de auditoría para cualquier modelo.
    - tabla: nombre de la tabla o modelo (str)
    - registroid: id del registro afectado (int)
    - accion: acción realizada (str, debe estar en AccionChoices)
    - estacion: nombre del equipo o estación (opcional)
    """
    AuditUser.objects.create(
        usuario=request.user,
        tabla=tabla,
        registroid=registroid,
        accion=accion,
        fecha=date.today(),
        hora=timezone.now().time(),
        estacion=estacion
    )
