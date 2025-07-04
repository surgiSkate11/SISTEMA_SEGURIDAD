from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from applications.doctor.models import Pago, DetallePago, ServiciosAdicionales
from applications.doctor.forms.pagos import PagoForm, DetallePagoForm
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from applications.doctor.utils.paypal_api import PayPalAPI
from django.views import View
from django.http import HttpResponse
import json
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from applications.core.models import Doctor
from applications.security.components.sidebar_menu_mixin import SidebarMenuMixin
from django.contrib import messages
from django.template.loader import render_to_string
from django.db.models import Q
from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from applications.doctor.utils.auditorias import registrar_auditoria
from django.db import transaction
from decimal import Decimal
from django.http import JsonResponse
import weasyprint
from django.urls import path
from django.utils import timezone

class PagoListView(SidebarMenuMixin, PermissionMixin, ListViewMixin, ListView):
    model = Pago
    template_name = 'doctor/pagos/list.html'
    context_object_name = 'pagos'
    paginate_by = 5
    permission_required = 'view_pago'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q') or self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(atencion__paciente__apellidos__icontains=search) |
                Q(atencion__paciente__nombres__icontains=search) |
                Q(monto_total__icontains=search)
            )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('doctor/pagos/_tabla_pagos.html', context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)

class PagoDetailView(SidebarMenuMixin, PermissionMixin, ListViewMixin, ListView):
    model = DetallePago
    template_name = 'doctor/pagos/detalle.html'
    context_object_name = 'detalles'
    permission_required = 'view_pago'

    def get_queryset(self):
        pago_id = self.kwargs.get('pk')
        return DetallePago.objects.filter(pago_id=pago_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pago'] = Pago.objects.get(pk=self.kwargs.get('pk'))
        return context

class PagoCreateView(SidebarMenuMixin, PermissionMixin, CreateViewMixin, CreateView):
    model = Pago
    form_class = PagoForm
    template_name = 'doctor/pagos/form.html'
    success_url = reverse_lazy('doctor:pago_list')
    permission_required = 'add_pago'

    def form_valid(self, form):
        data = self.request.POST.copy()
        detalles_data = self.request.POST.get('detalles_data')
        detalles = json.loads(detalles_data) if detalles_data else []
        try:
            with transaction.atomic():
                # Calcular monto_total sumando los subtotales de los detalles
                monto_total = Decimal('0.00')
                for detalle in detalles:
                    cantidad = Decimal(str(detalle.get('cantidad', 1)))
                    precio_unitario = Decimal(str(detalle.get('precio_unitario', 0)))
                    descuento = Decimal(str(detalle.get('descuento_porcentaje', 0)))
                    aplica_seguro = detalle.get('aplica_seguro', False)
                    valor_seguro = Decimal(str(detalle.get('valor_seguro', 0))) if aplica_seguro else Decimal('0.00')
                    subtotal = (cantidad * precio_unitario) * (Decimal('1.0') - (descuento/Decimal('100.0')))
                    subtotal -= valor_seguro if aplica_seguro else Decimal('0.00')
                    if subtotal < 0:
                        subtotal = Decimal('0.00')
                    monto_total += subtotal
                if monto_total <= 0:
                    messages.error(self.request, "Debes agregar al menos un servicio válido para el pago.")
                    return super().form_invalid(form)
                pago = form.save(commit=False)
                pago.monto_total = monto_total
                pago.created_by = self.request.user
                pago.updated_by = self.request.user
                # Registrar fecha de pago si el estado es 'pagado'
                if hasattr(pago, 'estado') and str(pago.estado).lower() == 'pagado':
                    pago.fecha_pago = timezone.now()
                pago.save()
                # Guardar detalles
                for detalle in detalles:
                    DetallePago.objects.create(
                        pago=pago,
                        servicio_adicional_id=detalle.get('servicio_adicional'),
                        cantidad=detalle.get('cantidad', 1),
                        precio_unitario=detalle.get('precio_unitario', 0),
                        descuento_porcentaje=detalle.get('descuento_porcentaje', 0),
                        aplica_seguro=detalle.get('aplica_seguro', False),
                        valor_seguro=detalle.get('valor_seguro', 0),
                        descripcion_seguro=detalle.get('descripcion_seguro', ''),
                        subtotal=(Decimal(str(detalle.get('cantidad', 1))) * Decimal(str(detalle.get('precio_unitario', 0))) * (Decimal('1.0') - Decimal(str(detalle.get('descuento_porcentaje', 0)))/Decimal('100.0'))) - (Decimal(str(detalle.get('valor_seguro', 0))) if detalle.get('aplica_seguro', False) else Decimal('0.00'))
                    )
                registrar_auditoria(self.request, 'Pago', pago.id, 'CREAR')
                messages.success(self.request, f"Pago #{pago.id} creado exitosamente.")
                return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Error al crear el pago: {e}")
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el pago. Por favor revisa el formulario.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicios_qs = ServiciosAdicionales.objects.filter(activo=True)
        servicios = [
            {
                'id': s['id'],
                'nombre_servicio': s['nombre_servicio'],
                'costo_servicio': float(s['costo_servicio']),
            }
            for s in servicios_qs.values('id', 'nombre_servicio', 'costo_servicio')
        ]
        context['servicios'] = json.dumps(servicios)
        return context

class PagoUpdateView(SidebarMenuMixin, PermissionMixin, UpdateViewMixin, UpdateView):
    model = Pago
    form_class = PagoForm
    template_name = 'doctor/pagos/form.html'
    success_url = reverse_lazy('doctor:pago_list')
    permission_required = 'change_pago'

    def form_valid(self, form):
        detalles_data = self.request.POST.get('detalles_data')
        detalles = json.loads(detalles_data) if detalles_data else []
        try:
            with transaction.atomic():
                monto_total = Decimal('0.00')
                for detalle in detalles:
                    cantidad = Decimal(str(detalle.get('cantidad', 1)))
                    precio_unitario = Decimal(str(detalle.get('precio_unitario', 0)))
                    descuento = Decimal(str(detalle.get('descuento_porcentaje', 0)))
                    aplica_seguro = detalle.get('aplica_seguro', False)
                    valor_seguro = Decimal(str(detalle.get('valor_seguro', 0))) if aplica_seguro else Decimal('0.00')
                    subtotal = (cantidad * precio_unitario) * (Decimal('1.0') - (descuento/Decimal('100.0')))
                    subtotal -= valor_seguro if aplica_seguro else Decimal('0.00')
                    if subtotal < 0:
                        subtotal = Decimal('0.00')
                    monto_total += subtotal
                if monto_total <= 0:
                    messages.error(self.request, "Debes agregar al menos un servicio válido para el pago.")
                    return super().form_invalid(form)
                pago = form.save(commit=False)
                pago.monto_total = monto_total
                pago.updated_by = self.request.user
                # Detectar cambio de estado a 'pagado' y registrar fecha_pago en tiempo real
                estado_nuevo = str(form.cleaned_data.get('estado', '')).lower() if 'estado' in form.cleaned_data else ''
                estado_anterior = str(Pago.objects.get(pk=pago.pk).estado).lower() if pago.pk and hasattr(pago, 'estado') else ''
                if estado_nuevo == 'pagado' and (not pago.fecha_pago or estado_anterior != 'pagado'):
                    pago.fecha_pago = timezone.now()
                elif estado_nuevo != 'pagado':
                    pago.fecha_pago = None
                pago.save()
                DetallePago.objects.filter(pago=pago).delete()
                for detalle in detalles:
                    DetallePago.objects.create(
                        pago=pago,
                        servicio_adicional_id=detalle.get('servicio_adicional'),
                        cantidad=detalle.get('cantidad', 1),
                        precio_unitario=detalle.get('precio_unitario', 0),
                        descuento_porcentaje=detalle.get('descuento_porcentaje', 0),
                        aplica_seguro=detalle.get('aplica_seguro', False),
                        valor_seguro=detalle.get('valor_seguro', 0),
                        descripcion_seguro=detalle.get('descripcion_seguro', ''),
                        subtotal=(Decimal(str(detalle.get('cantidad', 1))) * Decimal(str(detalle.get('precio_unitario', 0))) * (Decimal('1.0') - Decimal(str(detalle.get('descuento_porcentaje', 0)))/Decimal('100.0'))) - (Decimal(str(detalle.get('valor_seguro', 0))) if detalle.get('aplica_seguro', False) else Decimal('0.00'))
                    )
                registrar_auditoria(self.request, 'Pago', pago.id, 'EDITAR')
                messages.success(self.request, f"Pago #{pago.id} actualizado exitosamente.")
                return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Error al actualizar el pago: {e}")
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el pago. Por favor revisa el formulario.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicios_qs = ServiciosAdicionales.objects.filter(activo=True)
        servicios = [
            {
                'id': s['id'],
                'nombre_servicio': s['nombre_servicio'],
                'costo_servicio': float(s['costo_servicio']),
            }
            for s in servicios_qs.values('id', 'nombre_servicio', 'costo_servicio')
        ]
        context['servicios'] = json.dumps(servicios)
        # Pasar detalles actuales para edición
        if self.object:
            context['detalles'] = DetallePago.objects.filter(pago=self.object)
        return context

class PagoDeleteView(SidebarMenuMixin, PermissionMixin, DeleteViewMixin, DeleteView):
    model = Pago
    template_name = 'doctor/pagos/confirm_delete.html'
    success_url = reverse_lazy('doctor:pago_list')
    permission_required = 'delete_pago'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        object_id = self.object.id
        try:
            response = super().delete(request, *args, **kwargs)
            registrar_auditoria(request, 'Pago', object_id, 'ELIMINAR')
            messages.success(request, f"Pago eliminado exitosamente.")
            return response
        except Exception as e:
            messages.error(request, f"Error al eliminar el pago: {e}")
            return self.render_to_response(self.get_context_data(object=self.object))

# Vista para manejar el retorno de PayPal
class PagoPayPalReturnView(View):
    def get(self, request):
        order_id = request.GET.get('token')
        if not order_id:
            return HttpResponse('Error: No se recibió token de PayPal', status=400)
        paypal = PayPalAPI()
        capture = paypal.capture_order(order_id)
        # Recuperar datos del pago desde la sesión
        data = request.session.pop('pago_form_data', None)
        detalles = request.session.pop('pago_detalles', None)
        if not data or not detalles:
            return HttpResponse('Error: No se encontró información del pago en sesión', status=400)
        # Marcar como pagado si la captura fue exitosa
        data['estado'] = 'pagado'
        from applications.doctor.utils.transacciones_pago import crear_pago_con_detalles
        crear_pago_con_detalles(request, data, detalles)
        return redirect('doctor:pago_list')

# Vista para imprimir el PDF del pago
from django.shortcuts import get_object_or_404

def imprimir_pago_pdf(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    detalles = DetallePago.objects.filter(pago=pago)
    html_string = render_to_string('doctor/pagos/pago_pdf.html', {
        'pago': pago,
        'detalles': detalles,
        'fecha': pago.fecha_pago,
    })
    pdf_file = weasyprint.HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=pago_{pago.id}.pdf'
    return response

urlpatterns = [
    # ...otras rutas...
    path('pagos/<int:pk>/detalle/', PagoDetailView.as_view(), name='pago_detalle'),
    path('pagos/<int:pk>/imprimir/', imprimir_pago_pdf, name='imprimir_pago_pdf'),
]
