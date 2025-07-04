from django import forms
from applications.core.models import Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'apellidos': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'cedula_ecuatoriana': forms.TextInput(attrs={'class': 'form-input', 'required': True, 'pattern': r'^[0-9]{10}$', 'title': 'Debe tener 10 dígitos'}),
            'dni': forms.TextInput(attrs={'class': 'form-input'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-input', 'required': True}),
            'cargo': forms.Select(attrs={'class': 'form-input', 'required': True}),
            'sueldo': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'step': '0.01', 'required': True}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-input', 'required': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            # ...otros widgets...
        }
        error_messages = {
            'nombres': {'required': 'El nombre es obligatorio.'},
            'apellidos': {'required': 'El apellido es obligatorio.'},
            'cedula_ecuatoriana': {'required': 'La cédula es obligatoria.'},
            'cargo': {'required': 'El cargo es obligatorio.'},
        }

    def clean_cedula_ecuatoriana(self):
        cedula = self.cleaned_data.get('cedula_ecuatoriana')
        if Empleado.objects.filter(cedula_ecuatoriana=cedula).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Esta cédula ya está registrada para otro empleado.")
        return cedula
