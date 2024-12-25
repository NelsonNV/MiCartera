from django.urls import path
from wish.views.categoria_views import (
    CategoriaListView,
    CategoriaCreateView,
    CategoriaUpdateView,
    CategoriaDeleteView,
)
from wish.views.tiendas_views import (
    TiendasListView,
    TiendasDetailView,
    TiendasCreateView,
    TiendasUpdateView,
    TiendasDeleteView,
)
from wish.views.productos_views import (
    ProductoListView,
    ProductoCreateView,
    ProductoUpdateView,
    ProductoDeleteView,
)

urlpatterns = [
    path("categorias/", CategoriaListView.as_view(), name="wish_categoria"),
    path(
        "categorias/crear/", CategoriaCreateView.as_view(), name="wish_categoria_create"
    ),
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
    path("tiendas/", TiendasListView.as_view(), name="wish_tiendas_list"),
    path("tiendas/<int:pk>/", TiendasDetailView.as_view(), name="wish_tiendas_detail"),
    path("tiendas/crear/", TiendasCreateView.as_view(), name="wish_tiendas_create"),
    path(
        "tiendas/<int:pk>/editar/",
        TiendasUpdateView.as_view(),
        name="wish_tiendas_update",
    ),
    path(
        "tiendas/<int:pk>/eliminar/",
        TiendasDeleteView.as_view(),
        name="wish_tiendas_delete",
    ),
    path("productos/", ProductoListView.as_view(), name="wish_producto"),
    path("productos/crear/", ProductoCreateView.as_view(), name="wish_producto_create"),
    path(
        "productos/<int:pk>/editar/",
        ProductoUpdateView.as_view(),
        name="wish_producto_updates",
    ),
    path(
        "productos/<int:pk>/eliminar/",
        ProductoDeleteView.as_view(),
        name="wish_producto_delete",
    ),
]
