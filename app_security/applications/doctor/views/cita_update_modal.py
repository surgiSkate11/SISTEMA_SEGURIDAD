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

class CitaMedicaUpdateModalView(PermissionMixin, View):
    permission_required = 'doctor.change_citamedica'
    def get(self, request, pk):
        doctor = get_unique_doctor()
        cita = get_object_or_404(CitaMedica, pk=pk)
        form = CitaMedicaForm(instance=cita)
        context = {
            'form': form,
            'doctor': doctor,
            'doctor_id': doctor.id if doctor else None,
            'fecha': cita.fecha,
            'hora': cita.hora_cita,
        }
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

    def post(self, request, pk):
        doctor = get_unique_doctor()
        cita = get_object_or_404(CitaMedica, pk=pk)
        form = CitaMedicaForm(request.POST, instance=cita)
        if form.is_valid():
            cita = form.save()
            if request.GET.get('ajax') == '1' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': reverse('doctor:calendario_diario')})
            return redirect('doctor:calendario_diario')
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
            return render(request, 'doctor/citas/form_modal_calendario.html', context)
        return render(request, 'doctor/citas/form.html', context)
