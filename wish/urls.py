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
from wish.views.alternativa_views import (
    AlternativaListView,
    AlternativaCreateView,
    AlternativaUpdateView,
    AlternativaDeleteView,
)
from wish.views.deseo_views import (
    DeseoListView,
    DeseoCreateView,
    DeseoUpdateView,
    DeseoDeleteView,
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
    path("alternativas/", AlternativaListView.as_view(), name="wish_alternativa"),
    path(
        "alternativas/crear/",
        AlternativaCreateView.as_view(),
        name="wish_alternativa_create",
    ),
    path(
        "alternativas/<int:pk>/editar/",
        AlternativaUpdateView.as_view(),
        name="wish_alternativa_update",
    ),
    path(
        "alternativas/<int:pk>/eliminar/",
        AlternativaDeleteView.as_view(),
        name="wish_alternativa_delete",
    ),
    path("deseos/", DeseoListView.as_view(), name="wish_deseo"),
    path("deseos/crear/", DeseoCreateView.as_view(), name="wish_deseo_create"),
    path(
        "deseos/<int:pk>/editar/",
        DeseoUpdateView.as_view(),
        name="wish_deseo_update",
    ),
    path(
        "deseos/<int:pk>/eliminar/",
        DeseoDeleteView.as_view(),
        name="wish_deseo_delete",
    ),
]
