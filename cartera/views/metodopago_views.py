from core.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from cartera.models import MetodoPago
from cartera.forms import MetodoPagoForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

class MetodoPagoListView(BaseListView):
    model = MetodoPago
    table_headers = ["Método"]
    table_fields = ["metodo"]
    update_url_name = "metodopago_update"
    delete_url_name = "metodopago_delete"
    create_url_name = "metodopago_create"
    model_name_plural = "Métodos de Pago"

class MetodoPagoCreateView(SuccessMessageMixin, BaseCreateView):
    model = MetodoPago
    form_class = MetodoPagoForm
    success_url = reverse_lazy("metodopago_list")
    success_message = "Método de Pago creado exitosamente."

class MetodoPagoUpdateView(SuccessMessageMixin, BaseUpdateView):
    model = MetodoPago
    form_class = MetodoPagoForm
    success_url = reverse_lazy("metodopago_list")
    success_message = "Método de Pago actualizado exitosamente."

class MetodoPagoDeleteView(SuccessMessageMixin, BaseDeleteView):
    model = MetodoPago
    success_url = reverse_lazy("metodopago_list")
    success_message = "Método de Pago eliminado exitosamente."
    list_url_name = "metodopago_list"

