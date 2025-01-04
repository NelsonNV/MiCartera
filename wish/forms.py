from django import forms
from wish.models import Categoria, Tiendas, Producto, Alternativa, Deseo
from core.widgets import BulmaFileInput


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "input"}),
        }


class TiendasForm(forms.ModelForm):
    class Meta:
        model = Tiendas
        fields = ["nombre", "enlace", "logo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "input"}),
            "enlace": forms.URLInput(attrs={"class": "input"}),
            "logo": BulmaFileInput(attrs={"class": "file-input"}),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "imagen"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "input"}),
            "imagen": BulmaFileInput(attrs={"class": "file-input"}),
        }


class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = ["producto", "tienda", "enlace", "imagen", "costo"]
        widgets = {
            "producto": forms.Select(attrs={"class": "select"}),
            "tienda": forms.Select(attrs={"class": "select"}),
            "enlace": forms.URLInput(attrs={"class": "input"}),
            "imagen": BulmaFileInput(attrs={"class": "file-input"}),
            "costo": forms.NumberInput(attrs={"class": "input"}),
        }


class DeseoForm(forms.ModelForm):
    class Meta:
        model = Deseo
        fields = ["categoria", "producto"]
        widgets = {
            "categoria": forms.Select(attrs={"class": "select"}),
            "producto": forms.Select(attrs={"class": "select"}),
        }
