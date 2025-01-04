from django.urls import reverse_lazy
from wish.models import Categoria
from core.views import (
    BaseListView,
    BaseDetailView,
    BaseCreateView,
    BaseUpdateView,
    BaseDeleteView,
)
from wish.forms import CategoriaForm


class CategoriaListView(BaseListView):
    model = Categoria
    table_headers = ["ID", "Nombre"]
    table_fields = ["pk", "nombre"]
    update_url_name = "wish_categoria_update"
    delete_url_name = "wish_categoria_delete"
    create_url_name = "wish_categoria_create"
    has_permission = True
    null_values = {"nombre": "Sin nombre"}


class CategoriaDetailView(BaseDetailView):
    model = Categoria
    success_url = "wish_categoria"


class CategoriaCreateView(BaseCreateView):
    model = Categoria
    form_class = CategoriaForm
    success_url = "wish_categoria"


class CategoriaUpdateView(BaseUpdateView):
    model = Categoria
    form_class = CategoriaForm
    success_url = reverse_lazy("wish_categoria")


class CategoriaDeleteView(BaseDeleteView):
    model = Categoria
    success_url = reverse_lazy("wish_categoria")
    list_url_name = "wish_categoria"
