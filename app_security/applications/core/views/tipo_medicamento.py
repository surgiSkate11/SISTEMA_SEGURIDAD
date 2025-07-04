from django.urls import reverse_lazy
from applications.core.models import TipoMedicamento
from applications.core.forms.tipo_medicamento import TipoMedicamentoForm
from django.db.models import Q
from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.security.components.sidebar_menu_mixin import SidebarMenuMixin

class TipoMedicamentoListView(SidebarMenuMixin, PermissionMixin, ListViewMixin, ListView):
    model = TipoMedicamento
    template_name = 'core/tipo_medicamento/list.html'
    context_object_name = 'tipos'
    paginate_by = 10
    permission_required = 'view_tipomedicamento'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search)
            )
        return queryset

class TipoMedicamentoCreateView(SidebarMenuMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    template_name = 'core/tipo_medicamento/form.html'
    success_url = reverse_lazy('core:tipo_medicamento_list')
    permission_required = 'add_tipomedicamento'

class TipoMedicamentoUpdateView(SidebarMenuMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    template_name = 'core/tipo_medicamento/form.html'
    success_url = reverse_lazy('core:tipo_medicamento_list')
    permission_required = 'change_tipomedicamento'

class TipoMedicamentoDeleteView(SidebarMenuMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoMedicamento
    template_name = 'core/tipo_medicamento/confirm_delete.html'
    success_url = reverse_lazy('core:tipo_medicamento_list')
    permission_required = 'delete_tipomedicamento'
