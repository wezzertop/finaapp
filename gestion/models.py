from django.db import models
from django.utils import timezone

# Modelo para las Categorías
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

# Modelo para las Carteras
class Cartera(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    saldo_inicial = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name="Saldo Inicial")
    # Podríamos añadir un campo 'saldo_actual' que se actualice con cada transacción,
    # pero calcularlo dinámicamente suele ser más seguro, aunque menos performante.
    # Por ahora lo dejamos así.

    class Meta:
        verbose_name = "Cartera"
        verbose_name_plural = "Carteras"

    def __str__(self):
        return self.nombre

# Modelo para las Transacciones
class Transaccion(models.Model):
    # Definimos las opciones para el tipo de transacción
    TIPO_CHOICES = [
        ('I', 'Ingreso'),
        ('G', 'Gasto'),
    ]

    fecha = models.DateField(default=timezone.now, verbose_name="Fecha")
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, verbose_name="Tipo")
    monto = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Monto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    # Relaciones con Categoria y Cartera
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT, # Evita borrar una categoría si tiene transacciones
        related_name='transacciones',
        verbose_name="Categoría"
    )
    cartera = models.ForeignKey(
        Cartera,
        on_delete=models.CASCADE, # Si se borra una cartera, se borran sus transacciones
        related_name='transacciones',
        verbose_name="Cartera"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"
        ordering = ['-fecha'] # Ordena las transacciones por fecha descendente por defecto

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.monto} el {self.fecha}"


