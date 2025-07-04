from django.urls import reverse_lazy
from applications.core.models import TipoGasto
from applications.core.forms.tipo_gasto import TipoGastoForm
from django.db.models import Q
from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.security.components.sidebar_menu_mixin import SidebarMenuMixin

class TipoGastoListView(SidebarMenuMixin, PermissionMixin, ListViewMixin, ListView):
    model = TipoGasto
    template_name = 'core/tipo_gasto/list.html'
    context_object_name = 'tipos_gasto'
    paginate_by = 10
    permission_required = 'view_tipogasto'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search)
            )
        return queryset

class TipoGastoCreateView(SidebarMenuMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = TipoGasto
    form_class = TipoGastoForm
    template_name = 'core/tipo_gasto/form.html'
    success_url = reverse_lazy('core:tipogasto_list')
    permission_required = 'add_tipogasto'

class TipoGastoUpdateView(SidebarMenuMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoGasto
    form_class = TipoGastoForm
    template_name = 'core/tipo_gasto/form.html'
    success_url = reverse_lazy('core:tipogasto_list')
    permission_required = 'change_tipogasto'

class TipoGastoDeleteView(SidebarMenuMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoGasto
    template_name = 'core/tipo_gasto/confirm_delete.html'
    success_url = reverse_lazy('core:tipogasto_list')
    permission_required = 'delete_tipogasto'
