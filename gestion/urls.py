from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('', views.index, name='index'),
    # Transacciones
    path('transaccion/nueva/', views.crear_transaccion, name='crear_transaccion'),
    path('transacciones/', views.listar_transacciones, name='listar_transacciones'),
    # Categorías
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:pk>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),
    # Carteras
    path('carteras/', views.listar_carteras, name='listar_carteras'),
    path('carteras/nueva/', views.crear_cartera, name='crear_cartera'),
    # Nuevas URLs para Editar y Eliminar Carteras
    path('carteras/<int:pk>/editar/', views.editar_cartera, name='editar_cartera'),
    path('carteras/<int:pk>/eliminar/', views.eliminar_cartera, name='eliminar_cartera'),
]
