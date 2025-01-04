from core.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from cartera.models import Subcategoria
from cartera.forms import SubcategoriaForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.views import View

class SubcategoriaListView(BaseListView):
    model = Subcategoria
    table_headers = ["Nombre", "Categoría"]
    table_fields = ["nombre", "categoria"]
    update_url_name = "subcategoria_update"
    delete_url_name = "subcategoria_delete"
    create_url_name = "subcategoria_create"
    model_name_plural = "Subcategorías"

class SubcategoriaCreateView(SuccessMessageMixin, BaseCreateView):
    model = Subcategoria
    form_class = SubcategoriaForm
    success_url = reverse_lazy("subcategoria_list")
    success_message = "Subcategoría creada exitosamente."

class SubcategoriaUpdateView(SuccessMessageMixin, BaseUpdateView):
    model = Subcategoria
    form_class = SubcategoriaForm
    success_url = reverse_lazy("subcategoria_list")
    success_message = "Subcategoría actualizada exitosamente."

class SubcategoriaDeleteView(SuccessMessageMixin, BaseDeleteView):
    model = Subcategoria
    success_url = reverse_lazy("subcategoria_list")
    success_message = "Subcategoría eliminada exitosamente."
    list_url_name = "subcategoria_list"

class LoadSubcategoriasView(View):
    def get(self, request, *args, **kwargs):
        categoria_id = request.GET.get("categoria_id")
        subcategorias = Subcategoria.objects.filter(categoria_id=categoria_id).all()
        return JsonResponse(list(subcategorias.values("id", "nombre")), safe=False)
