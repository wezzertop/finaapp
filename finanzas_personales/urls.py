from django.contrib import admin
from django.urls import path, include # Asegúrate de importar 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Incluimos las URLs de la app 'gestion' en la raíz del sitio
    path('', include('gestion.urls')),
]
