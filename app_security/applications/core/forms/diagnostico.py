from django import forms
from applications.core.models import Diagnostico
from applications.utils.widgets import MicrophoneTextarea

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'descripcion': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'datos_adicionales': MicrophoneTextarea(attrs={'class': 'form-input', 'rows': 2}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        error_messages = {
            'codigo': {'required': 'El código es obligatorio.'},
            'descripcion': {'required': 'La descripción es obligatoria.'},
        }

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if Diagnostico.objects.filter(codigo__iexact=codigo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este código de diagnóstico ya existe.")
        return codigo
