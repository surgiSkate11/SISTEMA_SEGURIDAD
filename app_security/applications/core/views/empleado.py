from django.urls import reverse_lazy
from applications.core.models import Empleado
from applications.core.forms.empleado import EmpleadoForm
from django.db.models import Q
from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.security.components.sidebar_menu_mixin import SidebarMenuMixin
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages

class EmpleadoListView(SidebarMenuMixin, PermissionMixin, ListViewMixin, ListView):
    model = Empleado
    template_name = 'core/empleado/list.html'
    context_object_name = 'empleados'
    paginate_by = 5
    permission_required = 'view_empleado'

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
            html = render_to_string('core/empleado/_tabla_empleados.html', context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)

class EmpleadoCreateView(SidebarMenuMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'core/empleado/form.html'
    success_url = reverse_lazy('core:empleado_list')
    permission_required = 'add_empleado'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Empleado '{self.object.nombre}' creado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el empleado. Por favor revisa el formulario.")
        return super().form_invalid(form)

class EmpleadoUpdateView(SidebarMenuMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'core/empleado/form.html'
    success_url = reverse_lazy('core:empleado_list')
    permission_required = 'change_empleado'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Empleado '{self.object.nombre}' actualizado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el empleado. Por favor revisa el formulario.")
        return super().form_invalid(form)

class EmpleadoDeleteView(SidebarMenuMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = Empleado
    template_name = 'core/empleado/confirm_delete.html'
    success_url = reverse_lazy('core:empleado_list')
    permission_required = 'delete_empleado'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        object_id = self.object.id
        nombre = self.object.nombre
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, f"Empleado '{nombre}' eliminado exitosamente.")
            return response
        except Exception as e:
            messages.error(request, f"Error al eliminar el empleado: {e}")
            return self.render_to_response(self.get_context_data(object=self.object))
