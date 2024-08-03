from django.test import TestCase
from cartera import forms, models


class CategoriaFormTest(TestCase):
    def test_categoria_form_valid(self):
        form = forms.CategoriaForm(data={"nombre": "Alimentos"})
        self.assertTrue(form.is_valid())

    def test_categoria_form_invalid(self):
        form = forms.CategoriaForm(data={"nombre": ""})
        self.assertFalse(form.is_valid())

    def test_categoria_form_duplicate(self):
        models.Categoria.objects.create(nombre="Alimentos")
        form = forms.CategoriaForm(data={"nombre": "Alimentos"})
        self.assertFalse(form.is_valid())


class SubcategoriaFormTest(TestCase):
    def test_subcategoria_form_valid(self):
        categoria = models.Categoria.objects.create(nombre="Alimentos")
        form = forms.SubcategoriaForm(
            data={"nombre": "Frutas", "categoria": categoria.id}
        )
        self.assertTrue(form.is_valid())

    def test_subcategoria_form_invalid(self):
        form = forms.SubcategoriaForm(data={"nombre": "", "categoria": ""})
        self.assertFalse(form.is_valid())

    def test_subcategoria_form_invalid_no_categoria(self):
        form = forms.SubcategoriaForm(data={"nombre": "Frutas", "categoria": ""})
        self.assertFalse(form.is_valid())

    def test_subcategoria_form_duplicate(self):
        categoria = models.Categoria.objects.create(nombre="Alimentos")
        models.Subcategoria.objects.create(nombre="Frutas", categoria=categoria)
        form = forms.SubcategoriaForm(
            data={"nombre": "Frutas", "categoria": categoria.id}
        )
        self.assertFalse(form.is_valid())

    def test_subcategoria_form_invalid_no_nombre(self):
        categoria = models.Categoria.objects.create(nombre="Alimentos")
        form = forms.SubcategoriaForm(data={"nombre": "", "categoria": categoria.id})
        self.assertFalse(form.is_valid())


class FuenteFormTest(TestCase):
    def test_fuente_form_valid(self):
        form = forms.FuenteForm(data={"nombre": "Salario"})
        self.assertTrue(form.is_valid())

    def test_fuente_form_invalid(self):
        form = forms.FuenteForm(data={"nombre": ""})
        self.assertFalse(form.is_valid())

    def test_fuente_form_duplicate(self):
        models.Fuente.objects.create(nombre="Salario")
        form = forms.FuenteForm(data={"nombre": "Salario"})
        self.assertFalse(form.is_valid())


class IngresoFormTest(TestCase):
    def setUp(self):
        self.fuente = models.Fuente.objects.create(nombre="Trabajo")

    def test_ingreso_form_valid(self):
        form = forms.IngresoForm(
            data={
                "fecha": "2024-07-27",
                "fuente": self.fuente.id,
                "cantidad": 1500.00,  # Ingresar como número
                "descripcion": "Salario mensual",
            }
        )
        self.assertTrue(form.is_valid())

    def test_ingreso_form_invalid(self):
        form = forms.IngresoForm(
            data={
                "fecha": "",
                "fuente": "",
                "cantidad": "",
                "descripcion": "",
            }
        )
        self.assertFalse(form.is_valid())

    def test_ingreso_form_invalid_no_fecha(self):
        form = forms.IngresoForm(
            data={
                "fecha": "",
                "fuente": self.fuente.id,
                "cantidad": 1500.00,
                "descripcion": "Salario mensual",
            }
        )
        self.assertFalse(form.is_valid())

    def test_ingreso_form_invalid_no_fuente(self):
        form = forms.IngresoForm(
            data={
                "fecha": "2024-07-27",
                "fuente": "",
                "cantidad": 1500.00,
                "descripcion": "Salario mensual",
            }
        )
        self.assertFalse(form.is_valid())

    def test_ingreso_form_invalid_no_cantidad(self):
        form = forms.IngresoForm(
            data={
                "fecha": "2024-07-27",
                "fuente": self.fuente.id,
                "cantidad": "",
                "descripcion": "Salario mensual",
            }
        )
        self.assertFalse(form.is_valid())

    def test_ingreso_form_valid_no_descripcion(self):
        form = forms.IngresoForm(
            data={
                "fecha": "2024-07-27",
                "fuente": self.fuente.id,
                "cantidad": 1500.00,
                "descripcion": "",
            }
        )
        self.assertTrue(form.is_valid())

    def test_ingreso_form_invalid_negative_amount(self):
        form = forms.IngresoForm(
            data={
                "fecha": "2024-07-27",
                "fuente": self.fuente.id,
                "cantidad": -1500.00,
                "descripcion": "Salario mensual",
            }
        )
        self.assertFalse(form.is_valid())

    def test_ingreso_form_invalid_string_amount(self):
        form = forms.IngresoForm(
            data={
                "fecha": "2024-07-27",
                "fuente": self.fuente.id,
                "cantidad": "mil quinientos",
                "descripcion": "Salario mensual",
            }
        )
        self.assertFalse(form.is_valid())


class GastoFormTest(TestCase):
    def setUp(self):
        self.metodopago = models.MetodoPago.objects.create(metodo="efectivo")
        self.categoria = models.Categoria.objects.create(nombre="Transporte")
        self.subcategoria = models.Subcategoria.objects.create(
            nombre="Taxi", categoria=self.categoria
        )

    def test_gasto_form_valid(self):
        form = forms.GastoForm(
            data={
                "fecha": "2024-07-27",
                "categoria": self.categoria.id,
                "subcategoria": self.subcategoria.id,
                "cantidad": 20.00,  # Ingresar como número
                "metodo_pago": self.metodopago.id,
                "descripcion": "Viaje en taxi",
            }
        )
        self.assertTrue(form.is_valid())

    def test_gasto_form_invalid(self):
        form = forms.GastoForm(
            data={
                "fecha": "",
                "categoria": "",
                "subcategoria": "",
                "cantidad": "",
                "metodo_pago": "",
                "descripcion": "",
            }
        )
        self.assertFalse(form.is_valid())

    def test_gasto_form_invalid_no_fecha(self):
        form = forms.GastoForm(
            data={
                "fecha": "",
                "categoria": self.categoria.id,
                "subcategoria": self.subcategoria.id,
                "cantidad": 20.00,
                "metodo_pago": "Efectivo",
                "descripcion": "Viaje en taxi",
            }
        )
        self.assertFalse(form.is_valid())

    def test_gasto_form_invalid_no_categoria(self):
        form = forms.GastoForm(
            data={
                "fecha": "2024-07-27",
                "categoria": "",
                "subcategoria": self.subcategoria.id,
                "cantidad": 20.00,
                "metodo_pago": self.metodopago.id,
                "descripcion": "Viaje en taxi",
            }
        )
        self.assertFalse(form.is_valid())

    def test_gasto_form_invalid_no_subcategoria(self):
        form = forms.GastoForm(
            data={
                "fecha": "2024-07-27",
                "categoria": self.categoria.id,
                "subcategoria": "",
                "cantidad": 20.00,
                "metodo_pago": self.metodopago.id,
                "descripcion": "Viaje en taxi",
            }
        )
        self.assertFalse(form.is_valid())

    def test_gasto_form_invalid_no_cantidad(self):
        form = forms.GastoForm(
            data={
                "fecha": "2024-07-27",
                "categoria": self.categoria.id,
                "subcategoria": self.subcategoria.id,
                "cantidad": "",
                "metodo_pago": self.metodopago.id,
                "descripcion": "Viaje en taxi",
            }
        )
        self.assertFalse(form.is_valid())

    def test_gasto_form_invalid_no_metodo_pago(self):
        form = forms.GastoForm(
            data={
                "fecha": "2024-07-27",
                "categoria": self.categoria.id,
                "subcategoria": self.subcategoria.id,
                "cantidad": 20.00,
                "metodo_pago": "",
                "descripcion": "Viaje en taxi",
            }
        )
        self.assertFalse(form.is_valid())

    def test_gasto_form_valid_no_descripcion(self):
        form = forms.GastoForm(
            data={
                "fecha": "2024-07-27",
                "categoria": self.categoria.id,
                "subcategoria": self.subcategoria.id,
                "cantidad": 20.00,
                "metodo_pago": self.metodopago.id,
                "descripcion": "",
            }
        )
        self.assertTrue(form.is_valid())

    def test_gasto_form_invalid_negative_amount(self):
        form = forms.GastoForm(
            data={
                "fecha": "2024-07-27",
                "categoria": self.categoria.id,
                "subcategoria": self.subcategoria.id,
                "cantidad": -20.00,
                "metodo_pago": "Efectivo",
                "descripcion": "Viaje en taxi",
            }
        )
        self.assertFalse(form.is_valid())

    def test_gasto_form_invalid_string_amount(self):
        form = forms.GastoForm(
            data={
                "fecha": "2024-07-27",
                "categoria": self.categoria.id,
                "subcategoria": self.subcategoria.id,
                "cantidad": "veinte",
                "metodo_pago": "Efectivo",
                "descripcion": "Viaje en taxi",
            }
        )
        self.assertFalse(form.is_valid())
