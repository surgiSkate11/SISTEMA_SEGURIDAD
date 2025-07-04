from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from applications.core.models import Paciente
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.forms.pacientes import PacienteForm
from applications.doctor.utils.auditorias import registrar_auditoria
from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from applications.security.components.sidebar_menu_mixin import SidebarMenuMixin
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

"""  Vista para buscar pacientes mediante AJAX. Por nombres, apellidos, cédula o teléfono. """


@login_required
@permission_required('core.view_paciente', raise_exception=True)
@require_http_methods(["GET"])
def paciente_find(request):
    try:
        # Obtener el parámetro de búsqueda
        query = request.GET.get('q', '').strip()

        # Validar que se proporcione al menos 3 caracteres
        if len(query) < 3:
            return JsonResponse({
                'success': False,
                'message': 'Debe proporcionar al menos 3 caracteres para la búsqueda',
                'pacientes': []
            })

        # Construir la consulta de búsqueda
        # Buscar en nombres, apellidos, cédula, DNI y teléfono
        pacientes_query = Paciente.objects.filter(
            Q(activo=True) & (
                    Q(nombres__icontains=query) |
                    Q(apellidos__icontains=query) |
                    Q(cedula_ecuatoriana__icontains=query) |
                    Q(dni__icontains=query) |
                    Q(telefono__icontains=query)
            )
        ).select_related('tipo_sangre').prefetch_related(
            'atenciones__diagnostico',
            'atenciones__detalles__medicamento'
        ).order_by('apellidos', 'nombres')

        # Limitar resultados para mejorar rendimiento
        pacientes_query = pacientes_query[:20]

        # Convertir a lista de diccionarios
        pacientes_data = []
        for paciente in pacientes_query:
            # Calcular edad
            edad = paciente.edad

            # Obtener atenciones anteriores (últimas 10)
            atenciones = []
            for atencion in paciente.atenciones.all()[:10]:
                # Obtener prescripciones/detalles de esta atención
                detalles = []
                for detalle in atencion.detalles.all():
                    detalle_dict = {
                        'medicamento': detalle.medicamento.nombre if detalle.medicamento else None,
                        'cantidad': detalle.cantidad,
                        'prescripcion': detalle.prescripcion,
                        'duracion_tratamiento': detalle.duracion_tratamiento,
                        'frecuencia_diaria': detalle.frecuencia_diaria,
                    }
                    detalles.append(detalle_dict)

                # Obtener diagnósticos
                diagnosticos = [d.descripcion for d in atencion.diagnostico.all()]

                # Determinar tipo de consulta
                tipo_consulta = "Chequeo"
                if atencion.es_control:
                    tipo_consulta = "Control"
                elif "urgencia" in atencion.motivo_consulta.lower() or "dolor" in atencion.motivo_consulta.lower():
                    tipo_consulta = "Urgencia"

                atencion_dict = {
                    'id': atencion.id,
                    'fecha_atencion': atencion.fecha_atencion.isoformat(),
                    'tipo_consulta': tipo_consulta,

                    # Signos vitales
                    'presion_arterial': atencion.presion_arterial,
                    'pulso': atencion.pulso,
                    'temperatura': float(atencion.temperatura) if atencion.temperatura else None,
                    'frecuencia_respiratoria': atencion.frecuencia_respiratoria,
                    'saturacion_oxigeno': float(atencion.saturacion_oxigeno) if atencion.saturacion_oxigeno else None,
                    'peso': float(atencion.peso) if atencion.peso else None,
                    'altura': float(atencion.altura) if atencion.altura else None,
                    'imc': atencion.calcular_imc,

                    # Contenido de la atención
                    'motivo_consulta': atencion.motivo_consulta,
                    'sintomas': atencion.sintomas,
                    'tratamiento': atencion.tratamiento,
                    'diagnosticos': diagnosticos,
                    'examen_fisico': atencion.examen_fisico,
                    'examenes_enviados': atencion.examenes_enviados,
                    'comentario_adicional': atencion.comentario_adicional,
                    'es_control': atencion.es_control,

                    # Prescripciones
                    'prescripciones': detalles
                }
                atenciones.append(atencion_dict)

            paciente_dict = {
                'id': paciente.id,
                'nombres': paciente.nombres,
                'apellidos': paciente.apellidos,
                'cedula_ecuatoriana': paciente.cedula_ecuatoriana,
                'dni': paciente.dni,
                'fecha_nacimiento': paciente.fecha_nacimiento.isoformat() if paciente.fecha_nacimiento else None,
                'edad': edad,
                'telefono': paciente.telefono,
                'email': paciente.email,
                'sexo': paciente.sexo,
                'estado_civil': paciente.estado_civil,
                'direccion': paciente.direccion,
                'latitud': float(paciente.latitud) if paciente.latitud else None,
                'longitud': float(paciente.longitud) if paciente.longitud else None,
                'tipo_sangre': paciente.tipo_sangre.tipo if paciente.tipo_sangre else None,
                'foto_url': paciente.get_image,

                # Historia clínica
                'antecedentes_personales': paciente.antecedentes_personales,
                'antecedentes_quirurgicos': paciente.antecedentes_quirurgicos,
                'antecedentes_familiares': paciente.antecedentes_familiares,
                'alergias': paciente.alergias,
                'medicamentos_actuales': paciente.medicamentos_actuales,
                'habitos_toxicos': paciente.habitos_toxicos,
                'vacunas': paciente.vacunas,
                'antecedentes_gineco_obstetricos': paciente.antecedentes_gineco_obstetricos,

                # Atenciones anteriores
                'atenciones': atenciones,
                'total_atenciones': paciente.atenciones.count()
            }
            pacientes_data.append(paciente_dict)
        print(pacientes_data)
        return JsonResponse({
            'success': True,
            'pacientes': pacientes_data,
            'total': len(pacientes_data),
            'query': query
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error en la búsqueda: {str(e)}',
            'pacientes': []
        }, status=500)


class PacienteListView(SidebarMenuMixin, PermissionMixin, ListViewMixin, ListView):
    model = Paciente
    template_name = 'core/pacientes/list.html'
    context_object_name = 'pacientes'
    paginate_by = 5
    permission_required = 'view_paciente'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q') or self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(apellido__icontains=search) |
                Q(dni__icontains=search)
            )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string('core/pacientes/_tabla_pacientes.html', context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class PacienteCreateView(SidebarMenuMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'core/pacientes/form.html'
    success_url = reverse_lazy('core:pacientes_list')
    permission_required = 'add_paciente'

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_auditoria(self.request, 'Paciente', self.object.id, 'CREAR')
        messages.success(self.request, f"Paciente '{self.object.nombre}' creado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el paciente. Por favor revisa el formulario.")
        return super().form_invalid(form)


class PacienteUpdateView(SidebarMenuMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'core/pacientes/form.html'
    success_url = reverse_lazy('core:pacientes_list')
    permission_required = 'change_paciente'

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_auditoria(self.request, 'Paciente', self.object.id, 'EDITAR')
        messages.success(self.request, f"Paciente '{self.object.nombre}' actualizado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el paciente. Por favor revisa el formulario.")
        return super().form_invalid(form)


class PacienteDeleteView(SidebarMenuMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = Paciente
    template_name = 'core/pacientes/confirm_delete.html'
    success_url = reverse_lazy('core:paciente_list')
    permission_required = 'delete_paciente'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        object_id = self.object.id
        nombre = self.object.nombre
        try:
            response = super().delete(request, *args, **kwargs)
            registrar_auditoria(request, 'Paciente', object_id, 'ELIMINAR')
            messages.success(request, f"Paciente '{nombre}' eliminado exitosamente.")
            return response
        except Exception as e:
            messages.error(request, f"Error al eliminar el paciente: {e}")
            return self.render_to_response(self.get_context_data(object=self.object))


class PacienteCreateAjaxView(SidebarMenuMixin, PermissionMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'core/pacientes/form_basico.html'
    permission_required = 'add_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Forzar ajax=True si la petición es AJAX o si viene por GET/POST
        is_ajax = self.request.GET.get('ajax') == '1' or self.request.headers.get('x-requested-with') == 'XMLHttpRequest'
        context['ajax'] = kwargs.get('ajax', False) or is_ajax
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        context = self.get_context_data(form=form, ajax=True)
        html = render_to_string(self.template_name, context, request=request)
        return HttpResponse(html)

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            self.object = form.save()
            data = {
                'success': True,
                'paciente': {
                    'id': self.object.id,
                    'nombres': self.object.nombres,
                    'apellidos': self.object.apellidos
                }
            }
            return JsonResponse(data)
        else:
            # DEBUG: Log errors to console
            import sys
            print('PACIENTE AJAX FORM ERRORS:', form.errors.as_json(), file=sys.stderr)
            print('POST DATA:', request.POST.dict(), file=sys.stderr)
            context = self.get_context_data(form=form, ajax=True)
            html = render_to_string(self.template_name, context, request=request)
            return JsonResponse({'success': False, 'html': html})


