from django import forms
from applications.core.models import TipoGasto

class TipoGastoForm(forms.ModelForm):
    class Meta:
        model = TipoGasto
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        error_messages = {
            'nombre': {'required': 'El nombre del tipo de gasto es obligatorio.'},
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if TipoGasto.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este tipo de gasto ya existe.")
        return nombre
