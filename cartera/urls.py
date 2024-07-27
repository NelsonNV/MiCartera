from django.urls import path
from cartera import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("resumen_anual/", views.ResumenAnualView.as_view(), name="resumen_anual"),
    path("api/gastos-por-categoria/", views.GastosPorCategoriaView.as_view(), name="gastos_por_categoria"),
    # Categorías
    path("categorias/", views.CategoriaListView.as_view(), name="categoria_list"),
    path("categorias/crear/", views.CategoriaCreateView.as_view(), name="categoria_create"),
    path("categorias/editar/<int:pk>/", views.CategoriaUpdateView.as_view(), name="categoria_update"),
    path("categorias/eliminar/<int:pk>/", views.CategoriaDeleteView.as_view(), name="categoria_delete"),
    # Subcategorías
    path("subcategorias/", views.SubcategoriaListView.as_view(), name="subcategoria_list"),
    path("subcategorias/crear/", views.SubcategoriaCreateView.as_view(), name="subcategoria_create"),
    path("subcategorias/editar/<int:pk>/", views.SubcategoriaUpdateView.as_view(), name="subcategoria_update"),
    path("subcategorias/eliminar/<int:pk>/", views.SubcategoriaDeleteView.as_view(), name="subcategoria_delete"),
    # Fuentes
    path("fuentes/", views.FuenteListView.as_view(), name="fuente_list"),
    path("fuentes/crear/", views.FuenteCreateView.as_view(), name="fuente_create"),
    path("fuentes/editar/<int:pk>/", views.FuenteUpdateView.as_view(), name="fuente_update"),
    path("fuentes/eliminar/<int:pk>/", views.FuenteDeleteView.as_view(), name="fuente_delete"),
    # Ingresos
    path("ingresos/", views.IngresoListView.as_view(), name="ingreso_list"),
    path("ingresos/crear/", views.IngresoCreateView.as_view(), name="ingreso_create"),
    path("ingresos/editar/<int:pk>/", views.IngresoUpdateView.as_view(), name="ingreso_update"),
    path("ingresos/eliminar/<int:pk>/", views.IngresoDeleteView.as_view(), name="ingreso_delete"),
    # Gastos
    path("gastos/", views.GastoListView.as_view(), name="gasto_list"),
    path("gastos/crear/", views.GastoCreateView.as_view(), name="gasto_create"),
    path("gastos/editar/<int:pk>/", views.GastoUpdateView.as_view(), name="gasto_update"),
    path("gastos/eliminar/<int:pk>/", views.GastoDeleteView.as_view(), name="gasto_delete"),
]
