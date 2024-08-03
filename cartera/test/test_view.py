from django.test import TestCase, Client
from django.urls import reverse
from cartera.models import Categoria, Subcategoria, Fuente, Ingreso, Gasto, MetodoPago
from django.contrib.auth.models import User
from django.http import Http404


class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

        self.client = Client()
        self.client.login(username="testuser", password="12345")

        self.categoria = Categoria.objects.create(nombre="Categoría Test")
        self.subcategoria = Subcategoria.objects.create(
            nombre="Subcategoría Test", categoria=self.categoria
        )
        self.fuente = Fuente.objects.create(nombre="Fuente Test")
        self.metodo_pago = MetodoPago.objects.create(metodo="Efectivo")

        self.ingreso = Ingreso.objects.create(
            fecha="2024-07-27",
            fuente=self.fuente,
            cantidad=100.00,
            descripcion="Ingreso Test",
        )
        self.gasto = Gasto.objects.create(
            fecha="2024-07-27",
            categoria=self.categoria,
            subcategoria=self.subcategoria,
            cantidad=50.00,
            metodo_pago=self.metodo_pago,
            descripcion="Gasto Test",
        )

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_gastos_por_categoria_view(self):
        response = self.client.get(reverse("gastos_por_categoria"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_resumen_anual_view(self):
        response = self.client.get(reverse("resumen_anual"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_categoria_list_view(self):
        response = self.client.get(reverse("categoria_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "formulario/base_list.html")

    def test_categoria_create_view_get(self):
        response = self.client.get(reverse("categoria_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "formulario/categoria_form.html")

    def test_categoria_create_view_post(self):
        response = self.client.post(
            reverse("categoria_create"), {"nombre": "Nueva Categoría"}
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirección después de crear la categoría
        self.assertTrue(Categoria.objects.filter(nombre="Nueva Categoría").exists())

    def test_categoria_update_view_get(self):
        response = self.client.get(
            reverse("categoria_update", args=[self.categoria.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "formulario/categoria_form.html")

    def test_categoria_update_view_post(self):
        response = self.client.post(
            reverse("categoria_update", args=[self.categoria.id]),
            {"nombre": "Categoría Actualizada"},
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirección después de actualizar la categoría
        self.categoria.refresh_from_db()
        self.assertEqual(self.categoria.nombre, "Categoría Actualizada")

    def test_categoria_delete_view_get(self):
        response = self.client.get(
            reverse("categoria_delete", args=[self.categoria.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "formulario/base_confirm_delete.html")

    def test_categoria_delete_view_post(self):
        response = self.client.post(
            reverse("categoria_delete", args=[self.categoria.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Categoria.objects.filter(id=self.categoria.id).exists())

    def test_categoria_update_view_404(self):
        response = self.client.get(reverse("categoria_update", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_categoria_delete_view_404(self):
        response = self.client.get(reverse("categoria_delete", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_subcategoria_list_view(self):
        response = self.client.get(reverse("subcategoria_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "formulario/base_list.html")

    def test_fuente_list_view(self):
        response = self.client.get(reverse("fuente_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "formulario/base_list.html")

    def test_ingreso_list_view(self):
        response = self.client.get(reverse("ingreso_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "formulario/base_list.html")

    def test_gasto_list_view(self):
        response = self.client.get(reverse("gasto_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "formulario/base_list.html")

    def test_subcategoria_create_view_post(self):
        response = self.client.post(
            reverse("subcategoria_create"),
            {"nombre": "Nueva Subcategoría", "categoria": self.categoria.id},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Subcategoria.objects.filter(nombre="Nueva Subcategoría").exists()
        )

    def test_subcategoria_update_view_post(self):
        response = self.client.post(
            reverse("subcategoria_update", args=[self.subcategoria.id]),
            {"nombre": "Subcategoría Actualizada", "categoria": self.categoria.id},
        )
        self.assertEqual(response.status_code, 302)
        self.subcategoria.refresh_from_db()
        self.assertEqual(self.subcategoria.nombre, "Subcategoría Actualizada")

    def test_subcategoria_delete_view_post(self):
        response = self.client.post(
            reverse("subcategoria_delete", args=[self.subcategoria.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Subcategoria.objects.filter(id=self.subcategoria.id).exists())

    def test_subcategoria_update_view_404(self):
        response = self.client.get(reverse("subcategoria_update", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_subcategoria_delete_view_404(self):
        response = self.client.get(reverse("subcategoria_delete", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_fuente_create_view_post(self):
        response = self.client.post(
            reverse("fuente_create"), {"nombre": "Nueva Fuente"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Fuente.objects.filter(nombre="Nueva Fuente").exists())

    def test_fuente_update_view_post(self):
        response = self.client.post(
            reverse("fuente_update", args=[self.fuente.id]),
            {"nombre": "Fuente Actualizada"},
        )
        self.assertEqual(response.status_code, 302)
        self.fuente.refresh_from_db()
        self.assertEqual(self.fuente.nombre, "Fuente Actualizada")

    def test_fuente_delete_view_post(self):
        response = self.client.post(reverse("fuente_delete", args=[self.fuente.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Fuente.objects.filter(id=self.fuente.id).exists())

    def test_fuente_update_view_404(self):
        response = self.client.get(reverse("fuente_update", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_fuente_delete_view_404(self):
        response = self.client.get(reverse("fuente_delete", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_ingreso_create_view_post(self):
        response = self.client.post(
            reverse("ingreso_create"),
            {
                "fecha": "2024-07-27",
                "fuente": self.fuente.id,
                "cantidad": 200.00,
                "descripcion": "Nuevo Ingreso",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingreso.objects.filter(descripcion="Nuevo Ingreso").exists())

    def test_ingreso_update_view_post(self):
        response = self.client.post(
            reverse("ingreso_update", args=[self.ingreso.id]),
            {
                "fecha": "2024-07-27",
                "fuente": self.fuente.id,
                "cantidad": 300.00,
                "descripcion": "Ingreso Actualizado",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.ingreso.refresh_from_db()
        self.assertEqual(self.ingreso.descripcion, "Ingreso Actualizado")

    def test_ingreso_delete_view_post(self):
        response = self.client.post(reverse("ingreso_delete", args=[self.ingreso.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ingreso.objects.filter(id=self.ingreso.id).exists())

    def test_ingreso_update_view_404(self):
        response = self.client.get(reverse("ingreso_update", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_ingreso_delete_view_404(self):
        response = self.client.get(reverse("ingreso_delete", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_gasto_create_view_post(self):
        response = self.client.post(
            reverse("gasto_create"),
            {
                "fecha": "2024-07-27",
                "categoria": self.categoria.id,
                "subcategoria": self.subcategoria.id,
                "cantidad": 100.00,
                "metodo_pago": self.metodo_pago.id,
                "descripcion": "Nuevo Gasto",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Gasto.objects.filter(descripcion="Nuevo Gasto").exists())

    def test_gasto_update_view_post(self):
        response = self.client.post(
            reverse("gasto_update", args=[self.gasto.id]),
            {
                "fecha": "2024-07-27",
                "categoria": self.categoria.id,
                "subcategoria": self.subcategoria.id,
                "cantidad": 150.00,
                "metodo_pago": self.metodo_pago.id,
                "descripcion": "Gasto Actualizado",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.gasto.refresh_from_db()
        self.assertEqual(self.gasto.descripcion, "Gasto Actualizado")

    def test_gasto_delete_view_post(self):
        response = self.client.post(reverse("gasto_delete", args=[self.gasto.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Gasto.objects.filter(id=self.gasto.id).exists())

    def test_gasto_update_view_404(self):
        response = self.client.get(reverse("gasto_update", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_gasto_delete_view_404(self):
        response = self.client.get(reverse("gasto_delete", args=[9999]))
        self.assertEqual(response.status_code, 404)
