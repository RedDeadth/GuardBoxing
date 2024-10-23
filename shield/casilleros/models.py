from django.db import models

class Casillero(models.Model):
    # Campos del casillero
    nombre = models.CharField(max_length=100)
    location = models.CharField(max_length=255)  # Cambiado de 'ubicacion' a 'location'
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True, null=True)  # Cambiado de 'descripcion' a 'description'
    
    # Estado del casillero
    blocked = models.BooleanField(default=False)  # Cambiado de 'estado_bloqueo' a 'blocked'
    open = models.BooleanField(default=False)  # Cambiado de 'apertura' a 'open'
    occupied = models.BooleanField(default=False)  # Estado de ocupado
    userId = models.CharField(max_length=100)  # Campo para el ID del usuario

    def __str__(self):
        return f"{self.nombre} ({self.location})"

    class Meta:
        verbose_name = "Casillero"
        verbose_name_plural = "Casilleros"
