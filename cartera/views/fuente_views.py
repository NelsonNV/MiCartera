from core.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from cartera.models import Fuente
from cartera.forms import FuenteForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

class FuenteListView(BaseListView):
    model = Fuente
    table_headers = ["Nombre"]
    table_fields = ["nombre"]
    update_url_name = "fuente_update"
    delete_url_name = "fuente_delete"
    create_url_name = "fuente_create"
    model_name_plural = "Fuentes"

class FuenteCreateView(SuccessMessageMixin, BaseCreateView):
    model = Fuente
    form_class = FuenteForm
    success_url = reverse_lazy("fuente_list")
    success_message = "Fuente creada exitosamente."

class FuenteUpdateView(SuccessMessageMixin, BaseUpdateView):
    model = Fuente
    form_class = FuenteForm
    success_url = reverse_lazy("fuente_list")
    success_message = "Fuente actualizada exitosamente."

class FuenteDeleteView(SuccessMessageMixin, BaseDeleteView):
    model = Fuente
    success_url = reverse_lazy("fuente_list")
    success_message = "Fuente eliminada exitosamente."
    list_url_name = "fuente_list"
