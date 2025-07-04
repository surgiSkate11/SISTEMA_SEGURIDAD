from applications.core.models import Paciente, TipoSangre
from applications.doctor.models import HorarioAtencion, CitaMedica, Atencion, Pago
from applications.core.models import Doctor
from django.utils import timezone
from datetime import time, date, timedelta

# Obtener el primer doctor
primer_doctor = Doctor.objects.first()

# Obtener un tipo de sangre existente
primer_tipo_sangre = TipoSangre.objects.first()

# Crear 5 pacientes
pacientes = []
for i in range(5):
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
        tipo_sangre=primer_tipo_sangre
    )
    pacientes.append(paciente)

# Crear 5 horarios de atención para el primer doctor
from applications.doctor.utils.doctor import DiaSemanaChoices

dias = [c[0] for c in DiaSemanaChoices.choices][:5]
for i in range(5):
    HorarioAtencion.objects.create(
        doctor=primer_doctor,
        dia_semana=dias[i],
        hora_inicio=time(8, 0),
        hora_fin=time(16, 0)
    )

# Crear 5 citas médicas y 5 atenciones para el primer paciente
for i in range(5):
    cita = CitaMedica.objects.create(
        paciente=pacientes[0],
        fecha=timezone.now().date() + timedelta(days=i+1),
        hora_cita=time(9+i, 0),
        estado="PENDIENTE"
    )
    Atencion.objects.create(
        paciente=pacientes[0],
        created_by=primer_doctor.user if hasattr(primer_doctor, 'user') else primer_doctor,
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

# Crear 10 tipos de medicamento
from applications.core.models import TipoMedicamento, MarcaMedicamento, Medicamento

tipos_medicamento = []
for i in range(10):
    tm = TipoMedicamento.objects.create(nombre=f"TipoMed{i+1}", descripcion=f"Tipo de medicamento {i+1}")
    tipos_medicamento.append(tm)

# Crear 10 marcas de medicamento
marcas_medicamento = []
for i in range(10):
    mm = MarcaMedicamento.objects.create(nombre=f"MarcaMed{i+1}", descripcion=f"Marca de medicamento {i+1}")
    marcas_medicamento.append(mm)

# Crear 10 medicamentos
for i in range(10):
    Medicamento.objects.create(
        tipo=tipos_medicamento[i],
        marca_medicamento=marcas_medicamento[i],
        nombre=f"Medicamento{i+1}",
        descripcion=f"Descripción del medicamento {i+1}",
        concentracion="500mg",
        via_administracion="oral",
        cantidad=100+i,
        precio=10.5+i,
        comercial=True
    )

# Crear 10 pagos
for i in range(10):
    Pago.objects.create(
        atencion=Atencion.objects.order_by('?').first(),
        metodo_pago="efectivo",
        monto_total=50.0 + i * 10,
        estado="pendiente"
    )

# Mostrar todos los datos creados
print('Pacientes:')
for p in Paciente.objects.all():
    print(p)

print('\nHorarios de Atención:')
for h in HorarioAtencion.objects.all():
    print(h)

print('\nCitas Médicas:')
for c in CitaMedica.objects.all():
    print(c)

print('\nAtenciones:')
for a in Atencion.objects.all():
    print(a)

print('\nTipos de Medicamento:')
for tm in TipoMedicamento.objects.all():
    print(tm)

print('\nMarcas de Medicamento:')
for mm in MarcaMedicamento.objects.all():
    print(mm)

print('\nMedicamentos:')
for m in Medicamento.objects.all():
    print(m)

print('\nPagos:')
for p in Pago.objects.all():
    print(p)
