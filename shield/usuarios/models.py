from django.db import models

class Usuario(models.Model):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.email
