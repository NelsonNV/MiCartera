from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse
from django.views import View
from cartera.models import Ingreso, Gasto, Categoria, MetodoPago
import datetime


class HomeView(View):
    def get(self, request):
        today = datetime.date.today()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = (first_day_of_month + datetime.timedelta(days=31)).replace(
            day=1
        ) - datetime.timedelta(days=1)

        # Calcular ingresos y gastos del mes
        ingresos = Ingreso.objects.filter(
            fecha__range=[first_day_of_month, last_day_of_month]
        )
        gastos = Gasto.objects.filter(
            fecha__range=[first_day_of_month, last_day_of_month]
        )

        total_ingresos_mes = ingresos.aggregate(total=Sum("cantidad"))["total"] or 0
        total_gastos_mes = gastos.aggregate(total=Sum("cantidad"))["total"] or 0
        saldo_mes = total_ingresos_mes - total_gastos_mes

        # Calcular ingresos y gastos totales
        total_ingresos = Ingreso.objects.aggregate(total=Sum("cantidad"))["total"] or 0
        total_gastos = Gasto.objects.aggregate(total=Sum("cantidad"))["total"] or 0
        saldo = total_ingresos - total_gastos

        # Calcular saldo por tarjeta
        saldo_por_tarjeta = []
        tarjetas = MetodoPago.objects.all()
        for tarjeta in tarjetas:
            ingresos_tarjeta = (
                Ingreso.objects.filter(tarjeta=tarjeta)
                .aggregate(total=Sum("cantidad"))["total"]
                or 0
            )
            gastos_tarjeta = (
                Gasto.objects.filter(metodo_pago=tarjeta)
                .aggregate(total=Sum("cantidad"))["total"]
                or 0
            )
            saldo_tarjeta = ingresos_tarjeta - gastos_tarjeta
            saldo_por_tarjeta.append({
                "tarjeta": tarjeta.metodo,
                "ingresos": ingresos_tarjeta,
                "gastos": gastos_tarjeta,
                "saldo": saldo_tarjeta,
            })

        # Crear historial combinado de ingresos y gastos
        historial = []
        for ingreso in ingresos:
            historial.append(
                {
                    "fecha": ingreso.fecha,
                    "tipo": "Ingreso",
                    "categoria": ingreso.fuente,
                    "cantidad": ingreso.cantidad,
                }
            )
        for gasto in gastos:
            historial.append(
                {
                    "fecha": gasto.fecha,
                    "tipo": "Gasto",
                    "categoria": gasto.categoria.nombre,
                    "cantidad": gasto.cantidad,
                }
            )
        historial = sorted(historial, key=lambda x: x["fecha"])

        # Contexto para la plantilla
        context = {
            "historial": historial,
            "total_ingresos_mes": total_ingresos_mes,
            "total_gastos_mes": total_gastos_mes,
            "saldo_mes": saldo_mes,
            "total_ingresos": total_ingresos,
            "total_gastos": total_gastos,
            "saldo": saldo,
            "saldo_por_tarjeta": saldo_por_tarjeta,
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


class ResumenMensualView(View):
    def get(self, request):
        hoy = datetime.date.today()
        ano = hoy.year
        mes = hoy.month

        # Obtener el primer y último día del mes
        primer_dia_mes = hoy.replace(day=1)
        ultimo_dia_mes = (primer_dia_mes + datetime.timedelta(days=31)).replace(
            day=1
        ) - datetime.timedelta(days=1)

        # Obtener ingresos y gastos por día
        ingresos_diarios = (
            Ingreso.objects.filter(fecha__year=ano, fecha__month=mes)
            .values("fecha")
            .annotate(total=Sum("cantidad"))
            .order_by("fecha")
        )
        gastos_diarios = (
            Gasto.objects.filter(fecha__year=ano, fecha__month=mes)
            .values("fecha")
            .annotate(total=Sum("cantidad"))
            .order_by("fecha")
        )

        # Convertir los datos a formato adecuado para la gráfica
        fechas = []
        ingresos = []
        gastos = []

        current_date = primer_dia_mes
        while current_date <= ultimo_dia_mes:
            fechas.append(current_date.strftime("%d-%m"))  # Formato día-mes
            ingreso_total = next(
                (
                    item["total"]
                    for item in ingresos_diarios
                    if item["fecha"] == current_date
                ),
                0,
            )
            gasto_total = next(
                (
                    item["total"]
                    for item in gastos_diarios
                    if item["fecha"] == current_date
                ),
                0,
            )
            ingresos.append(ingreso_total)
            gastos.append(gasto_total)
            current_date += datetime.timedelta(days=1)

        data = {
            "labels": fechas,
            "ingresos": ingresos,
            "gastos": gastos,
        }

        return JsonResponse(data)
