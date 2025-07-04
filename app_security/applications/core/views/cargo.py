from django.urls import reverse_lazy
from applications.core.models import Cargo
from applications.core.forms.cargo import CargoForm
from django.db.models import Q
from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.security.components.sidebar_menu_mixin import SidebarMenuMixin

class CargoListView(SidebarMenuMixin, PermissionMixin, ListViewMixin, ListView):
    model = Cargo
    template_name = 'core/cargo/list.html'
    context_object_name = 'cargos'
    paginate_by = 10
    permission_required = 'view_cargo'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search)
            )
        return queryset

class CargoCreateView(SidebarMenuMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'core/cargo/form.html'
    success_url = reverse_lazy('core:cargo_list')
    permission_required = 'add_cargo'

class CargoUpdateView(SidebarMenuMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'core/cargo/form.html'
    success_url = reverse_lazy('core:cargo_list')
    permission_required = 'change_cargo'

class CargoDeleteView(SidebarMenuMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = Cargo
    template_name = 'core/cargo/confirm_delete.html'
    success_url = reverse_lazy('core:cargo_list')
    permission_required = 'delete_cargo'
