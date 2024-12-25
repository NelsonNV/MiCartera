from wish.views.base.base_views import (
    BaseListView,
    BaseCreateView,
    BaseUpdateView,
    BaseDeleteView,
)
from wish.models import Producto
from wish.forms import ProductoForm
from django.urls import reverse_lazy


class ProductoListView(BaseListView):
    model = Producto
    table_headers = ["Nombre", "Imagen"]
    table_fields = ["nombre", "imagen"]
    update_url_name = "wish_producto_updates"
    delete_url_name = "wish_producto_delete"
    create_url_name = "wish_producto_create"
    model_name_plural = "Productos"
    image_fields = ["imagen"]


class ProductoCreateView(BaseCreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy("wish_producto")


class ProductoUpdateView(BaseUpdateView):
    model = Producto
    fields = ["nombre", "imagen"]
    success_url = reverse_lazy("wish_producto")


class ProductoDeleteView(BaseDeleteView):
    model = Producto
    success_url = reverse_lazy("wish_producto")
    list_url_name = "wish_producto"
