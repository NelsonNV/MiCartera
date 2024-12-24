from django.urls import path
from wish.views.categoria_views import (
    CategoriaListView,
    CategoriaCreateView,
    CategoriaUpdateView,
    CategoriaDeleteView,
)

urlpatterns = [
    path("categorias/", CategoriaListView.as_view(), name="wish_categoria"),
    path("categorias/crear/", CategoriaCreateView.as_view(), name="create_view_name"),
    path(
        "cate/upd/<int:pk>/",
        CategoriaUpdateView.as_view(),
        name="wish_categoria_update",
    ),
    path(
        "categorias/delete/<int:pk>/",
        CategoriaDeleteView.as_view(),
        name="wish_categoria_delete",
    ),
]
