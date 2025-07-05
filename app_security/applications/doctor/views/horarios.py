from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from applications.doctor.models import HorarioAtencion
from applications.doctor.forms.horarios import HorarioAtencionForm
from applications.security.components.sidebar_menu_mixin import SidebarMenuMixin
from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin

class HorarioAtencionListView(SidebarMenuMixin, PermissionMixin, ListViewMixin, ListView):
    model = HorarioAtencion
    template_name = 'doctor/horarios/list.html'
    context_object_name = 'horarios'
    permission_required = 'view_horarioatencion'
    paginate_by = 20

    def get_queryset(self):
        # Ordenar por el orden de los días de la semana
        dias_orden = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        qs = super().get_queryset()
        # Si el modelo tiene campo doctor, filtrar por el doctor logueado si aplica
        user = self.request.user
        if hasattr(user, 'doctor'):
            qs = qs.filter(doctor=user.doctor)
        # Ordenar por el índice del día de la semana
        qs = list(qs)
        qs.sort(key=lambda h: dias_orden.index(h.dia_semana) if h.dia_semana in dias_orden else 99)
        return qs

class HorarioAtencionCreateView(SidebarMenuMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = HorarioAtencion
    form_class = HorarioAtencionForm
    template_name = 'doctor/horarios/form.html'
    success_url = reverse_lazy('doctor:horario_list')
    permission_required = 'add_horarioatencion'

    def form_valid(self, form):
        messages.success(self.request, "Horario de atención creado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el horario. Por favor revisa el formulario.")
        return super().form_invalid(form)

class HorarioAtencionUpdateView(SidebarMenuMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = HorarioAtencion
    form_class = HorarioAtencionForm
    template_name = 'doctor/horarios/form.html'
    success_url = reverse_lazy('doctor:horario_list')
    permission_required = 'change_horarioatencion'

    def form_valid(self, form):
        messages.success(self.request, "Horario de atención actualizado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el horario. Por favor revisa el formulario.")
        return super().form_invalid(form)

class HorarioAtencionDeleteView(SidebarMenuMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = HorarioAtencion
    template_name = 'fragments/delete.html'
    success_url = reverse_lazy('doctor:horario_list')
    permission_required = 'delete_horarioatencion'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Horario de atención eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)
