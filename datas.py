from app_security.applications.core.models import Paciente, TipoSangre, Especialidad, Empleado, Medicamento, Diagnostico, Doctor
from app_security.applications.core.models import HorarioAtencion, CitaMedica, Atencion, ServiciosAdicionales, Pago, DetallePago
from django.utils import timezone
from datetime import time, date
from django.contrib.auth import get_user_model
import random

User = get_user_model()

# Crear 8 tipos de sangre
for i in range(8):
    try:
        TipoSangre.objects.create(nombre=f"TipoSangre{i+1}")
    except Exception:
        pass

tipos_sangre = list(TipoSangre.objects.all())

# Crear 8 especialidades
for i in range(8):
    try:
        Especialidad.objects.create(nombre=f"Especialidad{i+1}")
    except Exception:
        pass

especialidades = list(Especialidad.objects.all())

# Crear 8 empleados (usuarios)
for i in range(8):
    try:
        user, _ = User.objects.get_or_create(username=f"empleado{i+1}", defaults={"email":f"empleado{i+1}@mail.com"})
        Empleado.objects.create(nombre=f"Empleado{i+1}", user=user)
    except Exception:
        pass

empleados = list(Empleado.objects.all())

# Crear 8 doctores
for i in range(8):
    try:
        Doctor.objects.create(nombre=f"Doctor{i+1}", especialidad=random.choice(especialidades))
    except Exception:
        pass

doctores = list(Doctor.objects.all())

# Crear 8 pacientes
pacientes = []
for i in range(8):
    try:
        paciente = Paciente.objects.create(
            nombres=f"Nombre{i+1}",
            apellidos=f"Apellido{i+1}",
            cedula_ecuatoriana=f"01020304{i+1}",
            fecha_nacimiento=f"199{i}-01-01",
            telefono=f"099000000{i+1}",
            email=f"paciente{i+1}@mail.com",
            sexo="M" if i % 2 == 0 else "F",
            estado_civil="SOLTERO",
            direccion=f"Calle {i+1}",
            tipo_sangre=random.choice(tipos_sangre)
        )
        pacientes.append(paciente)
    except Exception:
        pass

# Crear 8 medicamentos
for i in range(8):
    try:
        Medicamento.objects.create(nombre=f"Medicamento{i+1}", cantidad=10+i, precio=5.5+i)
    except Exception:
        pass

# Crear 8 diagnósticos
for i in range(8):
    try:
        Diagnostico.objects.create(paciente=random.choice(pacientes), descripcion=f"Diagnóstico {i+1}")
    except Exception:
        pass

# Crear 8 servicios adicionales
for i in range(8):
    try:
        ServiciosAdicionales.objects.create(nombre_servicio=f"Servicio{i+1}", precio=10+i)
    except Exception:
        pass

servicios = list(ServiciosAdicionales.objects.all())

# Crear 8 horarios de atención para los doctores
from applications.doctor.utils.doctor import DiaSemanaChoices
dias = [c[0] for c in DiaSemanaChoices.choices][:8]
for i in range(8):
    try:
        HorarioAtencion.objects.create(
            doctor=random.choice(doctores),
            dia_semana=dias[i % len(dias)],
            hora_inicio=time(8, 0),
            hora_fin=time(16, 0)
        )
    except Exception:
        pass

# Crear 8 citas médicas y 8 atenciones para pacientes
for i in range(8):
    try:
        cita = CitaMedica.objects.create(
            paciente=random.choice(pacientes),
            fecha=date(2025, 7, (i % 28) + 1),
            hora_cita=time(9+i, 0),
            estado="PENDIENTE"
        )
        Atencion.objects.create(
            paciente=cita.paciente,
            created_by=random.choice(doctores).user if hasattr(random.choice(doctores), 'user') else None,
            presion_arterial="120/80",
            pulso=70+i,
            temperatura=36.5,
            frecuencia_respiratoria=16,
            saturacion_oxigeno=98.0,
            peso=70.0+i,
            altura=1.70,
            motivo_consulta=f"Consulta motivo {i+1}",
            sintomas=f"Síntomas ejemplo {i+1}",
            tratamiento=f"Tratamiento ejemplo {i+1}"
        )
    except Exception:
        pass

# Crear 8 pagos y 8 detalles de pago
for i in range(8):
    try:
        pago = Pago.objects.create(
            paciente=random.choice(pacientes),
            monto_total=100+i*10,
            metodo_pago="EFECTIVO",
            estado="PENDIENTE"
        )
        for j in range(2):
            DetallePago.objects.create(
                pago=pago,
                descripcion=f"Detalle {j+1} del pago {i+1}",
                monto=50+j*10
            )
    except Exception:
        pass

print('Datos de prueba creados para todos los modelos principales de core y doctor.')
