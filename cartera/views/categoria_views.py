from cartera.forms import CategoriaForm
from cartera.models import Categoria
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages


class CategoriaView(View):
    def get_list(self, request):
        categorias = Categoria.objects.all()
        context = {
            "title": "Categorías",
            "title_singular": "Categoría",
            "create_url": "categoria_create",
            "update_url": "categoria_update",
            "delete_url": "categoria_delete",
            "headers": ["Nombre"],
            "fields": ["nombre"],
            "items": categorias,
        }
        return render(request, "formulario/base_list.html", context)

    def get_create(self, request):
        form = CategoriaForm()
        return render(request, "formulario/categoria_form.html", {"form": form})

    def get_update(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        form = CategoriaForm(instance=categoria)
        return render(request, "formulario/categoria_form.html", {"form": form})

    def get_delete(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        context = {
            "title_singular": "Categoría",
            "cancel_url": "categoria_list",
        }
        return render(request, "formulario/base_confirm_delete.html", context)

    def post_create(self, request):
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada exitosamente.")
            return redirect("categoria_list")
        else:
            messages.error(request, "Hubo un error al crear la categoría.")
        return render(request, "formulario/categoria_form.html", {"form": form})

    def post_update(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada exitosamente.")
            return redirect("categoria_list")
        else:
            messages.error(request, "Hubo un error al actualizar la categoría.")
        return render(request, "formulario/categoria_form.html", {"form": form})

    def post_delete(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.delete()
        messages.success(request, "Categoría eliminada exitosamente.")
        return redirect("categoria_list")

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
