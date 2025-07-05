from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Q
from applications.doctor.models import CitaMedica, HorarioAtencion
from applications.doctor.forms.citas import CitaMedicaForm
from applications.security.components.sidebar_menu_mixin import SidebarMenuMixin
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from applications.core.models import Doctor
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
import datetime
from django.contrib import messages
from django.contrib.auth.models import Group
import calendar
from datetime import date, timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from applications.doctor.utils.auditorias import registrar_auditoria
from applications.doctor.utils.cita_medica import EstadoCitaChoices
from applications.doctor.utils.horarios import obtener_horarios_disponibles_para_fecha
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest
from applications.doctor.forms.citas import CitaMedicaForm

def get_unique_doctor():
    """Obtiene el único doctor asociado al usuario autenticado que pertenece al grupo 'Médico'."""
    return Doctor.objects.filter(user__groups__name='Médico').first()


class CitaListView(SidebarMenuMixin, PermissionMixin, ListViewMixin, ListView):
    model = CitaMedica
    template_name = 'doctor/citas/list.html'
    context_object_name = 'citas'
    paginate_by = 5
    permission_required = 'view_cita'

    def get_queryset(self):
        queryset = super().get_queryset()
        # --- ACTUALIZAR ESTADO DE CITAS OCUPADAS CUYA FECHA Y HORA YA PASARON ---
        from django.utils import timezone
        from datetime import datetime
        now = timezone.localtime()
        citas_ocupadas = queryset.filter(estado=EstadoCitaChoices.OCUPADO)
        for cita in citas_ocupadas:
            cita_datetime = datetime.combine(cita.fecha, cita.hora_cita)
            cita_datetime = timezone.make_aware(cita_datetime, now.tzinfo)
            if cita_datetime <= now:
                cita.estado = EstadoCitaChoices.ATENDIDO
                cita.save(update_fields=["estado"])
        # --- FIN ACTUALIZACIÓN AUTOMÁTICA ---
        search = self.request.GET.get('q') or self.request.GET.get('search', '')
        mes = self.request.GET.get('mes')
        anio = self.request.GET.get('anio')
        if search:
            queryset = queryset.filter(
                Q(paciente__nombre__icontains=search) |
                Q(fecha__icontains=search)
            )
        if mes and mes.isdigit():
            queryset = queryset.filter(fecha__month=int(mes))
        if anio and anio.isdigit():
            queryset = queryset.filter(fecha__year=int(anio))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener todos los años y meses de todas las citas (sin filtrar por usuario ni doctor)
        years = CitaMedica.objects.dates('fecha', 'year', order='DESC')
        context['available_years'] = sorted(set([d.year for d in years]))
        # Obtener meses únicos de todas las citas
        months = CitaMedica.objects.dates('fecha', 'month', order='ASC')
        meses_unicos = sorted(set((d.month for d in months)))
        # Lista de tuplas (num, nombre) solo para los meses que existen en la BD
        meses_nombres = [
            (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
            (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
            (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
        ]
        context['meses'] = [(num, nombre) for num, nombre in meses_nombres if num in meses_unicos]
        # Mes y año seleccionados
        selected_year = self.request.GET.get('anio')
        selected_month = self.request.GET.get('mes')
        hoy = timezone.now().date()
        if not selected_year:
            selected_year = str(hoy.year)
        if not selected_month:
            selected_month = str(hoy.month)
        context['selected_year'] = int(selected_year)
        context['selected_month'] = int(selected_month)
        # Total de citas para el header (usar queryset sin paginación ni filtro)
        context['total_citas'] = CitaMedica.objects.count()
        # Debug en template
        context['debug_available_years'] = context['available_years']
        context['debug_meses'] = context['meses']
        return context

    def render_to_response(self, context, **response_kwargs):
        from django.contrib.messages import get_messages
        context['messages'] = get_messages(self.request)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string('doctor/citas/_tabla_citas.html', context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)

class CitaCreateView(SidebarMenuMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = CitaMedica
    form_class = CitaMedicaForm
    template_name = 'doctor/citas/form.html'
    success_url = reverse_lazy('doctor:citas_list')
    permission_required = 'add_cita'

    def dispatch(self, request, *args, **kwargs):
        # Si viene desde el calendario (tiene fecha y hora) y no es AJAX, redirigir al flujo premium reducido
        if request.method == 'GET' and not (request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax') == '1'):
            fecha = request.GET.get('fecha')
            hora = request.GET.get('hora') or request.GET.get('hora_cita')
            if fecha and hora:
                from django.urls import reverse
                from django.http import HttpResponseRedirect
                url = f"{reverse('doctor:cita_create_modal')}?ajax=1&fecha={fecha}&hora={hora}"
                next_param = request.GET.get('next')
                if next_param:
                    url += f"&next={next_param}"
                return HttpResponseRedirect(url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_auditoria(self.request, 'Cita', self.object.id, 'CREAR')
        messages.success(self.request, f"Cita registrada exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al registrar la cita. Por favor revisa el formulario.")
        return super().form_invalid(form)

    def get_success_url(self):
        next_view = self.request.GET.get('next') or self.request.POST.get('next') or self.request.GET.get('view')
        if next_view in ['diario', 'calendar']:
            return reverse('doctor:calendario_diario')
        elif next_view == 'semanal':
            return reverse('doctor:calendario_semanal')
        elif next_view == 'mensual':
            return reverse('doctor:calendario_mensual')
        elif next_view == 'list':
            return reverse('doctor:cita_list')
        # Valor por defecto seguro
        return reverse('doctor:calendario_diario')
        

class CitaUpdateView(SidebarMenuMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = CitaMedica
    form_class = CitaMedicaForm
    template_name = 'doctor/citas/form.html'
    success_url = reverse_lazy('doctor:citas_list')
    permission_required = 'change_cita'

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_auditoria(self.request, 'Cita', self.object.id, 'EDITAR')
        messages.success(self.request, f"Cita actualizada exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar la cita. Por favor revisa el formulario.")
        return super().form_invalid(form)

    def get_success_url(self):
        next_view = self.request.GET.get('next') or self.request.POST.get('next') or self.request.GET.get('view')
        if next_view == 'diario':
            return reverse('doctor:calendario_diario')
        elif next_view == 'semanal':
            return reverse('doctor:calendario_semanal')
        elif next_view == 'mensual':
            return reverse('doctor:calendario_mensual')
        elif next_view == 'list':
            return reverse('doctor:cita_list')
        # Valor por defecto seguro
        return reverse('doctor:calendario_diario')
        

class CitaDeleteView(SidebarMenuMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = CitaMedica
    template_name = 'doctor/citas/confirm_delete.html'
    success_url = reverse_lazy('doctor:citas_list')
    permission_required = 'delete_cita'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        object_id = self.object.id
        try:
            response = super().delete(request, *args, **kwargs)
            registrar_auditoria(request, 'Cita', object_id, 'ELIMINAR')
            messages.success(request, f"Cita eliminada exitosamente.")
            return response
        except Exception as e:
            messages.error(request, f"Error al eliminar la cita: {e}")
            return self.render_to_response(self.get_context_data(object=self.object))

    def render_to_response(self, context, **response_kwargs):
        from django.contrib.messages import get_messages
        context['messages'] = get_messages(self.request)
        return super().render_to_response(context, **response_kwargs)

    def get_success_url(self):
        next_view = self.request.GET.get('next') or self.request.POST.get('next') or self.request.GET.get('view')
        if next_view == 'diario':
            return reverse('doctor:calendario_diario')
        elif next_view == 'semanal':
            return reverse('doctor:calendario_semanal')
        elif next_view == 'mensual':
            return reverse('doctor:calendario_mensual')
        elif next_view == 'list':
            return reverse('doctor:cita_list')
        # Valor por defecto seguro
        return reverse('doctor:cita_list')
        

class CitaMedicaListView(SidebarMenuMixin, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CitaMedica
    template_name = 'doctor/citas/list.html'
    context_object_name = 'citas'
    paginate_by = 10
    permission_required = 'doctor.view_citamedica'

    def get_queryset(self):
        queryset = super().get_queryset()
        # --- ACTUALIZAR ESTADO DE CITAS OCUPADAS CUYA FECHA Y HORA YA PASARON ---
        from django.utils import timezone
        from datetime import datetime
        now = timezone.localtime()
        citas_ocupadas = queryset.filter(estado=EstadoCitaChoices.OCUPADO)
        for cita in citas_ocupadas:
            cita_datetime = datetime.combine(cita.fecha, cita.hora_cita)
            cita_datetime = timezone.make_aware(cita_datetime, now.tzinfo)
            if cita_datetime <= now:
                cita.estado = EstadoCitaChoices.ATENDIDO
                cita.save(update_fields=["estado"])
        # --- FIN ACTUALIZACIÓN AUTOMÁTICA ---
        q = self.request.GET.get('q', '')
        if q:
            queryset = queryset.filter(
                Q(paciente__nombres__icontains=q) |
                Q(paciente__apellidos__icontains=q) |
                Q(paciente__cedula_ecuatoriana__icontains=q) |
                Q(paciente__dni__icontains=q)
            )
        return queryset.order_by('-fecha', '-hora_cita')

    def render_to_response(self, context, **response_kwargs):
        from django.contrib.messages import get_messages
        context['messages'] = get_messages(self.request)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('doctor/citas/_tabla_citas.html', context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)

class CitaMedicaCreateView(SidebarMenuMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CitaMedica
    form_class = CitaMedicaForm
    template_name = 'doctor/citas/form.html'
    permission_required = 'doctor.add_citamedica'

    def dispatch(self, request, *args, **kwargs):
        # Si viene desde el calendario (tiene fecha y hora) y no es AJAX, redirigir al flujo premium reducido
        if request.method == 'GET' and not (request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax') == '1'):
            fecha = request.GET.get('fecha')
            hora = request.GET.get('hora') or request.GET.get('hora_cita')
            if fecha and hora:
                from django.urls import reverse
                from django.http import HttpResponseRedirect
                url = f"{reverse('doctor:cita_create_modal')}?ajax=1&fecha={fecha}&hora={hora}"
                next_param = request.GET.get('next')
                if next_param:
                    url += f"&next={next_param}"
                return HttpResponseRedirect(url)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Preseleccionar fecha si viene por GET
        fecha = self.request.GET.get('fecha')
        if fecha:
            kwargs['initial'] = kwargs.get('initial', {})
            kwargs['initial']['fecha'] = fecha
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = Doctor.objects.filter(activo=True).first()
        context['doctor_id'] = doctor.id if doctor else None
        return context

    def get_success_url(self):
        next_view = self.request.GET.get('next') or self.request.POST.get('next') or self.request.GET.get('view')
        if next_view == 'diario':
            return reverse('doctor:calendario_diario')
        elif next_view == 'semanal':
            return reverse('doctor:calendario_semanal')
        elif next_view == 'mensual':
            return reverse('doctor:calendario_mensual')
        elif next_view == 'list':
            return reverse('doctor:cita_list')
        # Valor por defecto seguro
        return reverse('doctor:cita_list')

    def form_valid(self, form):
        # Asignar el doctor logueado
        form.instance.doctor = get_unique_doctor()
        try:
            response = super().form_valid(form)
            messages.success(self.request, "Cita médica creada correctamente.")
            return redirect(self.get_success_url())
        except ValueError as e:
            form.add_error(None, str(e))
            messages.error(self.request, str(e))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Por favor corrige los errores en el formulario.")
        return super().form_invalid(form)

    def render_to_response(self, context, **response_kwargs):
        from django.contrib.messages import get_messages
        context['messages'] = get_messages(self.request)
        return super().render_to_response(context, **response_kwargs)

class CitaMedicaUpdateView(SidebarMenuMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CitaMedica
    form_class = CitaMedicaForm
    template_name = 'doctor/citas/form.html'
    permission_required = 'doctor.change_citamedica'

    def get_queryset(self):
        # Solo permitir editar citas del usuario logueado (sin filtrar por doctor)
        qs = super().get_queryset()
        return qs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = Doctor.objects.filter(activo=True).first()
        context['doctor_id'] = doctor.id if doctor else None
        return context

    def get_success_url(self):
        next_view = self.request.GET.get('next') or self.request.POST.get('next') or self.request.GET.get('view')
        if next_view == 'diario':
            return reverse('doctor:calendario_diario')
        elif next_view == 'semanal':
            return reverse('doctor:calendario_semanal')
        elif next_view == 'mensual':
            return reverse('doctor:calendario_mensual')
        elif next_view == 'list':
            return reverse('doctor:cita_list')
        # Valor por defecto seguro
        return reverse('doctor:cita_list')

    def form_valid(self, form):
        # Asegurar que la cita siga perteneciendo al doctor logueado
        form.instance.doctor = get_unique_doctor()
        response = super().form_valid(form)
        messages.success(self.request, "Cita médica actualizada correctamente.")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Por favor corrige los errores en el formulario.")
        return super().form_invalid(form)

    def render_to_response(self, context, **response_kwargs):
        from django.contrib.messages import get_messages
        context['messages'] = get_messages(self.request)
        return super().render_to_response(context, **response_kwargs)

class CitaMedicaDeleteView(SidebarMenuMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CitaMedica
    template_name = 'fragments/delete.html'
    permission_required = 'doctor.delete_citamedica'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def get_success_url(self):
        next_view = self.request.GET.get('next') or self.request.POST.get('next') or self.request.GET.get('view')
        if next_view == 'diario':
            return reverse('doctor:calendario_diario')
        elif next_view == 'semanal':
            return reverse('doctor:calendario_semanal')
        elif next_view == 'mensual':
            return reverse('doctor:calendario_mensual')
        elif next_view == 'list':
            return reverse('doctor:cita_list')
        # Valor por defecto seguro
        return reverse('doctor:cita_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Cita médica eliminada correctamente.")
        return redirect(self.get_success_url())

    def render_to_response(self, context, **response_kwargs):
        from django.contrib.messages import get_messages
        context['messages'] = get_messages(self.request)
        return super().render_to_response(context, **response_kwargs)

class CalendarioContenedorView(SidebarMenuMixin, TemplateView):
    template_name = 'doctor/citas/calendario.html'
    def dispatch(self, request, *args, **kwargs):
        # Redirige siempre a la vista de calendario diario
        return redirect('doctor:calendario_diario')

class CalendarioMensualView(SidebarMenuMixin, TemplateView):
    template_name = 'doctor/citas/calendario_mensual.html'

    def get_context_data(self, **kwargs):
        import calendar
        from datetime import date
        from django.utils import timezone
        context = super().get_context_data(**kwargs)
        hoy = timezone.localdate()
        mes = int(self.request.GET.get('mes', hoy.month))
        anio = int(self.request.GET.get('anio', hoy.year))
        primer_dia = date(anio, mes, 1)
        _, dias_en_mes = calendar.monthrange(anio, mes)
        citas = CitaMedica.objects.filter(fecha__year=anio, fecha__month=mes)
        citas_por_dia = {}
        for cita in citas:
            d = cita.fecha.day
            if d not in citas_por_dia:
                citas_por_dia[d] = []
            citas_por_dia[d].append(cita)
        ESTADO_COLOR = {
            'atendido': 'bg-green-500 text-white',
            'ocupado': 'bg-red-500 text-white',
            'disponible': 'bg-yellow-400 text-white',
        }
        meses = [
            (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'),
            (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
        ]
        anios = list(range(hoy.year-5, hoy.year+2))
        primer_semana, _ = calendar.monthrange(anio, mes)
        dias_del_mes = []
        for _ in range((primer_semana + 6) % 7):
            dias_del_mes.append({'numero': '', 'es_hoy': False, 'tiene_citas': False, 'citas': [], 'color': ''})
        for dia in range(1, dias_en_mes + 1):
            es_hoy = (anio == hoy.year and mes == hoy.month and dia == hoy.day)
            citas_dia = citas_por_dia.get(dia, [])
            tiene_citas = bool(citas_dia)
            estado_predominante = None
            if tiene_citas:
                estados = [c.estado for c in citas_dia]
                estado_predominante = max(set(estados), key=estados.count)
            color = ESTADO_COLOR.get(estado_predominante, 'bg-white text-gray-700') if tiene_citas else 'bg-white text-gray-700'
            citas_info = [
                {
                    'id': c.id,
                    'paciente': str(c.paciente),
                    'hora': c.hora_cita.strftime('%H:%M'),
                    'estado': c.estado,
                    'observaciones': c.observaciones or ''
                }
                for c in citas_dia
            ]
            dias_del_mes.append({
                'numero': dia,
                'es_hoy': es_hoy,
                'tiene_citas': tiene_citas,
                'citas': citas_info,
                'color': color,
            })
        while len(dias_del_mes) % 7 != 0 or len(dias_del_mes) < 35:
            dias_del_mes.append({'numero': '', 'es_hoy': False, 'tiene_citas': False, 'citas': [], 'color': ''})
        context.update({
            'mes_actual': meses[mes-1][1],
            'mes_actual_num': mes,
            'anio_actual': anio,
            'dias_mes': dias_del_mes,
            'meses': meses,
            'anios': anios,
        })
        return context

class CalendarioSemanalView(SidebarMenuMixin, TemplateView):
    template_name = 'doctor/citas/calendario_semanal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        import datetime
        from applications.doctor.models import HorarioAtencion, CitaMedica
        from applications.core.models import Doctor
        from django.utils import timezone
        hoy = timezone.localdate()
        fecha_str = self.request.GET.get('fecha')
        if fecha_str:
            try:
                hoy = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except Exception:
                pass
        lunes = hoy - datetime.timedelta(days=hoy.weekday())
        dias_semana = []
        dias_map = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        for i in range(7):
            dia = lunes + datetime.timedelta(days=i)
            dias_semana.append({
                'nombre': dias_map[i].capitalize(),
                'fecha': dia,
            })
        user = self.request.user
        doctor = None
        doctor_id = self.request.GET.get('doctor_id')
        if user.is_superuser or user.groups.filter(name='Administrador').exists():
            if doctor_id:
                doctor = Doctor.objects.filter(id=doctor_id).first()
            else:
                doctor = Doctor.objects.first()
        else:
            doctor = Doctor.objects.filter(user=user).first()
        if not doctor:
            context['error'] = 'No se encontró el doctor.'
            return context
        horarios_qs = HorarioAtencion.objects.filter(doctor=doctor, activo=True)
        min_hora = None
        max_hora = None
        duracion = getattr(doctor, 'duracion_atencion', 30)
        for h in horarios_qs:
            if min_hora is None or h.hora_inicio < min_hora:
                min_hora = h.hora_inicio
            if max_hora is None or h.hora_fin > max_hora:
                max_hora = h.hora_fin
        if not min_hora or not max_hora:
            context['error'] = 'No hay horarios configurados para el doctor.'
            return context
        horas_dia = []
        actual = datetime.datetime.combine(hoy, min_hora)
        fin = datetime.datetime.combine(hoy, max_hora)
        while actual < fin:
            horas_dia.append(actual.time().strftime('%H:%M'))
            actual += datetime.timedelta(minutes=duracion)
        # slots_semanales: lista de filas, cada fila es lista de 7 slots (uno por día)
        slots_semanales = []
        now = timezone.localtime()
        for hora_str in horas_dia:
            fila = []
            for i, dia in enumerate(dias_semana):
                fecha = dia['fecha']
                dia_semana = dias_map[i]
                horario = HorarioAtencion.objects.filter(doctor=doctor, activo=True, dia_semana=dia_semana).first()
                if not horario:
                    fila.append({'hora': hora_str, 'estado': 'no_disponible', 'cita': None, 'ya_pasado': True, 'fecha': fecha})
                    continue
                hora_dt = datetime.datetime.combine(fecha, datetime.datetime.strptime(hora_str, '%H:%M').time())
                if not (horario.hora_inicio <= hora_dt.time() < horario.hora_fin):
                    fila.append({'hora': hora_str, 'estado': 'no_disponible', 'cita': None, 'ya_pasado': True, 'fecha': fecha})
                    continue
                intervalo_desde = horario.intervalo_desde
                intervalo_hasta = horario.intervalo_hasta
                if intervalo_desde and intervalo_hasta:
                    if intervalo_desde <= hora_dt.time() < intervalo_hasta:
                        fila.append({'hora': hora_str, 'estado': 'no_disponible', 'cita': None, 'ya_pasado': True, 'fecha': fecha})
                        continue
                cita = CitaMedica.objects.select_related('paciente').filter(fecha=fecha, hora_cita=hora_dt.time()).first()
                if cita:
                    if cita.estado == EstadoCitaChoices.ATENDIDO:
                        estado = 'atendido'
                    else:
                        estado = 'ocupado'
                else:
                    estado = 'disponible'
                slot_datetime = hora_dt
                if timezone.is_naive(slot_datetime):
                    slot_datetime = timezone.make_aware(slot_datetime, timezone.get_current_timezone())
                ya_pasado = slot_datetime < now
                fila.append({
                    'hora': hora_str,
                    'estado': estado,
                    'cita': cita,
                    'ya_pasado': ya_pasado,
                    'fecha': fecha,
                })
            slots_semanales.append(fila)
        context.update({
            'doctor': doctor,
            'dias_semana': dias_semana,
            'semana_inicio': lunes,
            'semana_fin': lunes + datetime.timedelta(days=6),
            'horas_dia': horas_dia,
            'slots_semanales': slots_semanales,
        })
        return context

class CalendarioDiarioView(SidebarMenuMixin, TemplateView):
    template_name = 'doctor/citas/calendario_diario.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        import datetime
        from applications.doctor.models import HorarioAtencion, CitaMedica
        from django.utils import timezone
        from applications.core.models import Doctor
        fecha_actual = self.request.GET.get('fecha')
        if fecha_actual:
            try:
                fecha_actual = datetime.datetime.strptime(fecha_actual, '%Y-%m-%d').date()
            except Exception:
                fecha_actual = timezone.localdate()
        else:
            fecha_actual = timezone.localdate()
        dias_map = {
            'monday': 'lunes',
            'tuesday': 'martes',
            'wednesday': 'miércoles',
            'thursday': 'jueves',
            'friday': 'viernes',
            'saturday': 'sábado',
            'sunday': 'domingo',
        }
        dia_en = fecha_actual.strftime('%A').lower() if fecha_actual else ''
        dia_semana = dias_map.get(dia_en, dia_en)
        user = self.request.user
        doctor = None
        doctor_id = self.request.GET.get('doctor_id')
        if user.is_superuser or user.groups.filter(name='Administrador').exists():
            if doctor_id:
                doctor = Doctor.objects.filter(id=doctor_id).first()
            else:
                doctor = Doctor.objects.first()
        else:
            doctor = Doctor.objects.filter(user=user).first()
        if not doctor:
            context['error'] = 'No se encontró el doctor.'
            return context
        duracion = getattr(doctor, 'duracion_atencion', 30)
        horarios_qs = HorarioAtencion.objects.filter(doctor=doctor, dia_semana=dia_semana, activo=True)
        bloques = []
        total = 0
        disponibles = 0
        ocupadas = 0
        atendidas = 0
        now = timezone.localtime()
        if horarios_qs.exists():
            for horario in horarios_qs:
                hora_inicio = datetime.datetime.combine(fecha_actual, horario.hora_inicio)
                hora_fin = datetime.datetime.combine(fecha_actual, horario.hora_fin)
                intervalo_desde = datetime.datetime.combine(fecha_actual, horario.intervalo_desde) if horario.intervalo_desde else None
                intervalo_hasta = datetime.datetime.combine(fecha_actual, horario.intervalo_hasta) if horario.intervalo_hasta else None
                actual = hora_inicio
                while actual < hora_fin:
                    hora_bloque = actual.time()
                    # Excluir intervalo de descanso
                    if intervalo_desde and intervalo_hasta:
                        if isinstance(intervalo_desde, datetime.datetime):
                            intervalo_desde = intervalo_desde.time()
                        if isinstance(intervalo_hasta, datetime.datetime):
                            intervalo_hasta = intervalo_hasta.time()
                        if isinstance(hora_bloque, datetime.datetime):
                            hora_bloque = hora_bloque.time()
                        if (
                            isinstance(intervalo_desde, datetime.time)
                            and isinstance(intervalo_hasta, datetime.time)
                            and isinstance(hora_bloque, datetime.time)
                        ):
                            if intervalo_desde <= hora_bloque < intervalo_hasta:
                                actual += datetime.timedelta(minutes=duracion)
                                continue
                    cita = CitaMedica.objects.select_related('paciente').filter(fecha=fecha_actual, hora_cita=hora_bloque).first()
                    if cita:
                        if cita.estado == EstadoCitaChoices.ATENDIDO:
                            estado = 'atendido'
                            atendidas += 1
                        else:
                            estado = 'ocupado'
                            ocupadas += 1
                    else:
                        estado = 'disponible'
                        disponibles += 1
                    # Calcular si el slot ya pasó (ambos aware)
                    slot_datetime = datetime.datetime.combine(fecha_actual, hora_bloque)
                    if timezone.is_naive(slot_datetime):
                        slot_datetime = timezone.make_aware(slot_datetime, timezone.get_current_timezone())
                    ya_pasado = slot_datetime < now
                    bloques.append({
                        'hora': hora_bloque.strftime('%H:%M'),
                        'estado': estado,
                        'cita': cita,
                        'ya_pasado': ya_pasado,
                    })
                    total += 1
                    actual += datetime.timedelta(minutes=duracion)
        if total > 0:
            porcentaje_disponible = int(disponibles * 100 / total)
            porcentaje_ocupadas = int(ocupadas * 100 / total)
            porcentaje_atendidas = 100 - porcentaje_disponible - porcentaje_ocupadas
        else:
            porcentaje_disponible = porcentaje_ocupadas = porcentaje_atendidas = 0
        context.update({
            'doctor': doctor,
            'fecha_actual': fecha_actual,
            'bloques': bloques,
            'resumen': {
                'total_citas': total,
                'disponible': disponibles,
                'ocupadas': ocupadas,
                'consultas': atendidas,
            },
            'porcentaje_disponible': porcentaje_disponible,
            'porcentaje_ocupadas': porcentaje_ocupadas,
            'porcentaje_atendidas': porcentaje_atendidas,
        })
        # --- PREMIUM: Agregar permisos y menú premium al contexto (igual que los mixins) ---
        from applications.security.components.menu_module import MenuModule
        from applications.security.components.group_session import UserGroupSession
        from applications.security.components.group_permission import GroupPermission
        MenuModule(self.request).fill(context)
        userGroupSession = UserGroupSession(self.request)
        group = userGroupSession.get_group_session() if self.request.user.is_authenticated else None
        context['permissions'] = GroupPermission.get_permission_dict_of_group(self.request.user, group) if group else {}
        # -------------------------------------------------------------------------------
        return context

def calendario_diario(request):
    # Obtener el doctor único
    doctor = Doctor.objects.first()
    if not doctor:
        return render(request, 'doctor/citas/calendario_diario.html', {'error': 'No hay doctor registrado.'})

    # Determinar la fecha a mostrar (hoy por defecto)
    fecha_actual = request.GET.get('fecha')
    if fecha_actual:
        try:
            fecha_actual = datetime.strptime(fecha_actual, '%Y-%m-%d').date()
        except Exception:
            fecha_actual = timezone.localdate()
    else:
        fecha_actual = timezone.localdate()
    dias_map = {
        'monday': 'lunes',
        'tuesday': 'martes',
        'wednesday': 'miércoles',
        'thursday': 'jueves',
        'friday': 'viernes',
        'saturday': 'sábado',
        'sunday': 'domingo',
    }
    dia_en = fecha_actual.strftime('%A').lower() if fecha_actual else ''
    dia_semana = dias_map.get(dia_en, dia_en)

    # Buscar el horario de atención para ese día
    horario = HorarioAtencion.objects.filter(doctor=doctor, activo=True, dia_semana=dia_semana).first()
    bloques = []
    total = 0
    disponibles = 0
    ocupadas = 0
    atendidas = 0
    if horario:
        duracion = getattr(doctor, 'duracion_atencion', 30)
        hora_inicio = datetime.combine(fecha_actual, horario.hora_inicio)
        hora_fin = datetime.combine(fecha_actual, horario.hora_fin)
        intervalo_desde = horario.intervalo_desde
        intervalo_hasta = horario.intervalo_hasta
        actual = hora_inicio
        while actual < hora_fin:
            hora_bloque = actual.time()
            # Excluir intervalo de descanso
            if intervalo_desde and intervalo_hasta:
                # Convierte a time si es datetime
                if isinstance(intervalo_desde, datetime.datetime):
                    intervalo_desde = intervalo_desde.time()
                if isinstance(intervalo_hasta, datetime.datetime):
                    intervalo_hasta = intervalo_hasta.time()
                if isinstance(hora_bloque, datetime.datetime):
                    hora_bloque = hora_bloque.time()
                if (
                    isinstance(intervalo_desde, datetime.time)
                    and isinstance(intervalo_hasta, datetime.time)
                    and isinstance(hora_bloque, datetime.time)
                ):
                    if intervalo_desde <= hora_bloque < intervalo_hasta:
                        actual += timedelta(minutes=duracion)
                        continue
            # Buscar cita en ese horario, optimizando with select_related para paciente
            cita = CitaMedica.objects.select_related('paciente').filter(fecha=fecha_actual, hora_cita=hora_bloque).first()
            if cita:
                if cita.estado == EstadoCitaChoices.ATENDIDO:
                    estado = 'atendido'
                    atendidas += 1
                else:
                    estado = 'ocupado'
                    ocupadas += 1
            else:
                estado = 'disponible'
                disponibles += 1
            bloques.append({
                'hora': hora_bloque.strftime('%H:%M'),
                'estado': estado,
                'cita': cita
            })
            total += 1
            actual += timedelta(minutes=duracion)
    # Calcular porcentajes seguros
    if total > 0:
        porcentaje_disponible = int(disponibles * 100 / total)
        porcentaje_ocupadas = int(ocupadas * 100 / total)
        porcentaje_atendidas = 100 - porcentaje_disponible - porcentaje_ocupadas
    else:
        porcentaje_disponible = porcentaje_ocupadas = porcentaje_atendidas = 0
    context = {
        'doctor': doctor,
        'fecha_actual': fecha_actual,
        'bloques': bloques,
        'resumen': {
            'total_citas': total,
            'disponible': disponibles,
            'ocupadas': ocupadas,
            'consultas': atendidas,
        },
        'porcentaje_disponible': porcentaje_disponible,
        'porcentaje_ocupadas': porcentaje_ocupadas,
        'porcentaje_atendidas': porcentaje_atendidas,
    }
    # --- PREMIUM: Agregar permisos y menú premium al contexto (igual que los mixins) ---
    from applications.security.components.menu_module import MenuModule
    from applications.security.components.group_session import UserGroupSession
    from applications.security.components.group_permission import GroupPermission
    MenuModule(request).fill(context)
    userGroupSession = UserGroupSession(request)
    group = userGroupSession.get_group_session() if request.user.is_authenticated else None
    context['permissions'] = GroupPermission.get_permission_dict_of_group(request.user, group) if group else {}
    # -------------------------------------------------------------------------------
    return render(request, 'doctor/citas/calendario_diario.html', context)

@require_GET
def horarios_disponibles_ajax(request):
    try:
        fecha_str = request.GET.get('fecha')
        doctor_id = request.GET.get('doctor_id')
        print('AJAX horarios_disponibles_ajax params:', fecha_str, doctor_id)
        if not fecha_str or not doctor_id:
            return JsonResponse({'horarios': [], 'debug': 'Faltan parámetros fecha o doctor_id.'})
        try:
            fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except Exception:
            return JsonResponse({'horarios': [], 'debug': 'Fecha inválida.'})
        try:
            doctor = Doctor.objects.get(id=doctor_id, activo=True)
        except Doctor.DoesNotExist:
            return JsonResponse({'horarios': [], 'debug': 'No se encontró el doctor.'})
        if fecha < timezone.localdate():
            return JsonResponse({'horarios': [], 'debug': 'No se permiten fechas pasadas.'})
        dias_map = {
            'Monday': 'lunes',
            'Tuesday': 'martes',
            'Wednesday': 'miércoles',
            'Thursday': 'jueves',
            'Friday': 'viernes',
            'Saturday': 'sábado',
            'Sunday': 'domingo'
        }
        dia_semana = dias_map.get(fecha.strftime('%A'), '')
        print('AJAX horarios_disponibles_ajax dia_semana:', dia_semana)
        horarios_atencion = HorarioAtencion.objects.filter(
            doctor=doctor,
            dia_semana=dia_semana,
            activo=True
        )
        print('AJAX horarios_disponibles_ajax horarios_atencion:', list(horarios_atencion))
        if not horarios_atencion.exists():
            return JsonResponse({'horarios': [], 'debug': 'El doctor no tiene horario de atención para ese día.'})
        # CORREGIDO: solo filtrar por fecha, ya que CitaMedica no tiene campo doctor
        citas_ocupadas = set(CitaMedica.objects.filter(
            fecha=fecha
        ).values_list('hora_cita', flat=True))
        print('AJAX horarios_disponibles_ajax citas_ocupadas:', citas_ocupadas)
        duracion = getattr(doctor, 'duracion_atencion', 30)
        horas_disponibles = []
        for horario in horarios_atencion:
            hora_actual = horario.hora_inicio
            while hora_actual < horario.hora_fin:
                intervalo_desde = horario.intervalo_desde
                intervalo_hasta = horario.intervalo_hasta
                if intervalo_desde and intervalo_hasta:
                    if isinstance(intervalo_desde, datetime.datetime):
                        intervalo_desde = intervalo_desde.time()
                    if isinstance(intervalo_hasta, datetime.datetime):
                        intervalo_hasta = intervalo_hasta.time()
                    if isinstance(hora_actual, datetime.datetime):
                        hora_actual = hora_actual.time()
                    if (isinstance(intervalo_desde, datetime.time) and isinstance(intervalo_hasta, datetime.time) and isinstance(hora_actual, datetime.time)):
                        if intervalo_desde <= hora_actual < intervalo_hasta:
                            hora_actual = intervalo_hasta
                            continue
                if hora_actual not in citas_ocupadas:
                    if fecha == timezone.localdate() and hora_actual <= timezone.localtime().time():
                        pass
                    else:
                        horas_disponibles.append(hora_actual)
                hora_actual_dt = datetime.datetime.combine(datetime.date.today(), hora_actual)
                hora_actual = (hora_actual_dt + datetime.timedelta(minutes=duracion)).time()
        print('AJAX horarios_disponibles_ajax horas_disponibles:', horas_disponibles)
        horarios = [{'value': h.strftime('%H:%M'), 'label': h.strftime('%H:%M')} 
                    for h in horas_disponibles]
        if not horarios:
            return JsonResponse({'horarios': [], 'debug': 'No hay horarios disponibles para la fecha y doctor seleccionados.'})
        return JsonResponse({'horarios': horarios, 'debug': 'OK'})
    except Exception as e:
        import traceback
        print('ERROR en horarios_disponibles_ajax:', traceback.format_exc())
        return JsonResponse({'horarios': [], 'debug': f'Error inesperado: {str(e)}'})

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.http import HttpResponse, Http404

@login_required
def detalle_cita_ajax(request, cita_id):
    try:
        cita = CitaMedica.objects.select_related('paciente').get(pk=cita_id)
    except CitaMedica.DoesNotExist:
        raise Http404('Cita no encontrada')
    # Permisos: solo puede editar/eliminar si tiene permisos y la cita no está atendida
    puede_editar = request.user.has_perm('doctor.change_citamedica') and cita.estado != 'atendido'
    puede_eliminar = request.user.has_perm('doctor.delete_citamedica') and cita.estado != 'atendido'
    context = {
        'cita': cita,
        'puede_editar': puede_editar,
        'puede_eliminar': puede_eliminar,
        'perms': request.user.get_all_permissions(),
    }
    html = render_to_string('doctor/citas/fragmento_detalle_cita.html', context, request=request)
    return HttpResponse(html)

@login_required
@permission_required('doctor.add_citamedica', raise_exception=True)
@require_http_methods(["GET", "POST"])
def calendario_crear_cita(request):
    if request.method == "GET":
        # Permitir tanto AJAX como ?ajax=1
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax') == '1'
        hora = request.GET.get('hora')
        fecha = request.GET.get('fecha')
        if not hora or not fecha:
            return HttpResponseBadRequest("Faltan parámetros de hora o fecha")
        # Prellenar el form con hora y fecha
        initial = {'hora_cita': hora, 'fecha': fecha}
        form = CitaMedicaForm(initial=initial)
        context = {'form': form, 'request': request, 'doctor': getattr(request.user, 'doctor', None), 'doctor_id': getattr(getattr(request.user, 'doctor', None), 'id', None)}
        if is_ajax:
            html = render_to_string('doctor/citas/form_modal_calendario.html', context, request=request)
            return HttpResponse(html)
        else:
            return render(request, 'doctor/citas/form.html', context)
    elif request.method == "POST":
        form = CitaMedicaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            # Asignar el doctor logueado
            if hasattr(request.user, 'doctor'):
                cita.doctor = request.user.doctor
            else:
                # Fallback: buscar el doctor por grupo
                from applications.core.models import Doctor
                doctor = Doctor.objects.filter(user=request.user).first()
                if doctor:
                    cita.doctor = doctor
            cita.save()
            return JsonResponse({'success': True})
        else:
            context = {'form': form, 'request': request, 'doctor': getattr(request.user, 'doctor', None), 'doctor_id': getattr(getattr(request.user, 'doctor', None), 'id', None)}
            html = render_to_string('doctor/citas/form_modal_calendario.html', context, request=request)
            return JsonResponse({'success': False, 'html': html})

from django import forms
from applications.doctor.utils.cita_medica import EstadoCitaChoices
from django.utils import timezone

class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = ['paciente', 'fecha', 'hora_cita', 'observaciones']  # Excluir 'estado' intencionalmente

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar widgets si es necesario
        self.fields['fecha'].widget.attrs.update({'class': 'datepicker'})
        self.fields['hora_cita'].widget.attrs.update({'class': 'timepicker'})

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha < timezone.localdate():
            raise forms.ValidationError("La fecha no puede ser en el pasado.")
        return fecha

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Lógica automática de estado:
        # Si la cita es nueva, siempre inicia como 'ocupado'
        if not instance.pk:
            instance.estado = EstadoCitaChoices.OCUPADO
        else:
            # Si la cita ya existe, actualizar estado según la hora
            ahora = timezone.localtime()
            cita_datetime = timezone.make_aware(datetime.datetime.combine(instance.fecha, instance.hora_cita))
            if instance.estado == EstadoCitaChoices.OCUPADO and cita_datetime < ahora:
                instance.estado = EstadoCitaChoices.ATENDIDO
        if commit:
            instance.save()
        return instance


