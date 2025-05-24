from django.contrib import admin
from .models import Categoria, Cartera, Transaccion

# Personalización para el modelo Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',) # Campos a mostrar en la lista
    search_fields = ('nombre',) # Habilita un campo de búsqueda

# Personalización para el modelo Cartera
@admin.register(Cartera)
class CarteraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'saldo_inicial') # Campos a mostrar
    search_fields = ('nombre',)

# Personalización para el modelo Transaccion
@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'tipo', 'monto', 'categoria', 'cartera', 'descripcion') # Campos a mostrar
    list_filter = ('tipo', 'categoria', 'cartera', 'fecha') # Habilita filtros en el lateral
    search_fields = ('descripcion', 'categoria__nombre', 'cartera__nombre') # Búsqueda (incluye campos relacionados)
    list_per_page = 25 # Paginación
    date_hierarchy = 'fecha' # Navegación por fechas

# Si no quisieras personalización, podrías usar:
# admin.site.register(Categoria)
# admin.site.register(Cartera)
# admin.site.register(Transaccion)
