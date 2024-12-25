from wish.views.base.base_views import (
    BaseCreateView,
    BaseDeleteView,
    BaseListView,
    BaseUpdateView,
)
from wish.models import Deseo
from wish.forms import DeseoForm
from django.urls import reverse_lazy


class DeseoListView(BaseListView):
    model = Deseo
    table_headers = ["Categoria", "Producto"]
    table_fields = ["categoria", "producto"]
    update_url_name = "wish_deseo_update"
    delete_url_name = "wish_deseo_delete"
    create_url_name = "wish_deseo_create"
    model_name_plural = "Deseos"


class DeseoCreateView(BaseCreateView):
    success_url = reverse_lazy("wish_deseo")
    model = Deseo
    form_class = DeseoForm
    success_url = reverse_lazy("wish_deseo")


class DeseoUpdateView(BaseUpdateView):
    success_url = reverse_lazy("wish_deseo")
    model = Deseo
    fields = ["categoria", "producto"]
    success_url = reverse_lazy("wish_deseo")


class DeseoDeleteView(BaseDeleteView):
    model = Deseo
    success_url = reverse_lazy("wish_deseo")
    list_url_name = "wish_deseo"
