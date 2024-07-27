from django import forms
from .models import Categoria, Subcategoria, Fuente, Ingreso, Gasto


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "input", "placeholder": "Nombre de la categoría"}
            ),
        }


class SubcategoriaForm(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = ["nombre", "categoria"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "input", "placeholder": "Nombre de la subcategoría"}
            ),
            "categoria": forms.Select(attrs={"class": "select"}),
        }


class FuenteForm(forms.ModelForm):
    class Meta:
        model = Fuente
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "input", "placeholder": "Nombre de la fuente"}
            ),
        }


class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ["fecha", "fuente", "categoria", "cantidad", "descripcion"]
        widgets = {
            "fecha": forms.DateInput(attrs={"class": "input", "type": "date"}),
            "fuente": forms.Select(attrs={"class": "select2 input"}),
            "categoria": forms.Select(attrs={"class": "select2 input"}),
            "cantidad": forms.NumberInput(
                attrs={"class": "input", "placeholder": "Cantidad", "step": "0.01"}
            ),
            "descripcion": forms.Textarea(
                attrs={"class": "textarea", "placeholder": "Descripción", "rows": 3}
            ),
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
            "fecha": forms.DateInput(attrs={"class": "input", "type": "date"}),
            "categoria": forms.Select(attrs={"class": "select"}),
            "subcategoria": forms.Select(attrs={"class": "select"}),
            "cantidad": forms.NumberInput(
                attrs={"class": "input", "placeholder": "Cantidad", "step": "0.01"}
            ),
            "metodo_pago": forms.TextInput(
                attrs={"class": "input", "placeholder": "Método de pago"}
            ),
            "descripcion": forms.Textarea(
                attrs={"class": "textarea", "placeholder": "Descripción", "rows": 3}
            ),
        }
