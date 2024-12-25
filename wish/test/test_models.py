from django.test import TestCase
from django.core.exceptions import ValidationError
from wish.models import Categoria, Tiendas, Producto, Alternativa, Deseo
from django.core.files.base import ContentFile


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
        self.image_file = ContentFile(b"fake_image_data", name="test_image.png")

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

    def test_producto_con_varias_alternativas(self):
        producto = Producto.objects.create(nombre="Laptop", imagen=self.image_file)

        Tiendas.objects.all().delete()
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
        # Cambiar los nombres de los productos para evitar conflicto de UNIQUE
        producto1 = Producto.objects.create(nombre="Laptop", imagen=self.image_file)
        producto2 = Producto.objects.create(
            nombre="Smartphone X", imagen=self.image_file
        )

        # Crear tiendas con nombres únicos
        tienda1 = Tiendas.objects.create(
            nombre="Amazon Store", enlace="https://www.amazon.com"
        )
        tienda2 = Tiendas.objects.create(
            nombre="eBay Store", enlace="https://www.ebay.com"
        )
        tienda3 = Tiendas.objects.create(
            nombre="BestBuy Store", enlace="https://www.bestbuy.com"
        )
        tienda4 = Tiendas.objects.create(
            nombre="Walmart Store", enlace="https://www.walmart.com"
        )

        # Crear alternativas para el producto 1
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

        # Crear alternativas para el producto 2
        Alternativa.objects.create(
            producto=producto2,
            tienda=tienda3,
            enlace="https://www.bestbuy.com/smartphone-x",
            imagen=self.image_file,
            costo=800.00,
        )
        Alternativa.objects.create(
            producto=producto2,
            tienda=tienda4,
            enlace="https://www.walmart.com/smartphone-x",
            imagen=self.image_file,
            costo=850.00,
        )

        # Verificar que ambos productos tienen sus alternativas correctamente
        self.assertEqual(Alternativa.objects.filter(producto=producto1).count(), 2)
        self.assertEqual(Alternativa.objects.filter(producto=producto2).count(), 2)


class DeseoModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Hogar")
        self.producto = Producto.objects.create(nombre="Cafetera")

    def test_deseo_str(self):
        deseo = Deseo.objects.create(categoria=self.categoria, producto=self.producto)
        self.assertEqual(str(deseo), "Cafetera")
