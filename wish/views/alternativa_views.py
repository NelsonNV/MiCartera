from wish.models import Alternativa
from wish.forms import AlternativaForm
from django.urls import reverse_lazy
from wish.views.base.base_views import (
    BaseListView,
    BaseCreateView,
    BaseUpdateView,
    BaseDeleteView,
)


class AlternativaListView(BaseListView):
    model = Alternativa
    table_headers = ["Producto", "Tienda", "Enlace", "Imagen", "Costo"]
    table_fields = ["producto", "tienda", "enlace", "imagen", "costo"]
    update_url_name = "wish_alternativa_update"
    delete_url_name = "wish_alternativa_delete"
    create_url_name = "wish_alternativa_create"
    model_name_plural = "Alternativas"
    image_fields = ["imagen"]


class AlternativaCreateView(BaseCreateView):
    model = Alternativa
    form_class = AlternativaForm
    success_url = reverse_lazy("wish_alternativa")


class AlternativaUpdateView(BaseUpdateView):
    model = Alternativa
    fields = ["producto", "tienda", "enlace", "imagen", "costo"]
    success_url = reverse_lazy("wish_alternativa")


class AlternativaDeleteView(BaseDeleteView):
    model = Alternativa
    success_url = reverse_lazy("wish_alternativa")
    list_url_name = "wish_alternativa"
