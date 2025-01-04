from core.views import (
    BaseListView,
    BaseCreateView,
    BaseUpdateView,
    BaseDeleteView,
)
from cartera.forms import IngresoForm
from cartera.models import Ingreso
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


# Listado de ingresos
class IngresoListView(BaseListView):
    model = Ingreso
    table_headers = ["Fecha", "Fuente", "Cantidad", "Descripción", "Tarjeta"]
    table_fields = ["fecha", "fuente", "cantidad", "descripcion", "tarjeta"]
    update_url_name = "ingreso_update"
    delete_url_name = "ingreso_delete"
    create_url_name = "ingreso_create"
    model_name_plural = "Ingresos"


# Creación de ingreso
class IngresoCreateView(SuccessMessageMixin, BaseCreateView):
    model = Ingreso
    form_class = IngresoForm
    success_url = reverse_lazy("ingreso_list")
    success_message = "Ingreso creado exitosamente."


# Actualización de ingreso
class IngresoUpdateView(SuccessMessageMixin, BaseUpdateView):
    model = Ingreso
    form_class = IngresoForm
    success_url = reverse_lazy("ingreso_list")
    success_message = "Ingreso actualizado exitosamente."


# Eliminación de ingreso
class IngresoDeleteView(SuccessMessageMixin, BaseDeleteView):
    model = Ingreso
    success_url = reverse_lazy("ingreso_list")
    success_message = "Ingreso eliminado exitosamente."
    list_url_name = "ingreso_list"
