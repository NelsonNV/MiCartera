from cartera.forms import GastoForm
from cartera.models import Gasto
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages


class GastoView(View):
    def get_list(self, request):
        gastos = Gasto.objects.all()
        context = {
            "title": "Gastos",
            "title_singular": "Gasto",
            "create_url": "gasto_create",
            "update_url": "gasto_update",
            "delete_url": "gasto_delete",
            "headers": [
                "Fecha",
                "Categoría",
                "Subcategoría",
                "Cantidad",
                "Método de Pago",
                "Descripción",
            ],
            "fields": [
                "fecha",
                "categoria",
                "subcategoria",
                "cantidad",
                "metodo_pago",
                "descripcion",
            ],
            "items": gastos,
        }
        return render(request, "list/gasto_list.html", context)

    def get_create(self, request):
        form = GastoForm()
        return render(request, "formulario/gasto_form.html", {"form": form})

    def get_update(self, request, pk):
        gasto = get_object_or_404(Gasto, pk=pk)
        form = GastoForm(instance=gasto)
        return render(request, "formulario/gasto_form.html", {"form": form})

    def get_delete(self, request, pk):
        gasto = get_object_or_404(Gasto, pk=pk)
        context = {
            "title_singular": "Gasto",
            "cancel_url": "gasto_list",
        }
        return render(request, "formulario/base_confirm_delete.html", context)

    def post_create(self, request):
        form = GastoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Gasto creado exitosamente.")
            return redirect("gasto_list")
        else:
            messages.error(request, "Hubo un error al crear el gasto.")
        return render(request, "formulario/gasto_form.html", {"form": form})

    def post_update(self, request, pk):
        gasto = get_object_or_404(Gasto, pk=pk)
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            messages.success(request, "Gasto actualizado exitosamente.")
            return redirect("gasto_list")
        else:
            messages.error(request, "Hubo un error al actualizar el gasto.")
        return render(request, "formulario/gasto_form.html", {"form": form})

    def post_delete(self, request, pk):
        gasto = get_object_or_404(Gasto, pk=pk)
        gasto.delete()
        messages.success(request, "Gasto eliminado exitosamente.")
        return redirect("gasto_list")

    def dispatch(self, request, *args, **kwargs):
        action = kwargs.pop("action", None)
        pk = kwargs.get("pk", None)

        if request.method.lower() == "get":
            if action == "create":
                return self.get_create(request)
            elif action == "update":
                return self.get_update(request, pk)
            elif action == "delete":
                return self.get_delete(request, pk)
            else:
                return self.get_list(request)

        elif request.method.lower() == "post":
            if action == "create":
                return self.post_create(request)
            elif action == "update":
                return self.post_update(request, pk)
            elif action == "delete":
                return self.post_delete(request, pk)

        return super().dispatch(request, *args, **kwargs)
