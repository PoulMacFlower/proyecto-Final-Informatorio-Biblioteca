from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="home"),
    path('accounts/', include('apps.usuario.urls')),
    path('categorias/', include('apps.categoria.urls')),
    path('articulos/', include('apps.articulo.urls')),
    path('comentarios/', include('apps.comentarios.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handling404 = 'views.handling_404'
