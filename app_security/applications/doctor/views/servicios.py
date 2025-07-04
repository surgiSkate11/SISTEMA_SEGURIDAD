from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from applications.doctor.models import CitaMedica, ServiciosAdicionales
from applications.doctor.forms.citas import CitaMedicaForm
from applications.doctor.forms.servicios import ServiciosAdicionalesForm
from applications.core.models import Doctor
from applications.security.components.sidebar_menu_mixin import SidebarMenuMixin
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.views import View

class CitaMedicaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CitaMedica
    template_name = 'doctor/citas/list.html'
    context_object_name = 'citas'
    paginate_by = 10
    permission_required = 'doctor.view_citamedica'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(paciente__nombre_completo__icontains=q)
        return qs.order_by('-fecha', '-hora_cita')

class CitaMedicaCreateView(CreateView):
    model = CitaMedica
    form_class = CitaMedicaForm
    template_name = 'doctor/citas/form.html'
    success_url = reverse_lazy('doctor:cita_list')

class CitaMedicaUpdateView(UpdateView):
    model = CitaMedica
    form_class = CitaMedicaForm
    template_name = 'doctor/citas/form.html'
    success_url = reverse_lazy('doctor:cita_list')

class ServiciosAdicionalesListView(SidebarMenuMixin, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ServiciosAdicionales
    template_name = 'doctor/servicios/list.html'
    context_object_name = 'servicios'
    paginate_by = 5
    permission_required = 'doctor.view_serviciosadicionales'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q') or self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(codigo__icontains=search)
            )
        return queryset.order_by('nombre_servicio')

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('doctor/servicios/_tabla_servicios.html', context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)

class ServiciosAdicionalesCreateView(SidebarMenuMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ServiciosAdicionales
    form_class = ServiciosAdicionalesForm
    template_name = 'doctor/servicios/form.html'
    success_url = reverse_lazy('doctor:servicio_list')
    permission_required = 'doctor.add_serviciosadicionales'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Servicio adicional creado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el servicio adicional. Por favor revisa el formulario.")
        return super().form_invalid(form)

class ServiciosAdicionalesUpdateView(SidebarMenuMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ServiciosAdicionales
    form_class = ServiciosAdicionalesForm
    template_name = 'doctor/servicios/form.html'
    success_url = reverse_lazy('doctor:servicio_list')
    permission_required = 'doctor.change_serviciosadicionales'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Servicio adicional actualizado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el servicio adicional. Por favor revisa el formulario.")
        return super().form_invalid(form)

class ServiciosAdicionalesDeleteView(SidebarMenuMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ServiciosAdicionales
    template_name = 'doctor/servicios/confirm_delete.html'
    success_url = reverse_lazy('doctor:servicio_list')
    permission_required = 'doctor.delete_serviciosadicionales'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, f"Servicio adicional eliminado exitosamente.")
            return response
        except Exception as e:
            messages.error(request, f"Error al eliminar el servicio adicional: {e}")
            return self.render_to_response(self.get_context_data(object=self.object))

class ServicioCreateAjaxView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'doctor.add_serviciosadicionales'

    def get(self, request, *args, **kwargs):
        form = ServiciosAdicionalesForm()
        html = render_to_string('doctor/servicios/form_servicios.html', {'form': form, 'view': self}, request=request)
        return JsonResponse({'html': html})

    def post(self, request, *args, **kwargs):
        form = ServiciosAdicionalesForm(request.POST)
        if form.is_valid():
            servicio = form.save()
            data = {
                'success': True,
                'id': servicio.id,
                'nombre': servicio.nombre_servicio,
                'costo': str(servicio.costo_servicio),
                'activo': servicio.activo,
            }
            return JsonResponse(data)
        else:
            html = render_to_string('doctor/servicios/form_servicios.html', {'form': form, 'view': self}, request=request)
            return JsonResponse({'success': False, 'html': html})
