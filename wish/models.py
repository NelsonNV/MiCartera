from django.db import models
from django.core.exceptions import ValidationError


class Categoria(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    objects = models.Manager()

    def __str__(self):
        return f"{self.nombre}"


class Tiendas(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    enlace = models.CharField(unique=True, max_length=250)
    logo = models.ImageField(blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.nombre}"


class Producto(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    imagen = models.ImageField(blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.nombre}"


class alternativa(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tienda = models.ForeignKey(Tiendas, on_delete=models.CASCADE)
    enlace = models.CharField(unique=True, max_length=50)
    imagen = models.ImageField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, max_length=100)
    objects = models.Manager()

    def clean(self):
        if self.costo is not None and self.costo < 0:
            raise ValidationError("La cantidad no puede ser negativa.")


class Deseo(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return f"{self.producto}"
