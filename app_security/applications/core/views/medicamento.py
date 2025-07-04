from django.urls import reverse_lazy
from applications.core.models import Medicamento
from applications.core.forms.medicamento import MedicamentoForm
from django.db.models import Q
from applications.doctor.utils.auditorias import registrar_auditoria
from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from applications.security.components.sidebar_menu_mixin import SidebarMenuMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponse
from django.contrib import messages  # <-- Agregado para mensajes premium

class MedicamentoListView(SidebarMenuMixin, PermissionMixin, ListViewMixin, ListView):
    model = Medicamento
    template_name = 'core/medicamento/list.html'
    context_object_name = 'medicamentos'
    paginate_by = 5  # Cambiado de 10 a 5
    permission_required = 'view_medicamento'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Permitir búsqueda en tiempo real con 'q' (AJAX y normal)
        search = self.request.GET.get('q') or self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(marca_medicamento__nombre__icontains=search) |
                Q(tipo__nombre__icontains=search)
            )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Solo renderiza las filas <tr>...</tr> para AJAX
            from django.template.loader import render_to_string
            html = render_to_string('core/medicamento/_tabla_medicamentos.html', context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)

class MedicamentoCreateView(SidebarMenuMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'core/medicamento/form.html'
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'add_medicamento'

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_auditoria(self.request, 'Medicamento', self.object.id, 'CREAR')
        messages.success(self.request, f"Medicamento '{self.object.nombre}' creado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el medicamento. Por favor revisa el formulario.")
        return super().form_invalid(form)

class MedicamentoUpdateView(SidebarMenuMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'core/medicamento/form.html'
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'change_medicamento'

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_auditoria(self.request, 'Medicamento', self.object.id, 'EDITAR')
        messages.success(self.request, f"Medicamento '{self.object.nombre}' actualizado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el medicamento. Por favor revisa el formulario.")
        return super().form_invalid(form)

class MedicamentoDeleteView(SidebarMenuMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = Medicamento
    template_name = 'core/medicamento/confirm_delete.html'
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'delete_medicamento'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        object_id = self.object.id
        nombre = self.object.nombre
        try:
            response = super().delete(request, *args, **kwargs)
            registrar_auditoria(request, 'Medicamento', object_id, 'ELIMINAR')
            messages.success(request, f"Medicamento '{nombre}' eliminado exitosamente.")
            return response
        except Exception as e:
            messages.error(request, f"Error al eliminar el medicamento: {e}")
            return self.render_to_response(self.get_context_data(object=self.object))
