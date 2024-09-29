from django.test import TestCase
from django.core.files.base import ContentFile
from wish.forms import (
    CategoriaForm,
    TiendasForm,
    ProductoForm,
    AlternativaForm,
    DeseoForm,
)
from wish.models import Categoria, Tiendas, Producto, Alternativa


class FormTests(TestCase):
    def setUp(self):
        self.image_file = ContentFile(b"fake_image_data", name="test_image.png")

    def tearDown(self):
        self.image_file.close()

    def test_categoria_form_valid(self):
        form_data = {"nombre": "Electrónica"}
        form = CategoriaForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["nombre"], "Electrónica")

    def test_categoria_form_invalid(self):
        form_data = {"nombre": ""}
        form = CategoriaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("nombre", form.errors)

    def test_tiendas_form_valid(self):
        form_data = {
            "nombre": "Amazon",
            "enlace": "https://www.amazon.com",
            "logo": self.image_file,
        }
        form = TiendasForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["nombre"], "Amazon")

    def test_tiendas_form_invalid(self):
        form_data = {
            "nombre": "",
            "enlace": "not_a_url",
            "logo": self.image_file,
        }
        form = TiendasForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_producto_form_valid(self):
        form_data = {
            "nombre": "Laptop",
            "imagen": self.image_file,
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["nombre"], "Laptop")

    def test_producto_con_varias_alternativas(self):
        producto = Producto.objects.create(nombre="Laptop", imagen=self.image_file)

        tienda1 = Tiendas.objects.create(
            nombre="Amazon", enlace="https://www.amazon.com"
        )
        tienda2 = Tiendas.objects.create(nombre="eBay", enlace="https://www.ebay.com")

        Alternativa.objects.create(
            producto=producto,
            tienda=tienda1,
            enlace="https://www.amazon.com/laptop",
            imagen=self.image_file,
            costo=1200.00,
        )
        Alternativa.objects.create(
            producto=producto,
            tienda=tienda2,
            enlace="https://www.ebay.com/laptop",
            imagen=self.image_file,
            costo=1150.00,
        )

        self.assertEqual(Alternativa.objects.filter(producto=producto).count(), 2)

    def test_dos_productos_con_varias_alternativas(self):
        producto1 = Producto.objects.create(nombre="Laptop", imagen=self.image_file)
        producto2 = Producto.objects.create(nombre="Smartphone", imagen=self.image_file)

        tienda1 = Tiendas.objects.create(
            nombre="Amazon", enlace="https://www.amazon.com"
        )
        tienda2 = Tiendas.objects.create(nombre="eBay", enlace="https://www.ebay.com")
        tienda3 = Tiendas.objects.create(
            nombre="BestBuy", enlace="https://www.bestbuy.com"
        )
        tienda4 = Tiendas.objects.create(
            nombre="Walmart", enlace="https://www.walmart.com"
        )

        Alternativa.objects.create(
            producto=producto1,
            tienda=tienda1,
            enlace="https://www.amazon.com/laptop",
            imagen=self.image_file,
            costo=1200.00,
        )
        Alternativa.objects.create(
            producto=producto1,
            tienda=tienda2,
            enlace="https://www.ebay.com/laptop",
            imagen=self.image_file,
            costo=1150.00,
        )

        Alternativa.objects.create(
            producto=producto2,
            tienda=tienda3,
            enlace="https://www.bestbuy.com/smartphone",
            imagen=self.image_file,
            costo=800.00,
        )
        Alternativa.objects.create(
            producto=producto2,
            tienda=tienda4,
            enlace="https://www.walmart.com/smartphone",
            imagen=self.image_file,
            costo=850.00,
        )

        self.assertEqual(Alternativa.objects.filter(producto=producto1).count(), 2)
        self.assertEqual(Alternativa.objects.filter(producto=producto2).count(), 2)

    def test_alternativa_form_valid(self):
        categoria = Categoria.objects.create(nombre="Electrónica")
        tienda = Tiendas.objects.create(
            nombre="Amazon", enlace="https://www.amazon.com"
        )
        producto = Producto.objects.create(nombre="Laptop", imagen="image.png")
        form_data = {
            "producto": producto.id,
            "tienda": tienda.id,
            "enlace": "https://www.amazon.com/laptop",
            "imagen": self.image_file,
            "costo": 1200.00,
        }
        form = AlternativaForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_deseo_form_valid(self):
        categoria = Categoria.objects.create(nombre="Electrónica")
        producto = Producto.objects.create(nombre="Laptop", imagen="image.png")
        form_data = {
            "categoria": categoria.id,
            "producto": producto.id,
        }
        form = DeseoForm(data=form_data)
        self.assertTrue(form.is_valid())
