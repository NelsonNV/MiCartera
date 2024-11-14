from cartera.forms import IngresoForm
from cartera.models import Ingreso
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages


class IngresoView(View):
    def get_list(self, request):
        ingresos = Ingreso.objects.all().order_by("-fecha", "id").values()
        context = {
            "title": "Ingresos",
            "title_singular": "Ingreso",
            "create_url": "ingreso_create",
            "update_url": "ingreso_update",
            "delete_url": "ingreso_delete",
            "headers": ["Fecha", "Fuente", "Cantidad", "Descripción"],
            "fields": ["fecha", "fuente", "cantidad", "descripcion"],
            "items": ingresos,
        }
        return render(request, "list/ingreso_list.html", context)

    def get_create(self, request):
        form = IngresoForm()
        return render(request, "formulario/ingreso_form.html", {"form": form})

    def get_update(self, request, pk):
        ingreso = get_object_or_404(Ingreso, pk=pk)
        form = IngresoForm(instance=ingreso)
        return render(request, "formulario/ingreso_form.html", {"form": form})

    def get_delete(self, request, pk):
        ingreso = get_object_or_404(Ingreso, pk=pk)
        context = {
            "title_singular": "Ingreso",
            "cancel_url": "ingreso_list",
        }
        return render(request, "formulario/base_confirm_delete.html", context)

    def post_create(self, request):
        form = IngresoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ingreso creado exitosamente.")
            return redirect("ingreso_list")
        else:
            messages.error(request, "Hubo un error al crear el ingreso.")
        return render(request, "formulario/ingreso_form.html", {"form": form})

    def post_update(self, request, pk):
        ingreso = get_object_or_404(Ingreso, pk=pk)
        form = IngresoForm(request.POST, instance=ingreso)
        if form.is_valid():
            form.save()
            messages.success(request, "Ingreso actualizado exitosamente.")
            return redirect("ingreso_list")
        else:
            messages.error(request, "Hubo un error al actualizar el ingreso.")
        return render(request, "formulario/ingreso_form.html", {"form": form})

    def post_delete(self, request, pk):
        ingreso = get_object_or_404(Ingreso, pk=pk)
        ingreso.delete()
        messages.success(request, "Ingreso eliminado exitosamente.")
        return redirect("ingreso_list")

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
