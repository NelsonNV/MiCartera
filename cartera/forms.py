from django import forms
from .models import Categoria, Subcategoria, Fuente, Ingreso, Gasto


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre"]


class SubcategoriaForm(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = ["nombre", "categoria"]


class FuenteForm(forms.ModelForm):
    class Meta:
        model = Fuente
        fields = ["nombre"]


class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ["fecha", "fuente", "categoria", "cantidad", "descripcion"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
        }


class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = [
            "fecha",
            "categoria",
            "subcategoria",
            "cantidad",
            "metodo_pago",
            "descripcion",
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
        }
