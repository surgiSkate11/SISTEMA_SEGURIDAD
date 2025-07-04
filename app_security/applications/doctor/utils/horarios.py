from datetime import datetime, timedelta
from django.utils import timezone

def generar_horas_disponibles(horario, fecha, citas_ocupadas=None, intervalo_minutos=30):
    """
    Genera una lista de horas disponibles para agendar, omitiendo el intervalo bloqueado y las horas ocupadas.
    Usa la fecha proporcionada para construir datetimes precisos.
    """
    horas = []
    inicio = datetime.combine(fecha, horario.hora_inicio)
    fin = datetime.combine(fecha, horario.hora_fin)
    bloquea_desde = horario.intervalo_desde
    bloquea_hasta = horario.intervalo_hasta
    citas_ocupadas = citas_ocupadas or []

    actual = inicio
    now = timezone.localtime()  # para comparación segura

    while actual < fin:
        hora_actual = actual.time()
        if not (bloquea_desde and bloquea_hasta and bloquea_desde <= hora_actual < bloquea_hasta):
            if hora_actual not in citas_ocupadas:
                # Solo permitir horas futuras si es hoy
                if fecha > now.date() or (fecha == now.date() and actual.time() > now.time()):
                    horas.append(hora_actual)
        actual += timedelta(minutes=intervalo_minutos)
    return horas


def obtener_horarios_disponibles_para_fecha(doctor, fecha, citas_ocupadas=None, intervalo_minutos=30):
    """
    Devuelve la lista de horas disponibles para un doctor y una fecha específica.
    """
    dia_semana = fecha.strftime('%A').lower()
    from applications.doctor.models import HorarioAtencion
    horario = HorarioAtencion.objects.filter(doctor=doctor, dia_semana=dia_semana, activo=True).first()
    if not horario:
        return []
    return generar_horas_disponibles(horario, fecha, citas_ocupadas, intervalo_minutos)
