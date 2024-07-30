from cartera.forms import FuenteForm
from cartera.models import Fuente
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages


class FuenteView(View):
    def get_list(self, request):
        fuentes = Fuente.objects.all()
        context = {
            "title": "Fuentes",
            "title_singular": "Fuente",
            "create_url": "fuente_create",
            "update_url": "fuente_update",
            "delete_url": "fuente_delete",
            "headers": ["Nombre"],
            "fields": ["nombre"],
            "items": fuentes,
        }
        return render(request, "list/fuente_list.html", context)

    def get_create(self, request):
        form = FuenteForm()
        return render(request, "formulario/fuente_form.html", {"form": form})

    def get_update(self, request, pk):
        fuente = get_object_or_404(Fuente, pk=pk)
        form = FuenteForm(instance=fuente)
        return render(request, "formulario/fuente_form.html", {"form": form})

    def get_delete(self, request, pk):
        fuente = get_object_or_404(Fuente, pk=pk)
        context = {
            "title_singular": "Fuente",
            "cancel_url": "fuente_list",
        }
        return render(request, "formulario/base_confirm_delete.html", context)

    def post_create(self, request):
        form = FuenteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fuente creada exitosamente.")
            return redirect("fuente_list")
        else:
            messages.error(request, "Hubo un error al crear la fuente.")
        return render(request, "formulario/fuente_form.html", {"form": form})

    def post_update(self, request, pk):
        fuente = get_object_or_404(Fuente, pk=pk)
        form = FuenteForm(request.POST, instance=fuente)
        if form.is_valid():
            form.save()
            messages.success(request, "Fuente actualizada exitosamente.")
            return redirect("fuente_list")
        else:
            messages.error(request, "Hubo un error al actualizar la fuente.")
        return render(request, "formulario/fuente_form.html", {"form": form})

    def post_delete(self, request, pk):
        fuente = get_object_or_404(Fuente, pk=pk)
        fuente.delete()
        messages.success(request, "Fuente eliminada exitosamente.")
        return redirect("fuente_list")

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
