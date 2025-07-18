from django import forms
from django.utils import timezone
from applications.doctor.models import CitaMedica
from applications.core.models import Paciente
from applications.doctor.utils.horarios import obtener_horarios_disponibles_para_fecha
from django.forms import ChoiceField
import datetime

class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        # Excluir el campo doctor, ya que es global
        exclude = []  # No hay campo doctor en el modelo
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-input', 'autocomplete': 'off', 'id': 'id_fecha'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.active_patient.all()
        self.fields['hora_cita'].widget = forms.HiddenInput()
        # Ocultar el campo estado y ponerle un valor por defecto si es creación
        if 'estado' in self.fields:
            self.fields['estado'].widget = forms.HiddenInput()
            if not self.instance.pk:
                self.fields['estado'].required = False
                self.initial['estado'] = 'ocupado'

        fecha = self.data.get('fecha') or self.initial.get('fecha')
        hora_enviado = self.data.get('hora_cita')

        if fecha:
            try:
                if isinstance(fecha, str):
                    fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
            except Exception:
                fecha = None

            if fecha:
                citas_ocupadas = CitaMedica.objects.filter(fecha=fecha).values_list('hora_cita', flat=True)
                # El intervalo lo puedes dejar fijo o configurable si quieres
                intervalo = 30
                horas = obtener_horarios_disponibles_para_fecha(None, fecha, list(citas_ocupadas), intervalo)
                choices = [(h.strftime('%H:%M'), h.strftime('%H:%M')) for h in horas]

                if hora_enviado and hora_enviado not in dict(choices):
                    choices.append((hora_enviado, hora_enviado))

                self.fields['hora_cita'].choices = choices
            else:
                self.fields['hora_cita'].choices = []
        else:
            self.fields['hora_cita'].choices = []

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < timezone.now().date():
            raise forms.ValidationError("La fecha de la cita no puede ser en el pasado.")
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        # Si el campo estado está oculto y no viene en POST, ponerle un valor por defecto
        if 'estado' in self.fields and not cleaned_data.get('estado'):
            if not self.instance.pk:
                cleaned_data['estado'] = 'ocupado'
            else:
                cleaned_data['estado'] = self.instance.estado

        paciente = cleaned_data.get('paciente')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora_cita')
        # Validar paciente activo
        if paciente and not paciente.activo:
            self.add_error('paciente', 'El paciente no está activo.')
        if not paciente:
            self.add_error('paciente', 'Debe seleccionar un paciente.')
        if not fecha:
            self.add_error('fecha', 'Debe ingresar una fecha.')
        if not hora:
            self.add_error('hora_cita', 'Debe ingresar una hora.')
        # Validar duplicidad de cita para el mismo paciente, fecha y hora
        if paciente and fecha and hora:
            existe = CitaMedica.objects.filter(paciente=paciente, fecha=fecha, hora_cita=hora)
            if self.instance.pk:
                existe = existe.exclude(pk=self.instance.pk)
            if existe.exists():
                raise forms.ValidationError('Ya existe una cita para este paciente en la misma fecha y hora.')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Asignar automáticamente el doctor si es doctor autenticado
        if hasattr(self, 'user') and self.user and hasattr(self.user, 'doctor'):
            instance.doctor = self.user.doctor
        # Lógica automática de estado:
        # Si la cita es nueva, siempre inicia como 'ocupado'
        if not instance.pk:
            instance.estado = 'ocupado'
        else:
            # Si la cita ya existe, actualizar estado según la hora
            ahora = timezone.localtime()
            cita_datetime = timezone.make_aware(datetime.datetime.combine(instance.fecha, instance.hora_cita))
            if instance.estado == 'ocupado' and cita_datetime < ahora:
                instance.estado = 'atendido'
        if commit:
            instance.save()
        return instance
