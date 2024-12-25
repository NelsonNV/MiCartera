from django.urls import reverse_lazy
from wish.models import Tiendas
from wish.views.base.base_views import (
    BaseListView,
    BaseDetailView,
    BaseCreateView,
    BaseUpdateView,
    BaseDeleteView,
)


class TiendasListView(BaseListView):
    model = Tiendas
    model_name_plural = "Tiendas"
    table_headers = ["ID", "Nombre", "Enlace", "Logo"]
    table_fields = ["id", "nombre", "enlace", "logo"]
    update_url_name = "wish_tiendas_update"
    delete_url_name = "wish_tiendas_delete"
    create_url_name = "wish_tiendas_create"
    null_values = {"logo": "Sin logo"}


class TiendasDetailView(BaseDetailView):
    model = Tiendas


class TiendasCreateView(BaseCreateView):
    model = Tiendas
    fields = ["nombre", "enlace", "logo"]
    success_url = reverse_lazy("wish_tiendas_list")


class TiendasUpdateView(BaseUpdateView):
    model = Tiendas
    fields = ["nombre", "enlace", "logo"]
    success_url = reverse_lazy("wish_tiendas_list")


class TiendasDeleteView(BaseDeleteView):
    model = Tiendas
    success_url = reverse_lazy("wish_tiendas_list")
    list_url_name = "wish_tiendas_list"
