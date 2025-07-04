from django import forms
from applications.core.models import TipoSangre

class TipoSangreForm(forms.ModelForm):
    class Meta:
        model = TipoSangre
        fields = '__all__'
        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'descripcion': forms.TextInput(attrs={'class': 'form-input'}),
        }
        error_messages = {
            'tipo': {'required': 'El tipo de sangre es obligatorio.'},
        }

    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo')
        if TipoSangre.objects.filter(tipo__iexact=tipo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este tipo de sangre ya existe.")
        return tipo
