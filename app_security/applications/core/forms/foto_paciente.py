from django import forms
from applications.core.models import FotoPaciente

class FotoPacienteForm(forms.ModelForm):
    class Meta:
        model = FotoPaciente
        fields = ['imagen', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 2, 'class': 'form-input w-full'}),
        }

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            ext = imagen.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'pdf']:
                raise forms.ValidationError('Formato no permitido. Solo imágenes o PDF.')
            if imagen.size > 10*1024*1024:
                raise forms.ValidationError('El archivo no debe superar los 10MB.')
        return imagen
