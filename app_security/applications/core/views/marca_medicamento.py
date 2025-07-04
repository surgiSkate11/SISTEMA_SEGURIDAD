from django.urls import reverse_lazy
from applications.core.models import MarcaMedicamento
from applications.core.forms.marca_medicamento import MarcaMedicamentoForm
from django.db.models import Q
from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.security.components.sidebar_menu_mixin import SidebarMenuMixin

class MarcaMedicamentoListView(SidebarMenuMixin, PermissionMixin, ListViewMixin, ListView):
    model = MarcaMedicamento
    template_name = 'core/marca_medicamento/list.html'
    context_object_name = 'marcas'
    paginate_by = 10
    permission_required = 'view_marcamedicamento'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search)
            )
        return queryset

class MarcaMedicamentoCreateView(SidebarMenuMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = MarcaMedicamento
    form_class = MarcaMedicamentoForm
    template_name = 'core/marca_medicamento/form.html'
    success_url = reverse_lazy('core:marca_medicamento_list')
    permission_required = 'add_marcamedicamento'

class MarcaMedicamentoUpdateView(SidebarMenuMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = MarcaMedicamento
    form_class = MarcaMedicamentoForm
    template_name = 'core/marca_medicamento/form.html'
    success_url = reverse_lazy('core:marca_medicamento_list')
    permission_required = 'change_marcamedicamento'

class MarcaMedicamentoDeleteView(SidebarMenuMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = MarcaMedicamento
    template_name = 'core/marca_medicamento/confirm_delete.html'
    success_url = reverse_lazy('core:marca_medicamento_list')
    permission_required = 'delete_marcamedicamento'
