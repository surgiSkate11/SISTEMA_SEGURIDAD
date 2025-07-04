from django import forms
from django.utils import timezone
from applications.doctor.models import  Pago, DetallePago


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = [
            'atencion', 'metodo_pago', 'estado', 'fecha_pago',
            'nombre_pagador', 'referencia_externa', 'evidencia_pago', 'observaciones', 'activo'
        ]
        widgets = {
            'atencion': forms.Select(attrs={'class': 'form-control'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'estado': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'fecha_pago': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'nombre_pagador': forms.TextInput(attrs={'class': 'form-control'}),
            'referencia_externa': forms.TextInput(attrs={'class': 'form-control'}),
            'evidencia_pago': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_monto_total(self):
        monto = self.cleaned_data['monto_total']
        if monto is None or monto < 0:
            raise forms.ValidationError("El monto total debe ser mayor o igual a 0.")
        return monto

    def clean(self):
        cleaned_data = super().clean()
        metodo = cleaned_data.get('metodo_pago')
        referencia = cleaned_data.get('referencia_externa')
        evidencia = cleaned_data.get('evidencia_pago')
        if metodo and metodo != 'efectivo':
            if not referencia:
                self.add_error('referencia_externa', 'La referencia es obligatoria para pagos no en efectivo.')
            if not evidencia:
                self.add_error('evidencia_pago', 'Debe adjuntar evidencia para pagos no en efectivo.')
        return cleaned_data

class DetallePagoForm(forms.ModelForm):
    class Meta:
        model = DetallePago
        fields = [
            'servicio_adicional', 'cantidad', 'precio_unitario', 'descuento_porcentaje',
            'aplica_seguro', 'valor_seguro', 'descripcion_seguro'
        ]
        widgets = {
            'servicio_adicional': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'required': True}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01', 'required': True}),
            'descuento_porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'step': '0.01'}),
            'aplica_seguro': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'valor_seguro': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'descripcion_seguro': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        if cantidad is None or cantidad < 1:
            raise forms.ValidationError("La cantidad debe ser mayor o igual a 1.")
        return cantidad

    def clean_precio_unitario(self):
        precio = self.cleaned_data['precio_unitario']
        if precio is None or precio < 0:
            raise forms.ValidationError("El precio unitario debe ser mayor o igual a 0.")
        return precio

    def clean_descuento_porcentaje(self):
        descuento = self.cleaned_data['descuento_porcentaje']
        if descuento is not None and (descuento < 0 or descuento > 100):
            raise forms.ValidationError("El descuento debe estar entre 0 y 100.")
        return descuento

    def clean(self):
        cleaned_data = super().clean()
        aplica_seguro = cleaned_data.get('aplica_seguro')
        valor_seguro = cleaned_data.get('valor_seguro')
        if aplica_seguro and (valor_seguro is None or valor_seguro <= 0):
            self.add_error('valor_seguro', 'Debe ingresar el valor cubierto por el seguro.')
        return cleaned_data
