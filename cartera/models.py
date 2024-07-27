from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return str(self.nombre)


class Subcategoria(models.Model):
    nombre = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"


class Fuente(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return str(self.nombre)


class Ingreso(models.Model):
    fecha = models.DateField()
    fuente = models.ForeignKey(Fuente, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.categoria}: {self.cantidad}"


class Gasto(models.Model):
    fecha = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(
        Subcategoria, on_delete=models.SET_NULL, blank=True, null=True
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.categoria}: {self.cantidad}"
