from django import forms
from applications.core.models import Doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'apellidos': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'ruc': forms.TextInput(attrs={'class': 'form-input', 'required': True, 'pattern': r'^[0-9]{13}$', 'title': 'Debe tener 13 dígitos'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-input', 'required': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'codigo_unico_doctor': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'telefonos': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'horario_atencion': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'duracion_atencion': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            # ...otros widgets...
        }
        error_messages = {
            'nombres': {'required': 'El nombre es obligatorio.'},
            'apellidos': {'required': 'El apellido es obligatorio.'},
            'ruc': {'required': 'El RUC es obligatorio.'},
            'codigo_unico_doctor': {'required': 'El código único es obligatorio.'},
        }

    def clean_ruc(self):
        ruc = self.cleaned_data.get('ruc')
        if Doctor.objects.filter(ruc=ruc).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este RUC ya está registrado para otro doctor.")
        return ruc

    def clean_codigo_unico_doctor(self):
        codigo = self.cleaned_data.get('codigo_unico_doctor')
        if Doctor.objects.filter(codigo_unico_doctor=codigo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este código ya está registrado para otro doctor.")
        return codigo
