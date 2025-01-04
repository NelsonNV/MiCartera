from django.urls import path
from cartera.views import  home_views
from cartera.views.categoria_views import (
    CategoriaListView,
    CategoriaCreateView,
    CategoriaUpdateView,
    CategoriaDeleteView,
)
from cartera.views.fuente_views import (
    FuenteListView,
    FuenteCreateView,
    FuenteUpdateView,
    FuenteDeleteView,
)
from cartera.views.subcategoria_views import (
    SubcategoriaListView,
    SubcategoriaCreateView,
    SubcategoriaUpdateView,
    SubcategoriaDeleteView,
    LoadSubcategoriasView,
)
from cartera.views.gasto_views import (
    GastoListView,
    GastoCreateView,
    GastoUpdateView,
    GastoDeleteView,)
from cartera.views.ingreso_views import IngresoCreateView, IngresoListView, IngresoUpdateView, IngresoDeleteView
from cartera.views.metodopago_views import  (
    MetodoPagoListView,
    MetodoPagoCreateView,
    MetodoPagoUpdateView,
    MetodoPagoDeleteView,
)


urlpatterns = [
    path("", home_views.HomeView.as_view(), name="home"),
    # api
    path("api/resumen_anual/", home_views.ResumenAnualView.as_view(), name="resumen_anual"),
    path("api/resumen_mensual/", home_views.ResumenMensualView.as_view(), name="resumen_mensual"),
    path("api/gastos-por-categoria/", home_views.GastosPorCategoriaView.as_view(), name="gastos_por_categoria"),
    path('api/load-subcategorias/', LoadSubcategoriasView.as_view(), name='load_subcategorias'),
    # Categorias
    path("categorias/", CategoriaListView.as_view(), name="categoria_list"),
    path("categorias/crear/", CategoriaCreateView.as_view(), name="categoria_create"),
    path("categorias/editar/<int:pk>/", CategoriaUpdateView.as_view(), name="categoria_update"),
    path("categorias/eliminar/<int:pk>/", CategoriaDeleteView.as_view(), name="categoria_delete"),
    # SubCategorias
    path("subcategorias/", SubcategoriaListView.as_view(), name="subcategoria_list"),
    path("subcategorias/crear/", SubcategoriaCreateView.as_view(), name="subcategoria_create"),
    path("subcategorias/editar/<int:pk>/", SubcategoriaUpdateView.as_view(), name="subcategoria_update"),
    path("subcategorias/eliminar/<int:pk>/", SubcategoriaDeleteView.as_view(), name="subcategoria_delete"),
    # Fuentes
    path("fuentes/", FuenteListView.as_view(), name="fuente_list"),
    path("fuentes/crear/", FuenteCreateView.as_view(), name="fuente_create"),
    path("fuentes/editar/<int:pk>/", FuenteUpdateView.as_view(), name="fuente_update"),
    path("fuentes/eliminar/<int:pk>/", FuenteDeleteView.as_view(), name="fuente_delete"),
   # Ingresos
    path("ingresos/", IngresoListView.as_view(), name="ingreso_list"),
    path("ingresos/crear/", IngresoCreateView.as_view(), name="ingreso_create"),
    path("ingresos/editar/<int:pk>/", IngresoUpdateView.as_view(), name="ingreso_update"),
    path("ingresos/eliminar/<int:pk>/", IngresoDeleteView.as_view(), name="ingreso_delete"),
    # Gastos
    path("gastos/", GastoListView.as_view(), name="gasto_list"),
    path("gastos/crear/", GastoCreateView.as_view(), name="gasto_create"),
    path("gastos/editar/<int:pk>/", GastoUpdateView.as_view(), name="gasto_update"),
    path("gastos/eliminar/<int:pk>/", GastoDeleteView.as_view(), name="gasto_delete"),
     # Métodos de Pago
    path("metodospago/", MetodoPagoListView.as_view(), name="metodopago_list"),
    path("metodospago/crear/", MetodoPagoCreateView.as_view(), name="metodopago_create"),
    path("metodospago/editar/<int:pk>/", MetodoPagoUpdateView.as_view(), name="metodopago_update"),
    path("metodospago/eliminar/<int:pk>/", MetodoPagoDeleteView.as_view(), name="metodopago_delete"),
]
