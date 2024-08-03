from django import forms
from .models import Categoria, Subcategoria, Fuente, Ingreso, Gasto, MetodoPago


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "input", "placeholder": "Nombre de la categoría"}
            ),
        }


class MetodoPagoForm(forms.ModelForm):
    class Meta:
        model = MetodoPago
        fields = ["metodo"]
        widgets = {"metodo": forms.TextInput(attrs={"class": "input"})}


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
        fields = ["fecha", "fuente", "cantidad", "descripcion"]
        widgets = {
            "fecha": forms.DateInput(attrs={"class": "input", "type": "date"}),
            "fuente": forms.Select(attrs={"class": "select2 input"}),
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
            "categoria": forms.Select(attrs={"class": "select", "id": "id_categoria"}),
            "subcategoria": forms.Select(
                attrs={"class": "select", "id": "id_subcategoria"}
            ),
            "cantidad": forms.NumberInput(
                attrs={"class": "input", "placeholder": "Cantidad", "step": "0.01"}
            ),
            "metodo_pago": forms.Select(attrs={"class": "select"}),
            "descripcion": forms.Textarea(
                attrs={"class": "textarea", "placeholder": "Descripción", "rows": 3}
            ),
        }
