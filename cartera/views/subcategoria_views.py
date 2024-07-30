from cartera.forms import SubcategoriaForm
from cartera.models import Subcategoria
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages


class SubcategoriaView(View):
    def get_list(self, request):
        subcategorias = Subcategoria.objects.all()
        context = {
            "title": "Subcategorías",
            "title_singular": "Subcategoría",
            "create_url": "subcategoria_create",
            "update_url": "subcategoria_update",
            "delete_url": "subcategoria_delete",
            "headers": ["Nombre", "Categoría"],
            "fields": ["nombre", "categoria"],
            "items": subcategorias,
        }
        return render(request, "list/subcategoria_list.html", context)

    def get_create(self, request):
        form = SubcategoriaForm()
        return render(request, "formulario/subcategoria_form.html", {"form": form})

    def get_update(self, request, pk):
        subcategoria = get_object_or_404(Subcategoria, pk=pk)
        form = SubcategoriaForm(instance=subcategoria)
        return render(request, "formulario/subcategoria_form.html", {"form": form})

    def get_delete(self, request, pk):
        subcategoria = get_object_or_404(Subcategoria, pk=pk)
        context = {
            "title_singular": "Subcategoría",
            "cancel_url": "subcategoria_list",
        }
        return render(request, "formulario/base_confirm_delete.html", context)

    def post_create(self, request):
        form = SubcategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subcategoría creada exitosamente.")
            return redirect("subcategoria_list")
        else:
            messages.error(request, "Hubo un error al crear la subcategoría.")
        return render(request, "formulario/subcategoria_form.html", {"form": form})

    def post_update(self, request, pk):
        subcategoria = get_object_or_404(Subcategoria, pk=pk)
        form = SubcategoriaForm(request.POST, instance=subcategoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Subcategoría actualizada exitosamente.")
            return redirect("subcategoria_list")
        else:
            messages.error(request, "Hubo un error al actualizar la subcategoría.")
        return render(request, "formulario/subcategoria_form.html", {"form": form})

    def post_delete(self, request, pk):
        subcategoria = get_object_or_404(Subcategoria, pk=pk)
        subcategoria.delete()
        messages.success(request, "Subcategoría eliminada exitosamente.")
        return redirect("subcategoria_list")

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
