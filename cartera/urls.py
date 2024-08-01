from django.urls import path
from cartera.views import  home_views
from cartera.views.categoria_views import CategoriaView
from cartera.views.fuente_views import FuenteView
from cartera.views.subcategoria_views import SubcategoriaView
from cartera.views.gasto_views import GastoView
from cartera.views.ingreso_views import IngresoView
from cartera.views.metodopago_views import MetodoPagoView 

urlpatterns = [
    path("", home_views.HomeView.as_view(), name="home"),
    # api
    path("api/resumen_anual/", home_views.ResumenAnualView.as_view(), name="resumen_anual"),
    path("api/resumen_mensual/", home_views.ResumenMensualView.as_view(), name="resumen_mensual"),
    path("api/gastos-por-categoria/", home_views.GastosPorCategoriaView.as_view(), name="gastos_por_categoria"),
    # Categorias
    path("categorias/", CategoriaView.as_view(), name="categoria_list"),
    path("categorias/crear/", CategoriaView.as_view(), {"action": "create"}, name="categoria_create"),
    path("categorias/editar/<int:pk>/", CategoriaView.as_view(), {"action": "update"}, name="categoria_update"),
    path("categorias/eliminar/<int:pk>/", CategoriaView.as_view(), {"action": "delete"}, name="categoria_delete"),
    # SubCategorias
    path("subcategorias/", SubcategoriaView.as_view(), name="subcategoria_list"),
    path("subcategorias/crear/", SubcategoriaView.as_view(), {'action': 'create'}, name="subcategoria_create"),
    path("subcategorias/editar/<int:pk>/", SubcategoriaView.as_view(), {'action': 'update'}, name="subcategoria_update"),
    path("subcategorias/eliminar/<int:pk>/", SubcategoriaView.as_view(), {'action': 'delete'}, name="subcategoria_delete"),
    # Fuentes
    path("fuentes/", FuenteView.as_view(), name="fuente_list"),
    path("fuentes/crear/", FuenteView.as_view(), {'action': 'create'}, name="fuente_create"),
    path("fuentes/editar/<int:pk>/", FuenteView.as_view(), {'action': 'update'}, name="fuente_update"),
    path("fuentes/eliminar/<int:pk>/", FuenteView.as_view(), {'action': 'delete'}, name="fuente_delete"),
    # Ingreso
    path("ingresos/", IngresoView.as_view(), name="ingreso_list"),
    path("ingresos/crear/", IngresoView.as_view(), {'action': 'create'}, name="ingreso_create"),
    path("ingresos/editar/<int:pk>/", IngresoView.as_view(), {'action': 'update'}, name="ingreso_update"),
    path("ingresos/eliminar/<int:pk>/", IngresoView.as_view(), {'action': 'delete'}, name="ingreso_delete"),
    # Gastos
    path("gastos/", GastoView.as_view(), name="gasto_list"),
    path("gastos/crear/", GastoView.as_view(), {'action': 'create'}, name="gasto_create"),
    path("gastos/editar/<int:pk>/", GastoView.as_view(), {'action': 'update'}, name="gasto_update"),
    path("gastos/eliminar/<int:pk>/", GastoView.as_view(), {'action': 'delete'}, name="gasto_delete"),
     # Métodos de Pago
    path("metodospago/", MetodoPagoView.as_view(), name="metodopago_list"),
    path("metodospago/crear/", MetodoPagoView.as_view(), {'action': 'create'}, name="metodopago_create"),
    path("metodospago/editar/<int:pk>/", MetodoPagoView.as_view(), {'action': 'update'}, name="metodopago_update"),
    path("metodospago/eliminar/<int:pk>/", MetodoPagoView.as_view(), {'action': 'delete'}, name="metodopago_delete"),
]
