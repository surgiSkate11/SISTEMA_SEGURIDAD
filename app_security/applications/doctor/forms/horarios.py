from django import forms
from applications.doctor.models import HorarioAtencion

class HorarioAtencionForm(forms.ModelForm):
    class Meta:
        model = HorarioAtencion
        fields = ['dia_semana', 'hora_inicio', 'hora_fin', 'intervalo_desde', 'intervalo_hasta', 'activo']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'intervalo_desde': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'intervalo_hasta': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        dia_semana = cleaned_data.get('dia_semana')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        doctor = getattr(self.instance, 'doctor', None) or self.initial.get('doctor')
        if not doctor and 'doctor' in self.data:
            doctor = self.data['doctor']
        # Validación: solo un horario por día para el mismo doctor
        if dia_semana and doctor:
            qs = HorarioAtencion.objects.filter(doctor=doctor, dia_semana=dia_semana)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('dia_semana', 'Ya existe un horario para este día. Solo se permite un horario por día.')
        # Validación: hora inicio < hora fin
        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            self.add_error('hora_fin', 'La hora de fin debe ser mayor que la hora de inicio.')
        return cleaned_data
