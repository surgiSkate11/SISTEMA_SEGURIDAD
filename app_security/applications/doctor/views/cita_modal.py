from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views import View
from applications.security.components.mixin_crud import PermissionMixin
from applications.doctor.models import CitaMedica
from applications.doctor.forms.citas import CitaMedicaForm
from applications.core.models import Paciente
from applications.core.models import Doctor

def get_unique_doctor():
    """Obtiene el único doctor global del sistema (asume solo uno activo)."""
    return Doctor.objects.filter(activo=True).first()

class CitaMedicaCreateModalView(PermissionMixin, View):
    permission_required = 'doctor.add_citamedica'
    def get(self, request):
        doctor = get_unique_doctor()
        fecha = request.GET.get('fecha')
        hora = request.GET.get('hora')
        initial = {}
        if fecha:
            initial['fecha'] = fecha
        if hora:
            initial['hora_cita'] = hora
        form = CitaMedicaForm(initial=initial)  # <--- sin doctor
        context = {
            'form': form,
            'doctor': doctor,
            'doctor_id': doctor.id if doctor else None,
            'fecha': fecha,  # <-- Asegura que esté en el contexto
            'hora': hora,    # <-- Asegura que esté en el contexto
        }
        # Llenar permisos y menú como en los mixins
        from applications.security.components.menu_module import MenuModule
        from applications.security.components.group_session import UserGroupSession
        MenuModule(request).fill(context)
        userGroupSession = UserGroupSession(request)
        group = userGroupSession.get_group_session()
        from applications.security.components.group_permission import GroupPermission
        context['permissions'] = GroupPermission.get_permission_dict_of_group(request.user, group)
        if request.GET.get('ajax') == '1' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'doctor/citas/form_modal_calendario.html', context)
        return render(request, 'doctor/citas/form.html', context)

    def post(self, request):
        doctor = get_unique_doctor()
        form = CitaMedicaForm(request.POST)  # <--- sin doctor
        if form.is_valid():
            cita = form.save()
            if request.GET.get('ajax') == '1' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': reverse('doctor:cita_list')})
            return redirect('doctor:cita_list')
        # Si el form no es válido, mantener los valores de fecha y hora en el contexto
        fecha = request.POST.get('fecha') or request.GET.get('fecha')
        hora = request.POST.get('hora_cita') or request.GET.get('hora')
        context = {
            'form': form,
            'doctor': doctor,
            'doctor_id': doctor.id if doctor else None,
            'fecha': fecha,
            'hora': hora,
        }
        from applications.security.components.menu_module import MenuModule
        from applications.security.components.group_session import UserGroupSession
        MenuModule(request).fill(context)
        userGroupSession = UserGroupSession(request)
        group = userGroupSession.get_group_session()
        from applications.security.components.group_permission import GroupPermission
        context['permissions'] = GroupPermission.get_permission_dict_of_group(request.user, group)
        if request.GET.get('ajax') == '1' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render(request, 'doctor/citas/form_modal_calendario.html', context)
            return JsonResponse({'success': False, 'html': html.content.decode()})
        return render(request, 'doctor/citas/form.html', context)
