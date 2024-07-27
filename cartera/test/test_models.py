from django.test import TestCase
from cartera.models import Categoria, Subcategoria, Fuente, Ingreso, Gasto
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


class ModeloTests(TestCase):
    def test_creacion_categoria(self):
        categoria = Categoria.objects.create(nombre="Alimentos")
        self.assertTrue(
            Categoria.objects.filter(nombre="Alimentos").exists(),
            "La categoría no fue creada correctamente",
        )

    def test_creacion_subcategoria(self):
        categoria = Categoria.objects.create(nombre="Entretenimiento")
        subcategoria = Subcategoria.objects.create(nombre="Cine", categoria=categoria)
        self.assertTrue(
            Subcategoria.objects.filter(nombre="Cine", categoria=categoria).exists(),
            "La subcategoría no fue creada correctamente",
        )

    def test_creacion_fuente(self):
        fuente = Fuente.objects.create(nombre="Trabajo")
        self.assertTrue(
            Fuente.objects.filter(nombre="Trabajo").exists(),
            "La fuente no fue creada correctamente",
        )

    def test_creacion_ingreso(self):
        categoria = Categoria.objects.create(nombre="Salario")
        fuente = Fuente.objects.create(nombre="Empresa XYZ")
        ingreso = Ingreso.objects.create(
            fecha="2023-01-01", fuente=fuente, categoria=categoria, cantidad=1000.00
        )
        self.assertTrue(
            Ingreso.objects.filter(
                fecha="2023-01-01", fuente=fuente, categoria=categoria, cantidad=1000.00
            ).exists(),
            "El ingreso no fue creado correctamente",
        )

    def test_creacion_gasto(self):
        categoria = Categoria.objects.create(nombre="Transporte")
        subcategoria = Subcategoria.objects.create(
            nombre="Gasolina", categoria=categoria
        )
        gasto = Gasto.objects.create(
            fecha="2023-01-02",
            categoria=categoria,
            subcategoria=subcategoria,
            cantidad=50.00,
            metodo_pago="Efectivo",
        )
        self.assertTrue(
            Gasto.objects.filter(
                fecha="2023-01-02",
                categoria=categoria,
                subcategoria=subcategoria,
                cantidad=50.00,
                metodo_pago="Efectivo",
            ).exists(),
            "El gasto no fue creado correctamente",
        )

    def test_validacion_categoria_unica(self):
        Categoria.objects.create(nombre="Educación")
        with self.assertRaises(IntegrityError):
            Categoria.objects.create(nombre="Educación")

    def test_actualizacion_categoria(self):
        categoria = Categoria.objects.create(nombre="Salud")
        categoria.nombre = "Salud y Bienestar"
        categoria.save()
        categoria_refrescada = Categoria.objects.get(id=categoria.id)
        self.assertEqual(
            categoria_refrescada.nombre,
            "Salud y Bienestar",
            "El nombre de la categoría no fue actualizado correctamente",
        )

    def test_eliminacion_categoria(self):
        categoria = Categoria.objects.create(nombre="Viajes")
        categoria.delete()
        self.assertFalse(
            Categoria.objects.filter(nombre="Viajes").exists(),
            "La categoría no fue eliminada correctamente",
        )

    def test_creacion_subcategoria_sin_categoria(self):
        with self.assertRaises(IntegrityError):
            Subcategoria.objects.create(nombre="Sin Categoría")

    def test_creacion_ingreso_sin_fuente(self):
        categoria = Categoria.objects.create(nombre="Salario")
        with self.assertRaises(IntegrityError):
            Ingreso.objects.create(
                fecha="2023-01-01", categoria=categoria, cantidad=1000.00
            )

    def test_creacion_gasto_sin_metodo_pago(self):
        categoria = Categoria.objects.create(nombre="Transporte")
        subcategoria = Subcategoria.objects.create(
            nombre="Gasolina", categoria=categoria
        )
        gasto = Gasto(
            fecha="2023-01-02",
            categoria=categoria,
            subcategoria=subcategoria,
            cantidad=50.00,
        )
        with self.assertRaises(ValidationError):
            gasto.full_clean()

    def test_creacion_categoria_vacia(self):
        with self.assertRaises(IntegrityError):
            Categoria.objects.create(nombre=None)

    def test_creacion_ingreso_cantidad_negativa(self):
        categoria = Categoria.objects.create(nombre="Salario")
        fuente = Fuente.objects.create(nombre="Empresa XYZ")
        with self.assertRaises(ValidationError):
            ingreso = Ingreso(
                fecha="2023-01-01",
                fuente=fuente,
                categoria=categoria,
                cantidad=-1000.00,
            )
            ingreso.full_clean()

    def test_creacion_gasto_cantidad_negativa(self):
        categoria = Categoria.objects.create(nombre="Transporte")
        subcategoria = Subcategoria.objects.create(
            nombre="Gasolina", categoria=categoria
        )
        with self.assertRaises(ValidationError):
            gasto = Gasto(
                fecha="2023-01-02",
                categoria=categoria,
                subcategoria=subcategoria,
                cantidad=-50.00,
                metodo_pago="Efectivo",
            )
            gasto.full_clean()

    def test_actualizacion_ingreso(self):
        categoria = Categoria.objects.create(nombre="Salario")
        fuente = Fuente.objects.create(nombre="Empresa XYZ")
        ingreso = Ingreso.objects.create(
            fecha="2023-01-01", fuente=fuente, categoria=categoria, cantidad=1000.00
        )
        ingreso.cantidad = 1200.00
        ingreso.save()
        ingreso_refrescado = Ingreso.objects.get(id=ingreso.id)
        self.assertEqual(
            ingreso_refrescado.cantidad,
            1200.00,
            "El ingreso no fue actualizado correctamente",
        )

    def test_eliminacion_ingreso(self):
        categoria = Categoria.objects.create(nombre="Salario")
        fuente = Fuente.objects.create(nombre="Empresa XYZ")
        ingreso = Ingreso.objects.create(
            fecha="2023-01-01", fuente=fuente, categoria=categoria, cantidad=1000.00
        )
        ingreso.delete()
        self.assertFalse(
            Ingreso.objects.filter(
                fecha="2023-01-01", fuente=fuente, categoria=categoria, cantidad=1000.00
            ).exists(),
            "El ingreso no fue eliminado correctamente",
        )
