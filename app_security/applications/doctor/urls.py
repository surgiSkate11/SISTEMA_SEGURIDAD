from django.urls import path

from applications.doctor.views.atenciones import AtencionListView, AtencionCreateView, AtencionUpdateView, \
    AtencionDeleteView, imprimir_receta
from applications.doctor.views.pagos import (
    PagoListView, PagoCreateView, PagoUpdateView, PagoDeleteView, PagoDetailView, PagoPayPalReturnView, imprimir_pago_pdf
)
from applications.doctor.views.citas import (
    CitaMedicaListView, CitaMedicaCreateView, CitaMedicaUpdateView, CitaMedicaDeleteView, CalendarioContenedorView,
    CalendarioMensualView, CalendarioSemanalView, CalendarioDiarioView, horarios_disponibles_ajax, detalle_cita_ajax, calendario_crear_cita
)
from applications.doctor.views.servicios import (
    ServiciosAdicionalesListView, ServiciosAdicionalesCreateView, ServiciosAdicionalesUpdateView, ServiciosAdicionalesDeleteView, ServicioCreateAjaxView
)
from applications.doctor.views.citas import calendario_diario
from applications.doctor.utils.transacciones_pago import crear_orden_paypal
from applications.doctor.views.cita_modal import CitaMedicaCreateModalView
from applications.doctor.views.cita_update_modal import CitaMedicaUpdateModalView
from applications.doctor import views
from applications.doctor.views.horarios import (
    HorarioAtencionListView, HorarioAtencionCreateView, HorarioAtencionUpdateView, HorarioAtencionDeleteView
)

app_name='doctor' # define un espacio de nombre para la aplicacion
urlpatterns = [
    # Rutas  para vistas relacionadas con Doctor
    path('atenciones/', AtencionListView.as_view(), name="atencion_list"),
    path('atenciones/create/', AtencionCreateView.as_view(), name="atencion_create"),
    path('atenciones/update/<int:pk>/', AtencionUpdateView.as_view(), name="atencion_update"),
    path('atenciones/delete/<int:pk>/', AtencionDeleteView.as_view(), name="atencion_delete"),
    path('atenciones/<int:pk>/imprimir/', imprimir_receta, name="imprimir_atencion_pdf"),


    # Rutas para vistas relacionadas con Pagos
    path('pagos/', PagoListView.as_view(), name="pago_list"),
    path('pagos/create/', PagoCreateView.as_view(), name="pago_create"),
    path('pagos/update/<int:pk>/', PagoUpdateView.as_view(), name="pago_update"),
    path('pago/paypal/return/', PagoPayPalReturnView.as_view(), name="pago_paypal_return"),
    path('pagos/<int:pk>/detalle/', PagoDetailView.as_view(), name="pago_detalle"),
    path('pagos/<int:pk>/imprimir/', imprimir_pago_pdf, name="imprimir_pago_pdf"),
    path('pagos/<int:pk>/eliminar/', PagoDeleteView.as_view(), name="pago_delete"),
    path('pagos/paypal/create-order/', crear_orden_paypal, name='pago_paypal_create_order'),

    # Rutas para Citas Médicas
    path('citas/', CitaMedicaListView.as_view(), name="cita_list"),
    path('citas/create/', CitaMedicaCreateView.as_view(), name="cita_create"),
    path('citas/update/<int:pk>/', CitaMedicaUpdateView.as_view(), name="cita_update"),
    path('citas/update/modal/<int:pk>/', CitaMedicaUpdateModalView.as_view(), name='cita_update_modal'),
    path('citas/<int:pk>/eliminar/', CitaMedicaDeleteView.as_view(), name="cita_delete"),
    path('citas/calendario/', CalendarioContenedorView.as_view(), name="calendario"),
    path('citas/calendario/mensual/', CalendarioMensualView.as_view(), name="calendario_mensual"),
    path('citas/calendario/semanal/', CalendarioSemanalView.as_view(), name="calendario_semanal"),
    path('citas/calendario/diario/', CalendarioDiarioView.as_view(), name="calendario_diario"),
    path('citas/create/modal/', CitaMedicaCreateModalView.as_view(), name='cita_create_modal'),


    # Rutas para Servicios Adicionales
    path('servicios/', ServiciosAdicionalesListView.as_view(), name="servicio_list"),
    path('servicios/create/', ServiciosAdicionalesCreateView.as_view(), name="servicio_create"),
    path('servicios/update/<int:pk>/', ServiciosAdicionalesUpdateView.as_view(), name="servicio_update"),
    path('servicios/delete/<int:pk>/', ServiciosAdicionalesDeleteView.as_view(), name="servicio_delete"),
    path('servicios/ajax/create/', ServicioCreateAjaxView.as_view(), name="servicio_create_ajax"),

    # Rutas para Horarios Disponibles
    path('admin/doctor/horarios-disponibles/', horarios_disponibles_ajax, name='horarios_disponibles_ajax'),
    path('horarios_radios_ajax/', horarios_disponibles_ajax, name='horarios_radios_ajax'),
    path('ajax/horarios_disponibles/', horarios_disponibles_ajax, name='ajax_horarios_disponibles'),

    # Rutas para Horarios de Atención
    path('horarios/', HorarioAtencionListView.as_view(), name="horario_list"),
    path('horarios/create/', HorarioAtencionCreateView.as_view(), name="horario_create"),
    path('horarios/update/<int:pk>/', HorarioAtencionUpdateView.as_view(), name="horario_update"),
    path('horarios/delete/<int:pk>/', HorarioAtencionDeleteView.as_view(), name="horario_delete"),
]