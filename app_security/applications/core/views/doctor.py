from django.urls import reverse_lazy
from applications.core.models import Doctor
from applications.core.forms.doctor import DoctorForm
from django.db.models import Q
from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.security.components.sidebar_menu_mixin import SidebarMenuMixin

class DoctorListView(SidebarMenuMixin, PermissionMixin, ListViewMixin, ListView):
    model = Doctor
    template_name = 'core/doctor/list.html'
    context_object_name = 'doctores'
    paginate_by = 10
    permission_required = 'view_doctor'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombres__icontains=search) |
                Q(apellidos__icontains=search) |
                Q(ruc__icontains=search)
            )
        return queryset

class DoctorCreateView(SidebarMenuMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'core/doctor/form.html'
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'add_doctor'

class DoctorUpdateView(SidebarMenuMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'core/doctor/form.html'
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'change_doctor'

class DoctorDeleteView(SidebarMenuMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = Doctor
    template_name = 'core/doctor/confirm_delete.html'
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'delete_doctor'
