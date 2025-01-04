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

        # Calcular ingresos, gastos y saldos para el mes
        total_ingresos_mes, total_gastos_mes, ingresos_mes, gastos_mes = self._calcular_ingresos_y_gastos(
            first_day_of_month, last_day_of_month
        )
        saldo_mes = total_ingresos_mes - total_gastos_mes

        # Calcular ingresos, gastos y saldos totales
        total_ingresos, total_gastos, _, _ = self._calcular_ingresos_y_gastos(
            datetime.date.min, datetime.date.max
        )
        saldo = total_ingresos - total_gastos

        # Calcular saldo por tarjeta
        saldo_por_tarjeta = self._calcular_saldo_por_tarjeta()

        # Crear historial combinado
        historial = self._generar_historial(ingresos_mes, gastos_mes)

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

    def _calcular_ingresos_y_gastos(self, fecha_inicio, fecha_fin):
        """Calcula los ingresos y gastos en un rango de fechas."""
        ingresos = Ingreso.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        gastos = Gasto.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        total_ingresos = ingresos.aggregate(total=Sum("cantidad"))["total"] or 0
        total_gastos = gastos.aggregate(total=Sum("cantidad"))["total"] or 0
        return total_ingresos, total_gastos, ingresos, gastos

    def _calcular_saldo_por_tarjeta(self):
        """Calcula el saldo por tarjeta."""
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
        return saldo_por_tarjeta

    def _generar_historial(self, ingresos, gastos):
        """Crea un historial combinado de ingresos y gastos."""
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
        return sorted(historial, key=lambda x: x["fecha"])
class GastosPorCategoriaView(View):
    def get(self, request):
        mes = request.GET.get("mes", datetime.date.today().month)
        ano = request.GET.get("ano", datetime.date.today().year)
        formato = request.GET.get("format")

        gastos = (
            Gasto.objects.filter(fecha__month=mes, fecha__year=ano)
            .values("categoria__nombre", "subcategoria__nombre")
            .annotate(total=Sum("cantidad"))
            .order_by("-total")
        )

        data = {}
        for gasto in gastos:
            categoria = gasto["categoria__nombre"]
            subcategoria = gasto["subcategoria__nombre"]
            total = gasto["total"]

            if categoria not in data:
                data[categoria] = {"total": 0, "subcategorias": {}}
            data[categoria]["total"] += total
            data[categoria]["subcategorias"][subcategoria] = total

        if formato == "sunburst":
            return JsonResponse(self.transformar_a_sunburst(data), safe=False)
        return JsonResponse(data)

    def transformar_a_sunburst(self, data):
        """
        Transforma los datos al formato requerido por el gráfico Sunburst.
        """
        return [
            {
                "name": categoria,
                "value": float(detalles["total"]),
                "children": [
                    {"name": subcategoria, "value": float(valor)}
                    for subcategoria, valor in detalles["subcategorias"].items()
                ],
            }
            for categoria, detalles in data.items()
        ]

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
