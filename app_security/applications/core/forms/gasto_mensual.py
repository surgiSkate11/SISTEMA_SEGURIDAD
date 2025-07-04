from django import forms
from applications.core.models import GastoMensual

class GastoMensualForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Forzar el valor inicial de fecha en formato YYYY-MM-DD si existe
        if self.instance and self.instance.pk and self.instance.fecha:
            self.initial['fecha'] = self.instance.fecha.strftime('%Y-%m-%d')

    class Meta:
        model = GastoMensual
        # Excluir el campo user si se asigna automáticamente en la vista
        exclude = ['user']
        widgets = {
            'tipo_gasto': forms.Select(attrs={'class': 'form-input', 'required': True}),
            # Usar el formato por defecto para type="date" (YYYY-MM-DD)
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-input', 'required': True}),
            'valor': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'step': '0.01', 'required': True}),
            'observacion': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
        }
        error_messages = {
            'tipo_gasto': {'required': 'El tipo de gasto es obligatorio.'},
            'fecha': {'required': 'La fecha es obligatoria.'},
            'valor': {'required': 'El valor es obligatorio.'},
        }
