from django import forms
from .models import Articles

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ('title', 'content', 'image', 'date_published', 'category')
        labels = {
            'title': 'Título',
            'content': 'Contenido',
            'image': 'Imagen',
            'date_published': 'Fecha de Publicación',
            'category': 'Categoría',
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if not title.strip():
            raise forms.ValidationError("El título no puede estar vacío.")
        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        if not content.strip():
            raise forms.ValidationError("El contenido no puede estar vacío.")
        return content

   


