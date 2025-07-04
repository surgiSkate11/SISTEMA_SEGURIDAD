from django import forms
from applications.doctor.models import ServiciosAdicionales

class ServiciosAdicionalesForm(forms.ModelForm):
    class Meta:
        model = ServiciosAdicionales
        fields = ['nombre_servicio', 'costo_servicio', 'descripcion', 'activo']
        widgets = {
            'nombre_servicio': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'costo_servicio': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01', 'required': True}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_nombre_servicio(self):
        nombre = self.cleaned_data['nombre_servicio']
        if ServiciosAdicionales.objects.filter(nombre_servicio__iexact=nombre).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un servicio con este nombre.")
        return nombre

    def clean_costo_servicio(self):
        costo = self.cleaned_data['costo_servicio']
        if costo is None or costo <= 0:
            raise forms.ValidationError("El costo debe ser mayor a 0.")
        return costo
