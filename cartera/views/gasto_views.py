from core.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from cartera.models import Gasto
from cartera.forms import GastoForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

class GastoListView(BaseListView):
    model = Gasto
    table_headers = ["Fecha", "Categoría", "Subcategoría", "Cantidad", "Método de Pago", "Descripción"]
    table_fields = ["fecha", "categoria", "subcategoria", "cantidad", "metodo_pago", "descripcion"]
    update_url_name = "gasto_update"
    delete_url_name = "gasto_delete"
    create_url_name = "gasto_create"
    model_name_plural = "Gastos"


class GastoCreateView(SuccessMessageMixin, BaseCreateView):
    model = Gasto
    form_class = GastoForm
    success_url = reverse_lazy("gasto_list")
    success_message = "Gasto creado exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_gastos'] = True
        return context

class GastoUpdateView(SuccessMessageMixin, BaseUpdateView):
    model = Gasto
    form_class = GastoForm
    success_url = reverse_lazy("gasto_list")
    success_message = "Gasto actualizado exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_gastos'] = True
        return context


class GastoDeleteView(SuccessMessageMixin, BaseDeleteView):
    model = Gasto
    success_url = reverse_lazy("gasto_list")
    success_message = "Gasto eliminado exitosamente."
    list_url_name = "gasto_list"
