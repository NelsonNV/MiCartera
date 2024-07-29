from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse
from django.views import View
from cartera.models import Ingreso, Gasto, Categoria
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
