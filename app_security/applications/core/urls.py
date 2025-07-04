from django.urls import path
from applications.core.views.tipo_sangre import (
    TipoSangreListView, TipoSangreCreateView, TipoSangreUpdateView, TipoSangreDeleteView
)
from applications.core.views.pacientes import (
    PacienteListView, PacienteCreateView, PacienteUpdateView, PacienteDeleteView, PacienteCreateAjaxView
)
from applications.core.views.especialidad import (
    EspecialidadListView, EspecialidadCreateView, EspecialidadUpdateView, EspecialidadDeleteView
)
from applications.core.views.doctor import (
    DoctorListView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView
)
from applications.core.views.cargo import (
    CargoListView, CargoCreateView, CargoUpdateView, CargoDeleteView
)
from applications.core.views.empleado import (
    EmpleadoListView, EmpleadoCreateView, EmpleadoUpdateView, EmpleadoDeleteView
)
from applications.core.views.tipo_medicamento import (
    TipoMedicamentoListView, TipoMedicamentoCreateView, TipoMedicamentoUpdateView, TipoMedicamentoDeleteView
)
from applications.core.views.marca_medicamento import (
    MarcaMedicamentoListView, MarcaMedicamentoCreateView, MarcaMedicamentoUpdateView, MarcaMedicamentoDeleteView
)
from applications.core.views.medicamento import (
    MedicamentoListView, MedicamentoCreateView, MedicamentoUpdateView, MedicamentoDeleteView
)
from applications.core.views.diagnostico import (
    DiagnosticoListView, DiagnosticoCreateView, DiagnosticoUpdateView, DiagnosticoDeleteView
)
from applications.core.views.tipo_gasto import (
    TipoGastoListView, TipoGastoCreateView, TipoGastoUpdateView, TipoGastoDeleteView
)
from applications.core.views.gasto_mensual import (
    GastoMensualListView, GastoMensualCreateView, GastoMensualUpdateView, GastoMensualDeleteView
)
from applications.core.views.paciente_find import paciente_find
from applications.core.views.foto_paciente import (
    FotoPacienteListView, FotoPacienteDeleteView
)

app_name = 'core'
urlpatterns = [
    # TipoSangre
    path('tiposangre/', TipoSangreListView.as_view(), name='tiposangre_list'),
    path('tiposangre/nuevo/', TipoSangreCreateView.as_view(), name='tiposangre_create'),
    path('tiposangre/<int:pk>/editar/', TipoSangreUpdateView.as_view(), name='tiposangre_update'),
    path('tiposangre/<int:pk>/eliminar/', TipoSangreDeleteView.as_view(), name='tiposangre_delete'),

    # Paciente
    path('pacientes/', PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/nuevo/', PacienteCreateView.as_view(), name='paciente_create'),
    path('pacientes/nuevo/ajax/', PacienteCreateAjaxView.as_view(), name='paciente_create_ajax'),
    path('pacientes/<int:pk>/editar/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('pacientes/<int:pk>/eliminar/', PacienteDeleteView.as_view(), name='paciente_delete'),
    path('paciente_find/', paciente_find, name='paciente_find'),

    # Especialidad
    path('especialidad/', EspecialidadListView.as_view(), name='especialidad_list'),
    path('especialidad/nuevo/', EspecialidadCreateView.as_view(), name='especialidad_create'),
    path('especialidad/<int:pk>/editar/', EspecialidadUpdateView.as_view(), name='especialidad_update'),
    path('especialidad/<int:pk>/eliminar/', EspecialidadDeleteView.as_view(), name='especialidad_delete'),

    # Doctor
    path('doctor/', DoctorListView.as_view(), name='doctor_list'),
    path('doctor/nuevo/', DoctorCreateView.as_view(), name='doctor_create'),
    path('doctor/<int:pk>/editar/', DoctorUpdateView.as_view(), name='doctor_update'),
    path('doctor/<int:pk>/eliminar/', DoctorDeleteView.as_view(), name='doctor_delete'),

    # Cargo
    path('cargo/', CargoListView.as_view(), name='cargo_list'),
    path('cargo/nuevo/', CargoCreateView.as_view(), name='cargo_create'),
    path('cargo/<int:pk>/editar/', CargoUpdateView.as_view(), name='cargo_update'),
    path('cargo/<int:pk>/eliminar/', CargoDeleteView.as_view(), name='cargo_delete'),

    # Empleado
    path('empleado/', EmpleadoListView.as_view(), name='empleado_list'),
    path('empleado/nuevo/', EmpleadoCreateView.as_view(), name='empleado_create'),
    path('empleado/<int:pk>/editar/', EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('empleado/<int:pk>/eliminar/', EmpleadoDeleteView.as_view(), name='empleado_delete'),

    # TipoMedicamento
    path('tipo_medicamento/', TipoMedicamentoListView.as_view(), name='tipo_medicamento_list'),
    path('tipo_medicamento/nuevo/', TipoMedicamentoCreateView.as_view(), name='tipo_medicamento_create'),
    path('tipo_medicamento/<int:pk>/editar/', TipoMedicamentoUpdateView.as_view(), name='tipo_medicamento_update'),
    path('tipo_medicamento/<int:pk>/eliminar/', TipoMedicamentoDeleteView.as_view(), name='tipo_medicamento_delete'),

    # MarcaMedicamento
    path('marca_medicamento/', MarcaMedicamentoListView.as_view(), name='marca_medicamento_list'),
    path('marca_medicamento/nuevo/', MarcaMedicamentoCreateView.as_view(), name='marca_medicamento_create'),
    path('marca_medicamento/<int:pk>/editar/', MarcaMedicamentoUpdateView.as_view(), name='marca_medicamento_update'),
    path('marca_medicamento/<int:pk>/eliminar/', MarcaMedicamentoDeleteView.as_view(), name='marca_medicamento_delete'),

    # Medicamento
    path('medicamento/', MedicamentoListView.as_view(), name='medicamento_list'),
    path('medicamento/nuevo/', MedicamentoCreateView.as_view(), name='medicamento_create'),
    path('medicamento/<int:pk>/editar/', MedicamentoUpdateView.as_view(), name='medicamento_update'),
    path('medicamento/<int:pk>/eliminar/', MedicamentoDeleteView.as_view(), name='medicamento_delete'),

    # Diagnostico
    path('diagnostico/', DiagnosticoListView.as_view(), name='diagnostico_list'),
    path('diagnostico/nuevo/', DiagnosticoCreateView.as_view(), name='diagnostico_create'),
    path('diagnostico/<int:pk>/editar/', DiagnosticoUpdateView.as_view(), name='diagnostico_update'),
    path('diagnostico/<int:pk>/eliminar/', DiagnosticoDeleteView.as_view(), name='diagnostico_delete'),

    # TipoGasto
    path('tipo_gasto/', TipoGastoListView.as_view(), name='tipo_gasto_list'),
    path('tipo_gasto/nuevo/', TipoGastoCreateView.as_view(), name='tipo_gasto_create'),
    path('tipo_gasto/<int:pk>/editar/', TipoGastoUpdateView.as_view(), name='tipo_gasto_update'),
    path('tipo_gasto/<int:pk>/eliminar/', TipoGastoDeleteView.as_view(), name='tipo_gasto_delete'),

    # GastoMensual
    path('gasto_mensual/', GastoMensualListView.as_view(), name='gasto_mensual_list'),
    path('gasto_mensual/nuevo/', GastoMensualCreateView.as_view(), name='gasto_mensual_create'),
    path('gasto_mensual/<int:pk>/editar/', GastoMensualUpdateView.as_view(), name='gasto_mensual_update'),
    path('gasto_mensual/<int:pk>/eliminar/', GastoMensualDeleteView.as_view(), name='gasto_mensual_delete'),

    # Galería de fotos de pacientes
    path('pacientes/<int:paciente_id>/galeriafotos/', FotoPacienteListView.as_view(), name='galeriafotos'),
    path('pacientes/<int:paciente_id>/galeriafotos/<int:pk>/eliminar/', FotoPacienteDeleteView.as_view(), name='eliminar_foto'),
]