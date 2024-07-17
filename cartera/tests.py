from django.test import TestCase
from django.urls import reverse
from .models import Ingreso, Gasto, Categoria, Subcategoria, Fuente
from decimal import Decimal
from datetime import date
from django.db.models import Sum
from .forms import CategoriaForm, SubcategoriaForm, FuenteForm, IngresoForm, GastoForm


class TestFinanzas(TestCase):
    def setUp(self):
        # Crear categorías y subcategorías
        self.categoria_comida = Categoria.objects.create(nombre="Comida")
        self.subcategoria_restaurantes = Subcategoria.objects.create(
            nombre="Restaurantes", categoria=self.categoria_comida
        )
        self.subcategoria_supermercados = Subcategoria.objects.create(
            nombre="Supermercados", categoria=self.categoria_comida
        )

        # Crear fuentes
        self.fuente_salario = Fuente.objects.create(nombre="Salario")
        self.fuente_ahorros = Fuente.objects.create(nombre="Ahorros")

        # Crear ingresos
        Ingreso.objects.create(
            fecha=date.today(),
            fuente=self.fuente_salario,
            categoria=self.categoria_comida,
            cantidad=Decimal("1500.00"),
        )
        Ingreso.objects.create(
            fecha=date.today(),
            fuente=self.fuente_ahorros,
            categoria=self.categoria_comida,
            cantidad=Decimal("300.00"),
        )

        # Crear gastos
        Gasto.objects.create(
            fecha=date.today(),
            categoria=self.categoria_comida,
            subcategoria=self.subcategoria_restaurantes,
            cantidad=Decimal("50.00"),
            metodo_pago="Tarjeta",
        )
        Gasto.objects.create(
            fecha=date.today(),
            categoria=self.categoria_comida,
            subcategoria=self.subcategoria_supermercados,
            cantidad=Decimal("80.00"),
            metodo_pago="Efectivo",
        )

    def test_ingresos(self):
        total_ingresos = Ingreso.objects.aggregate(total=Sum("cantidad"))["total"]
        self.assertEqual(total_ingresos, Decimal("1800.00"))

    def test_gastos(self):
        total_gastos = Gasto.objects.aggregate(total=Sum("cantidad"))["total"]
        self.assertEqual(total_gastos, Decimal("130.00"))

    def test_subcategoria(self):
        gasto = Gasto.objects.get(subcategoria__nombre="Restaurantes")
        self.assertIsNotNone(gasto)  # Asegurarse de que el objeto gasto no sea None


class TestForms(TestCase):
    def test_categoria_form_valid(self):
        form_data = {"nombre": "Mi categoría"}
        form = CategoriaForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_subcategoria_form_valid(self):
        categoria = Categoria.objects.create(nombre="Comida")
        form_data = {"nombre": "Supermercados", "categoria": categoria.id}
        form = SubcategoriaForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_fuente_form_valid(self):
        form_data = {"nombre": "Salario"}
        form = FuenteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_ingreso_form_valid(self):
        categoria = Categoria.objects.create(nombre="Comida")
        fuente = Fuente.objects.create(nombre="Salario")
        form_data = {
            "fecha": date.today(),
            "fuente": fuente.id,
            "categoria": categoria.id,
            "cantidad": "1500.00",
            "descripcion": "Salario mensual",
        }
        form = IngresoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_gasto_form_valid(self):
        categoria = Categoria.objects.create(nombre="Comida")
        subcategoria = Subcategoria.objects.create(
            nombre="Restaurantes", categoria=categoria
        )
        form_data = {
            "fecha": date.today(),
            "categoria": categoria.id,
            "subcategoria": subcategoria.id,
            "cantidad": "50.00",
            "metodo_pago": "Tarjeta",
            "descripcion": "Cena en restaurante",
        }
        form = GastoForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestViews(TestCase):
    def setUp(self):
        # Crear categorías y subcategorías para las pruebas
        self.categoria_comida = Categoria.objects.create(nombre="Comida")
        self.subcategoria_restaurantes = Subcategoria.objects.create(
            nombre="Restaurantes", categoria=self.categoria_comida
        )
        self.subcategoria_supermercados = Subcategoria.objects.create(
            nombre="Supermercados", categoria=self.categoria_comida
        )

        # Crear fuentes para las pruebas
        self.fuente_salario = Fuente.objects.create(nombre="Salario")
        self.fuente_ahorros = Fuente.objects.create(nombre="Ahorros")

    def test_formulario_GET(self):
        # Prueba GET request a la vista formulario
        url = reverse("formulario")  # Obtener la URL usando el nombre de la vista
        response = self.client.get(url)

        # Verificar que la respuesta sea exitosa (código 200)
        self.assertEqual(response.status_code, 200)

        # Verificar que todos los formularios están presentes en el contexto
        self.assertIn("forms", response.context)
        forms = response.context["forms"]

        # Verificar que cada formulario es una instancia correcta de su clase respectiva
        self.assertIsInstance(forms["categoria"], CategoriaForm)
        self.assertIsInstance(forms["subcategoria"], SubcategoriaForm)
        self.assertIsInstance(forms["fuente"], FuenteForm)
        self.assertIsInstance(forms["ingreso"], IngresoForm)
        self.assertIsInstance(forms["gasto"], GastoForm)

    def test_formulario_POST(self):
        # Prueba POST request a la vista formulario para guardar una categoría
        url = reverse("formulario")
        form_data = {"form_type": "categoria", "nombre": "Nueva Categoría"}
        response = self.client.post(url, form_data)

        # Verificar que se redirige después de un POST exitoso
        self.assertRedirects(response, reverse("formulario"))

        # Verificar que la nueva categoría fue creada
        nueva_categoria = Categoria.objects.get(nombre="Nueva Categoría")
        self.assertEqual(nueva_categoria.nombre, "Nueva Categoría")
