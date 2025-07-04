from django.urls import reverse_lazy
from applications.core.models import Especialidad
from applications.core.forms.especialidad import EspecialidadForm
from django.db.models import Q
from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.security.components.sidebar_menu_mixin import SidebarMenuMixin
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages

class EspecialidadListView(SidebarMenuMixin, PermissionMixin, ListViewMixin, ListView):
    model = Especialidad
    template_name = 'core/especialidad/list.html'
    context_object_name = 'especialidades'
    paginate_by = 5
    permission_required = 'view_especialidad'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q') or self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search)
            )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('core/especialidad/_tabla_especialidades.html', context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)

class EspecialidadCreateView(SidebarMenuMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'core/especialidad/form.html'
    success_url = reverse_lazy('core:especialidad_list')
    permission_required = 'add_especialidad'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Especialidad '{self.object.nombre}' creada exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear la especialidad. Por favor revisa el formulario.")
        return super().form_invalid(form)

class EspecialidadUpdateView(SidebarMenuMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'core/especialidad/form.html'
    success_url = reverse_lazy('core:especialidad_list')
    permission_required = 'change_especialidad'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Especialidad '{self.object.nombre}' actualizada exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar la especialidad. Por favor revisa el formulario.")
        return super().form_invalid(form)

class EspecialidadDeleteView(SidebarMenuMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = Especialidad
    template_name = 'core/especialidad/confirm_delete.html'
    success_url = reverse_lazy('core:especialidad_list')
    permission_required = 'delete_especialidad'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        object_id = self.object.id
        nombre = self.object.nombre
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, f"Especialidad '{nombre}' eliminada exitosamente.")
            return response
        except Exception as e:
            messages.error(request, f"Error al eliminar la especialidad: {e}")
            return self.render_to_response(self.get_context_data(object=self.object))
