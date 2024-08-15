from django.test import TestCase
from django.core.exceptions import ValidationError
from wish.models import Categoria, Tiendas, Producto, Alternativa, Deseo


class CategoriaModelTest(TestCase):
    def test_categoria_nombre_unico(self):
        Categoria.objects.create(nombre="Electrónica")
        with self.assertRaises(ValidationError):
            cat = Categoria(nombre="Electrónica")
            cat.full_clean()


class TiendasModelTest(TestCase):
    def test_tienda_nombre_unico(self):
        Tiendas.objects.create(nombre="Amazon", enlace="https://amazon.com")
        with self.assertRaises(ValidationError):
            tienda = Tiendas(nombre="Amazon", enlace="https://amazon.com/store")
            tienda.full_clean()

    def test_tienda_enlace_unico(self):
        Tiendas.objects.create(nombre="BestBuy", enlace="https://bestbuy.com")
        with self.assertRaises(ValidationError):
            tienda = Tiendas(nombre="Walmart", enlace="https://bestbuy.com")
            tienda.full_clean()


class ProductoModelTest(TestCase):
    def test_producto_nombre_unico(self):
        Producto.objects.create(nombre="Laptop")
        with self.assertRaises(ValidationError):
            producto = Producto(nombre="Laptop")
            producto.full_clean()


class AlternativaModelTest(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(nombre="Smartphone")
        self.tienda = Tiendas.objects.create(nombre="eBay", enlace="https://ebay.com")

    def test_Alternativa_enlace_unico(self):
        Alternativa.objects.create(
            producto=self.producto,
            tienda=self.tienda,
            enlace="https://ebay.com/product1",
            costo=100,
        )
        with self.assertRaises(ValidationError):
            alt = Alternativa(
                producto=self.producto,
                tienda=self.tienda,
                enlace="https://ebay.com/product1",
                costo=120,
            )
            alt.full_clean()

    def test_Alternativa_costo_no_negativo(self):
        alt = Alternativa(
            producto=self.producto,
            tienda=self.tienda,
            enlace="https://ebay.com/product2",
            costo=-50,
        )
        with self.assertRaises(ValidationError):
            alt.full_clean()


class DeseoModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Hogar")
        self.producto = Producto.objects.create(nombre="Cafetera")

    def test_deseo_str(self):
        deseo = Deseo.objects.create(categoria=self.categoria, producto=self.producto)
        self.assertEqual(str(deseo), "Cafetera")
