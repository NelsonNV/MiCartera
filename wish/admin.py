from django.contrib import admin
from wish.models import Categoria, Tiendas, Producto, Alternativa, Deseo


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(Tiendas)
class TiendasAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "enlace")
    search_fields = ("nombre", "enlace")
    ordering = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(Alternativa)
class AlternativaAdmin(admin.ModelAdmin):
    list_display = ("id", "producto", "tienda", "enlace", "costo")
    search_fields = ("producto__nombre", "tienda__nombre", "enlace")
    list_filter = ("producto", "tienda")
    ordering = ("producto",)


@admin.register(Deseo)
class DeseoAdmin(admin.ModelAdmin):
    list_display = ("id", "categoria", "producto")
    search_fields = ("categoria__nombre", "producto__nombre")
    list_filter = ("categoria",)
    ordering = ("categoria",)
