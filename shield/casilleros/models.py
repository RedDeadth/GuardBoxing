from django.db import models

class Casillero(models.Model):
    # Campos del casillero
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)

    # Estado del casillero
    estado_bloqueo = models.BooleanField(default=False)  # Si es True, está bloqueado; False, desbloqueado
    apertura = models.CharField(
        max_length=10,
        choices=[('abierto', 'Abierto'), ('cerrado', 'Cerrado')],
        default='cerrado'
    )  # Estado de apertura del casillero: Abierto o Cerrado

    def __str__(self):
        return f"{self.nombre} ({self.ubicacion})"

    class Meta:
        verbose_name = "Casillero"
        verbose_name_plural = "Casilleros"
