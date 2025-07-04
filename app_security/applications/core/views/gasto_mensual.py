from django.urls import reverse_lazy
from applications.core.models import GastoMensual
from applications.core.forms.gasto_mensual import GastoMensualForm
from django.db.models import Q
from applications.doctor.utils.auditorias import registrar_auditoria
from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from applications.security.components.sidebar_menu_mixin import SidebarMenuMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.db import models
from django.contrib import messages
from django.utils import timezone

class GastoMensualListView(SidebarMenuMixin, PermissionMixin, ListViewMixin, ListView):
    model = GastoMensual
    template_name = 'core/gasto_mensual/list.html'
    context_object_name = 'gastos'
    paginate_by = 5
    permission_required = 'view_gastomensual'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(user=user)
        # Filtros año y mes
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        if year and year.isdigit():
            queryset = queryset.filter(fecha__year=int(year))
        if month and month.isdigit():
            queryset = queryset.filter(fecha__month=int(month))
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(tipo_gasto__nombre__icontains=search) |
                Q(valor__icontains=search) |
                Q(observacion__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gastos = context['gastos']
        # Años disponibles dinámicamente
        years = GastoMensual.objects.dates('fecha', 'year', order='DESC')
        context['available_years'] = [d.year for d in years]
        # Mes seleccionado y año seleccionado
        selected_year = self.request.GET.get('year')
        selected_month = self.request.GET.get('month')
        # Si no hay selección, usar el año/mes actual
        hoy = timezone.now().date()
        if not selected_year:
            selected_year = str(hoy.year)
        if not selected_month:
            selected_month = str(hoy.month)
        context['selected_year'] = int(selected_year)
        context['selected_month'] = int(selected_month)
        # Total del mes filtrado
        total_mes = GastoMensual.objects.filter(
            fecha__year=selected_year,
            fecha__month=selected_month
        )
        user = self.request.user
        if not user.is_superuser:
            total_mes = total_mes.filter(user=user)
        context['total_gastos'] = total_mes.aggregate(total=models.Sum('valor'))['total'] or 0
        # ...otros cálculos premium filtrados...
        # Mayor gasto del mes filtrado
        mayor_gasto = total_mes.order_by('-valor').first()
        context['mayor_gasto'] = mayor_gasto
        # Promedio diario del mes filtrado
        from calendar import monthrange
        dias_mes = monthrange(int(selected_year), int(selected_month))[1]
        context['promedio_diario'] = (context['total_gastos'] / dias_mes) if dias_mes else 0
        # Categorías activas del mes filtrado
        context['categorias_activas'] = total_mes.values('tipo_gasto').distinct().count()
        context['meses'] = [
            (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
            (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
            (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
        ]
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('ajax') == '1':
            tabla_html = render_to_string('core/gasto_mensual/_tabla_gastos.html', context, request=self.request)
            return HttpResponse(tabla_html)
        return super().render_to_response(context, **response_kwargs)

class GastoMensualCreateView(SidebarMenuMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = GastoMensual
    form_class = GastoMensualForm
    template_name = 'core/gasto_mensual/form.html'
    success_url = reverse_lazy('core:gasto_mensual_list')
    permission_required = 'add_gastomensual'

    def form_valid(self, form):
        # Asignar el usuario autenticado al gasto antes de guardar
        form.instance.user = self.request.user
        response = super().form_valid(form)
        registrar_auditoria(self.request, 'GastoMensual', self.object.id, 'CREAR')
        messages.success(self.request, 'Gasto mensual creado exitosamente.')
        return response

class GastoMensualUpdateView(SidebarMenuMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = GastoMensual
    form_class = GastoMensualForm
    template_name = 'core/gasto_mensual/form.html'
    success_url = reverse_lazy('core:gasto_mensual_list')
    permission_required = 'change_gastomensual'

    def form_valid(self, form):
        # Asegurar que el usuario no cambie en la edición
        form.instance.user = self.request.user
        response = super().form_valid(form)
        registrar_auditoria(self.request, 'GastoMensual', self.object.id, 'EDITAR')
        messages.success(self.request, 'Gasto mensual actualizado correctamente.')
        return response

class GastoMensualDeleteView(SidebarMenuMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = GastoMensual
    template_name = 'core/gasto_mensual/delete.html'
    success_url = reverse_lazy('core:gasto_mensual_list')
    permission_required = 'delete_gastomensual'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Gasto Mensual'
        context['description'] = f"¿Desea eliminar el gasto: {self.object}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        object_id = self.object.id
        response = super().delete(request, *args, **kwargs)
        registrar_auditoria(request, 'GastoMensual', object_id, 'ELIMINAR')
        messages.success(request, 'Gasto mensual eliminado correctamente.')
        return response
