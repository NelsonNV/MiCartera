from django.shortcuts import render, redirect
from .forms import CategoriaForm, SubcategoriaForm, FuenteForm, IngresoForm, GastoForm


def formulario(request):
    forms = {
        "categoria": CategoriaForm(),
        "subcategoria": SubcategoriaForm(),
        "fuente": FuenteForm(),
        "ingreso": IngresoForm(),
        "gasto": GastoForm(),
    }

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type in forms:
            form = forms[form_type].__class__(
                request.POST
            )  # Instanciar el formulario con los datos POST

            if form.is_valid():
                form.save()  # Guardar el formulario si es válido
                return redirect("formulario")

    return render(request, "formulario.html", {"forms": forms})
