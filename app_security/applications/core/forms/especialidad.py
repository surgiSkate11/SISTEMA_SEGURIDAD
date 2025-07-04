from django import forms
from applications.core.models import Especialidad

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        error_messages = {
            'nombre': {'required': 'El nombre de la especialidad es obligatorio.'},
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Especialidad.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Esta especialidad ya existe.")
        return nombre
