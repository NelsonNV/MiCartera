from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from cartera.forms import MetodoPagoForm
from cartera.models import MetodoPago


class MetodoPagoView(View):
    def get_list(self, request):
        metodos = MetodoPago.objects.all()
        context = {
            "title": "Métodos de Pago",
            "title_singular": "Método de Pago",
            "create_url": "metodopago_create",
            "update_url": "metodopago_update",
            "delete_url": "metodopago_delete",
            "headers": ["Método"],
            "fields": ["metodo"],
            "items": metodos,
        }
        return render(request, "list/metodopago_list.html", context)

    def get_create(self, request):
        form = MetodoPagoForm()
        return render(request, "formulario/metodopago_form.html", {"form": form})

    def get_update(self, request, pk):
        metodo = get_object_or_404(MetodoPago, pk=pk)
        form = MetodoPagoForm(instance=metodo)
        return render(request, "formulario/metodopago_form.html", {"form": form})

    def get_delete(self, request, pk):
        metodo = get_object_or_404(MetodoPago, pk=pk)
        context = {
            "title_singular": "Método de Pago",
            "cancel_url": "metodopago_list",
        }
        return render(request, "formulario/base_confirm_delete.html", context)

    def post_create(self, request):
        form = MetodoPagoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Método de Pago creado exitosamente.")
            return redirect("metodopago_list")
        else:
            messages.error(request, "Hubo un error al crear el Método de Pago.")
        return render(request, "formulario/metodopago_form.html", {"form": form})

    def post_update(self, request, pk):
        metodo = get_object_or_404(MetodoPago, pk=pk)
        form = MetodoPagoForm(request.POST, instance=metodo)
        if form.is_valid():
            form.save()
            messages.success(request, "Método de Pago actualizado exitosamente.")
            return redirect("metodopago_list")
        else:
            messages.error(request, "Hubo un error al actualizar el Método de Pago.")
        return render(request, "formulario/metodopago_form.html", {"form": form})

    def post_delete(self, request, pk):
        metodo = get_object_or_404(MetodoPago, pk=pk)
        metodo.delete()
        messages.success(request, "Método de Pago eliminado exitosamente.")
        return redirect("metodopago_list")

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

