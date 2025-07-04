from django.urls import reverse_lazy
from applications.core.models import Diagnostico
from applications.core.forms.diagnostico import DiagnosticoForm
from django.db.models import Q
from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.security.components.sidebar_menu_mixin import SidebarMenuMixin
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages

class DiagnosticoListView(SidebarMenuMixin, PermissionMixin, ListViewMixin, ListView):
    model = Diagnostico
    template_name = 'core/diagnostico/list.html'
    context_object_name = 'diagnosticos'
    paginate_by = 5
    permission_required = 'view_diagnostico'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q') or self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(codigo__icontains=search)
            )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('core/diagnostico/_tabla_diagnosticos.html', context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)

class DiagnosticoCreateView(SidebarMenuMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = Diagnostico
    form_class = DiagnosticoForm
    template_name = 'core/diagnostico/form.html'
    success_url = reverse_lazy('core:diagnostico_list')
    permission_required = 'add_diagnostico'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Diagnóstico '{self.object.nombre}' creado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el diagnóstico. Por favor revisa el formulario.")
        return super().form_invalid(form)

class DiagnosticoUpdateView(SidebarMenuMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = Diagnostico
    form_class = DiagnosticoForm
    template_name = 'core/diagnostico/form.html'
    success_url = reverse_lazy('core:diagnostico_list')
    permission_required = 'change_diagnostico'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Diagnóstico '{self.object.nombre}' actualizado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el diagnóstico. Por favor revisa el formulario.")
        return super().form_invalid(form)

class DiagnosticoDeleteView(SidebarMenuMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = Diagnostico
    template_name = 'core/diagnostico/confirm_delete.html'
    success_url = reverse_lazy('core:diagnostico_list')
    permission_required = 'delete_diagnostico'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        object_id = self.object.id
        nombre = self.object.nombre
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, f"Diagnóstico '{nombre}' eliminado exitosamente.")
            return response
        except Exception as e:
            messages.error(request, f"Error al eliminar el diagnóstico: {e}")
            return self.render_to_response(self.get_context_data(object=self.object))
