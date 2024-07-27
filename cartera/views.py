from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.http import JsonResponse
from django.views import View
from cartera.forms import CategoriaForm, SubcategoriaForm, FuenteForm, IngresoForm, GastoForm
from cartera.models import Categoria, Subcategoria, Fuente, Ingreso, Gasto
import datetime


class HomeView(View):
    def get(self, request):
        today = datetime.date.today()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = (first_day_of_month + datetime.timedelta(days=31)).replace(
            day=1
        ) - datetime.timedelta(days=1)

        ingresos = Ingreso.objects.filter(
            fecha__range=[first_day_of_month, last_day_of_month]
        )
        gastos = Gasto.objects.filter(
            fecha__range=[first_day_of_month, last_day_of_month]
        )

        total_ingresos = ingresos.aggregate(total=Sum("cantidad"))["total"] or 0
        total_gastos = gastos.aggregate(total=Sum("cantidad"))["total"] or 0
        saldo = total_ingresos - total_gastos

        gastos_por_categoria = (
            gastos.values("categoria__nombre")
            .annotate(total=Sum("cantidad"))
            .order_by("-total")
        )

        context = {
            "ingresos": ingresos,
            "gastos": gastos,
            "total_ingresos": total_ingresos,
            "total_gastos": total_gastos,
            "saldo": saldo,
            "gastos_por_categoria": gastos_por_categoria,
            "today": today,
        }
        return render(request, "home.html", context)


class GastosPorCategoriaView(View):
    def get(self, request):
        mes = request.GET.get("mes", datetime.date.today().month)
        ano = request.GET.get("ano", datetime.date.today().year)

        gastos = (
            Gasto.objects.filter(fecha__month=mes, fecha__year=ano)
            .values("categoria__nombre")
            .annotate(total=Sum("cantidad"))
            .order_by("-total")
        )

        labels = [gasto["categoria__nombre"] for gasto in gastos]
        data = [gasto["total"] for gasto in gastos]

        return JsonResponse({"labels": labels, "data": data})


class ResumenAnualView(View):
    def get(self, request):
        hoy = datetime.date.today()
        ano = hoy.year
        meses = range(1, 13)

        ingresos_por_mes = []
        gastos_por_mes = []

        for mes in meses:
            total_ingresos = (
                Ingreso.objects.filter(fecha__year=ano, fecha__month=mes).aggregate(
                    total=Sum("cantidad")
                )["total"]
                or 0
            )
            total_gastos = (
                Gasto.objects.filter(fecha__year=ano, fecha__month=mes).aggregate(
                    total=Sum("cantidad")
                )["total"]
                or 0
            )

            ingresos_por_mes.append(total_ingresos)
            gastos_por_mes.append(total_gastos)

        data = {
            "labels": [
                "Enero",
                "Febrero",
                "Marzo",
                "Abril",
                "Mayo",
                "Junio",
                "Julio",
                "Agosto",
                "Septiembre",
                "Octubre",
                "Noviembre",
                "Diciembre",
            ],
            "ingresos": ingresos_por_mes,
            "gastos": gastos_por_mes,
        }

        return JsonResponse(data)


class CategoriaListView(View):
    def get(self, request):
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


class CategoriaCreateView(View):
    def get(self, request):
        form = CategoriaForm()
        return render(request, "formulario/categoria_form.html", {"form": form})

    def post(self, request):
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada exitosamente.")
            return redirect("categoria_list")
        else:
            messages.error(request, "Hubo un error al crear la categoría.")
        return render(request, "formulario/categoria_form.html", {"form": form})


class CategoriaUpdateView(View):
    def get(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        form = CategoriaForm(instance=categoria)
        return render(request, "formulario/categoria_form.html", {"form": form})

    def post(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada exitosamente.")
            return redirect("categoria_list")
        else:
            messages.error(request, "Hubo un error al actualizar la categoría.")
        return render(request, "formulario/categoria_form.html", {"form": form})


class CategoriaDeleteView(View):
    def get(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        context = {
            "title_singular": "Categoría",
            "cancel_url": "categoria_list",
        }
        return render(request, "formulario/base_confirm_delete.html", context)

    def post(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.delete()
        messages.success(request, "Categoría eliminada exitosamente.")
        return redirect("categoria_list")


class SubcategoriaListView(View):
    def get(self, request):
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
        return render(request, "formulario/base_list.html", context)


class SubcategoriaCreateView(View):
    def get(self, request):
        form = SubcategoriaForm()
        return render(request, "formulario/subcategoria_form.html", {"form": form})

    def post(self, request):
        form = SubcategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subcategoría creada exitosamente.")
            return redirect("subcategoria_list")
        else:
            messages.error(request, "Hubo un error al crear la subcategoría.")
        return render(request, "formulario/subcategoria_form.html", {"form": form})


class SubcategoriaUpdateView(View):
    def get(self, request, pk):
        subcategoria = get_object_or_404(Subcategoria, pk=pk)
        form = SubcategoriaForm(instance=subcategoria)
        return render(request, "formulario/subcategoria_form.html", {"form": form})

    def post(self, request, pk):
        subcategoria = get_object_or_404(Subcategoria, pk=pk)
        form = SubcategoriaForm(request.POST, instance=subcategoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Subcategoría actualizada exitosamente.")
            return redirect("subcategoria_list")
        else:
            messages.error(request, "Hubo un error al actualizar la subcategoría.")
        return render(request, "formulario/subcategoria_form.html", {"form": form})


class SubcategoriaDeleteView(View):
    def get(self, request, pk):
        subcategoria = get_object_or_404(Subcategoria, pk=pk)
        context = {
            "title_singular": "Subcategoría",
            "cancel_url": "subcategoria_list",
        }
        return render(request, "formulario/base_confirm_delete.html", context)

    def post(self, request, pk):
        subcategoria = get_object_or_404(Subcategoria, pk=pk)
        subcategoria.delete()
        messages.success(request, "Subcategoría eliminada exitosamente.")
        return redirect("subcategoria_list")


class FuenteListView(View):
    def get(self, request):
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
        return render(request, "formulario/base_list.html", context)


class FuenteCreateView(View):
    def get(self, request):
        form = FuenteForm()
        return render(request, "formulario/fuente_form.html", {"form": form})

    def post(self, request):
        form = FuenteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fuente creada exitosamente.")
            return redirect("fuente_list")
        else:
            messages.error(request, "Hubo un error al crear la fuente.")
        return render(request, "formulario/fuente_form.html", {"form": form})


class FuenteUpdateView(View):
    def get(self, request, pk):
        fuente = get_object_or_404(Fuente, pk=pk)
        form = FuenteForm(instance=fuente)
        return render(request, "formulario/fuente_form.html", {"form": form})

    def post(self, request, pk):
        fuente = get_object_or_404(Fuente, pk=pk)
        form = FuenteForm(request.POST, instance=fuente)
        if form.is_valid():
            form.save()
            messages.success(request, "Fuente actualizada exitosamente.")
            return redirect("fuente_list")
        else:
            messages.error(request, "Hubo un error al actualizar la fuente.")
        return render(request, "formulario/fuente_form.html", {"form": form})


class FuenteDeleteView(View):
    def get(self, request, pk):
        fuente = get_object_or_404(Fuente, pk=pk)
        context = {
            "title_singular": "Fuente",
            "cancel_url": "fuente_list",
        }
        return render(request, "formulario/base_confirm_delete.html", context)

    def post(self, request, pk):
        fuente = get_object_or_404(Fuente, pk=pk)
        fuente.delete()
        messages.success(request, "Fuente eliminada exitosamente.")
        return redirect("fuente_list")


class IngresoListView(View):
    def get(self, request):
        ingresos = Ingreso.objects.all()
        context = {
            "title": "Ingresos",
            "title_singular": "Ingreso",
            "create_url": "ingreso_create",
            "update_url": "ingreso_update",
            "delete_url": "ingreso_delete",
            "headers": ["Fecha", "Fuente", "Categoría", "Cantidad", "Descripción"],
            "fields": ["fecha", "fuente", "categoria", "cantidad", "descripcion"],
            "items": ingresos,
        }
        return render(request, "formulario/base_list.html", context)


class IngresoCreateView(View):
    def get(self, request):
        form = IngresoForm()
        return render(request, "formulario/ingreso_form.html", {"form": form})

    def post(self, request):
        form = IngresoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ingreso creado exitosamente.")
            return redirect("ingreso_list")
        else:
            messages.error(request, "Hubo un error al crear el ingreso.")
        return render(request, "formulario/ingreso_form.html", {"form": form})


class IngresoUpdateView(View):
    def get(self, request, pk):
        ingreso = get_object_or_404(Ingreso, pk=pk)
        form = IngresoForm(instance=ingreso)
        return render(request, "formulario/ingreso_form.html", {"form": form})

    def post(self, request, pk):
        ingreso = get_object_or_404(Ingreso, pk=pk)
        form = IngresoForm(request.POST, instance=ingreso)
        if form.is_valid():
            form.save()
            messages.success(request, "Ingreso actualizado exitosamente.")
            return redirect("ingreso_list")
        else:
            messages.error(request, "Hubo un error al actualizar el ingreso.")
        return render(request, "formulario/ingreso_form.html", {"form": form})


class IngresoDeleteView(View):
    def get(self, request, pk):
        ingreso = get_object_or_404(Ingreso, pk=pk)
        context = {
            "title_singular": "Ingreso",
            "cancel_url": "ingreso_list",
        }
        return render(request, "formulario/base_confirm_delete.html", context)

    def post(self, request, pk):
        ingreso = get_object_or_404(Ingreso, pk=pk)
        ingreso.delete()
        messages.success(request, "Ingreso eliminado exitosamente.")
        return redirect("ingreso_list")


# Vistas para Gasto
class GastoListView(View):
    def get(self, request):
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
        return render(request, "formulario/base_list.html", context)


class GastoCreateView(View):
    def get(self, request):
        form = GastoForm()
        return render(request, "formulario/gasto_form.html", {"form": form})

    def post(self, request):
        form = GastoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Gasto creado exitosamente.")
            return redirect("gasto_list")
        else:
            messages.error(request, "Hubo un error al crear el gasto.")
        return render(request, "formulario/gasto_form.html", {"form": form})


class GastoUpdateView(View):
    def get(self, request, pk):
        gasto = get_object_or_404(Gasto, pk=pk)
        form = GastoForm(instance=gasto)
        return render(request, "formulario/gasto_form.html", {"form": form})

    def post(self, request, pk):
        gasto = get_object_or_404(Gasto, pk=pk)
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            messages.success(request, "Gasto actualizado exitosamente.")
            return redirect("gasto_list")
        else:
            messages.error(request, "Hubo un error al actualizar el gasto.")
        return render(request, "formulario/gasto_form.html", {"form": form})


class GastoDeleteView(View):
    def get(self, request, pk):
        gasto = get_object_or_404(Gasto, pk=pk)
        context = {
            "title_singular": "Gasto",
            "cancel_url": "gasto_list",
        }
        return render(request, "formulario/base_confirm_delete.html", context)

    def post(self, request, pk):
        gasto = get_object_or_404(Gasto, pk=pk)
        gasto.delete()
        messages.success(request, "Gasto eliminado exitosamente.")
        return redirect("gasto_list")
