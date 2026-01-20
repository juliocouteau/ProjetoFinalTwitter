from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Aqui dizemos ao Django para procurar as rotas dentro da pasta twitter
    path('', include('twitter.urls')), 
]

# Configuração para imagens de perfil aparecerem
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)