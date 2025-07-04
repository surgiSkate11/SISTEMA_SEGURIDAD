from django import forms
from applications.core.models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-input', 'required': True}),
            'telefono': forms.TextInput(attrs={'class': 'form-input', 'pattern': r'^[0-9, ]+$', 'title': 'Solo números y comas', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'ejemplo@correo.com'}),
            'nombres': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'apellidos': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'cedula_ecuatoriana': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'dni': forms.TextInput(attrs={'class': 'form-input'}),
            'direccion': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            # ...otros widgets según el modelo...
        }
        error_messages = {
            'nombres': {'required': 'El nombre es obligatorio.'},
            'apellidos': {'required': 'El apellido es obligatorio.'},
            'cedula_ecuatoriana': {'required': 'La cédula es obligatoria.'},
            'telefono': {'required': 'El teléfono es obligatorio.'},
            'fecha_nacimiento': {'required': 'La fecha de nacimiento es obligatoria.'},
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        if not all(x.isdigit() or x in ', ' for x in telefono):
            raise forms.ValidationError("El teléfono solo debe contener números y comas.")
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Paciente.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este correo ya está registrado para otro paciente.")
        return email

    def clean_cedula_ecuatoriana(self):
        cedula = self.cleaned_data.get('cedula_ecuatoriana')
        if Paciente.objects.filter(cedula_ecuatoriana=cedula).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Esta cédula ya está registrada para otro paciente.")
        return cedula

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        from datetime import date
        if fecha:
            if fecha > date.today():
                raise forms.ValidationError("La fecha de nacimiento no puede ser en el futuro.")
            edad = (date.today() - fecha).days // 365
            if edad > 125:
                raise forms.ValidationError("La edad no puede ser mayor a 125 años (el récord mundial es 122 años).")
        return fecha
