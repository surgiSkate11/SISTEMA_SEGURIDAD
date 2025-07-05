from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from applications.doctor.models import CitaMedica
from applications.doctor.forms.citas import CitaMedicaForm
from applications.core.models import Paciente

def cita_medica_create(request):
    doctor = getattr(request.user, 'doctor', None)
    if not doctor:
        return HttpResponse('No autorizado', status=403)
    if request.method == 'POST':
        form = CitaMedicaForm(request.POST, doctor=doctor)
        if form.is_valid():
            cita = form.save()
            if request.GET.get('ajax') == '1' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': reverse('doctor:cita_list')})
            return redirect('doctor:cita_list')
    else:
        form = CitaMedicaForm(doctor=doctor)
    context = {
        'form': form,
        'doctor': doctor,
        'doctor_id': doctor.id if doctor else None,
    }
    if request.GET.get('ajax') == '1' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'doctor/citas/form_modal_calendario.html', context)
    return render(request, 'doctor/citas/form.html', context)

def cita_medica_update(request, pk):
    doctor = getattr(request.user, 'doctor', None)
    cita = get_object_or_404(CitaMedica, pk=pk, doctor=doctor)
    if request.method == 'POST':
        form = CitaMedicaForm(request.POST, instance=cita, doctor=doctor)
        if form.is_valid():
            cita = form.save()
            if request.GET.get('ajax') == '1' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': reverse('doctor:cita_list')})
            return redirect('doctor:cita_list')
    else:
        form = CitaMedicaForm(instance=cita, doctor=doctor)
    context = {
        'form': form,
        'doctor': doctor,
        'doctor_id': doctor.id if doctor else None,
    }
    if request.GET.get('ajax') == '1' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'doctor/citas/form_modal_calendario.html', context)
    return render(request, 'doctor/citas/form.html', context)
