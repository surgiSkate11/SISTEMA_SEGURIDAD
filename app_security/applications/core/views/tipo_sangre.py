from django.urls import reverse_lazy
from applications.core.models import TipoSangre
from applications.core.forms.tipo_sangre import TipoSangreForm
from django.db.models import Q
from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.security.components.sidebar_menu_mixin import SidebarMenuMixin

class TipoSangreListView(SidebarMenuMixin, PermissionMixin, ListViewMixin, ListView):
    model = TipoSangre
    template_name = 'core/tipo_sangre/list.html'
    context_object_name = 'tipos_sangre'
    paginate_by = 10
    permission_required = 'view_tiposangre'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(tipo__icontains=search) |
                Q(descripcion__icontains=search)
            )
        return queryset

class TipoSangreCreateView(SidebarMenuMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = TipoSangre
    form_class = TipoSangreForm
    template_name = 'core/tipo_sangre/form.html'
    success_url = reverse_lazy('core:tipo_sangre_list')
    permission_required = 'add_tiposangre'

class TipoSangreUpdateView(SidebarMenuMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoSangre
    form_class = TipoSangreForm
    template_name = 'core/tipo_sangre/form.html'
    success_url = reverse_lazy('core:tipo_sangre_list')
    permission_required = 'change_tiposangre'

class TipoSangreDeleteView(SidebarMenuMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoSangre
    template_name = 'core/tipo_sangre/confirm_delete.html'
    success_url = reverse_lazy('core:tipo_sangre_list')
    permission_required = 'delete_tiposangre'
