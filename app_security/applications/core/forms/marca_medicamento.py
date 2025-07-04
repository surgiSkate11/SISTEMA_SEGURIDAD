from django import forms
from applications.core.models import MarcaMedicamento

class MarcaMedicamentoForm(forms.ModelForm):
    class Meta:
        model = MarcaMedicamento
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        error_messages = {
            'nombre': {'required': 'El nombre de la marca es obligatorio.'},
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if MarcaMedicamento.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Esta marca de medicamento ya existe.")
        return nombre
