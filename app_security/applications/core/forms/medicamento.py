from django import forms
from applications.core.models import Medicamento

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'concentracion': forms.TextInput(attrs={'class': 'form-input'}),
            'via_administracion': forms.Select(attrs={'class': 'form-input', 'required': True}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'required': True}),
            'precio': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'step': '0.01', 'required': True}),
            'comercial': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        error_messages = {
            'nombre': {'required': 'El nombre del medicamento es obligatorio.'},
            'via_administracion': {'required': 'La vía de administración es obligatoria.'},
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Medicamento.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este medicamento ya existe.")
        return nombre
