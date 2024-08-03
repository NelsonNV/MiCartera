from django.db import models
from django.core.exceptions import ValidationError


class Categoria(models.Model):
    nombre = models.CharField(unique=True, max_length=50)

    objects = models.Manager()

    def __str__(self):
        return str(self.nombre)


class Subcategoria(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"


class Fuente(models.Model):
    nombre = models.CharField(unique=True, max_length=100)

    objects = models.Manager()

    def __str__(self):
        return str(self.nombre)


class Ingreso(models.Model):
    fecha = models.DateField()
    fuente = models.ForeignKey(Fuente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)

    objects = models.Manager()

    def clean(self):
        if self.cantidad is not None and self.cantidad < 0:
            raise ValidationError("La cantidad no puede ser negativa.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fuente}: ${self.cantidad}"


class MetodoPago(models.Model):
    metodo = models.CharField(unique=True, max_length=100)
    objects = models.Manager()

    def __str__(self):
        return f"{self.metodo}"


class Gasto(models.Model):
    fecha = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)

    objects = models.Manager()

    def clean(self):
        if self.cantidad is not None and self.cantidad < 0:
            raise ValidationError("La cantidad no puede ser negativa.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.categoria}: {self.cantidad}"
