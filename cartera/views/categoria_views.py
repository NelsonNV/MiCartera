from core.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from cartera.models import Categoria
from cartera.forms import CategoriaForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

class CategoriaListView(BaseListView):
    model = Categoria
    table_headers = ["Nombre"]
    table_fields = ["nombre"]
    update_url_name = "categoria_update"
    delete_url_name = "categoria_delete"
    create_url_name = "categoria_create"
    model_name_plural = "Categorías"

class CategoriaCreateView(SuccessMessageMixin, BaseCreateView):
    model = Categoria
    form_class = CategoriaForm
    success_url = reverse_lazy("categoria_list")
    success_message = "Categoría creada exitosamente."

class CategoriaUpdateView(SuccessMessageMixin, BaseUpdateView):
    model = Categoria
    form_class = CategoriaForm
    success_url = reverse_lazy("categoria_list")
    success_message = "Categoría actualizada exitosamente."

class CategoriaDeleteView(SuccessMessageMixin, BaseDeleteView):
    model = Categoria
    success_url = reverse_lazy("categoria_list")
    success_message = "Categoría eliminada exitosamente."
    list_url_name = "categoria_list"
