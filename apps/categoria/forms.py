from django import forms
from .models import Categoria



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('nombre',)
        labels = {
            'nombre': 'Nombre de la Categoría',
        }

    def clean_name(self):
        name = self.cleaned_data['nombre']
        if not name.strip():
            raise forms.ValidationError("El nombre de la categoría no puede estar vacío.")
        return name
