from django import template
from django.urls import reverse, NoReverseMatch
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_table(
    headers, fields, items, permiso=False, update_url=None, delete_url=None, null=None, image_fields=None
):
    """
    Genera una tabla HTML dinámica con los botones de acción (Editar, Eliminar).
    headers: Lista de encabezados de la tabla.
    fields: Lista de campos que deben mostrarse de cada objeto.
    items: Lista de objetos o diccionarios a mostrar.
    permiso: Si es True, se agregan los botones de acción.
    update_url: URL para editar un objeto.
    delete_url: URL para eliminar un objeto.
    null: Diccionario opcional para definir valores a mostrar si el campo es None o vacío.
    image_fields: Lista de campos que representan URLs de imágenes.
    """
    null = null or {}
    image_fields = image_fields or []
    table_html = '<table class="table table-bordered table-striped">'

    # Generar los encabezados de la tabla
    table_html += "<thead><tr>"
    for header in headers:
        table_html += f"<th>{header}</th>"
    if permiso:
        table_html += "<th>Acciones</th>"
    table_html += "</tr></thead>"

    # Generar las filas de la tabla
    table_html += "<tbody>"
    for item in items:
        table_html += "<tr>"
        # Generar las celdas de la tabla según los campos proporcionados

        for field in fields:
            if isinstance(item, dict):  # Verificar si el item es un diccionario
                field_value = item.get(field, "")
            else:  # Si no es un diccionario, tratamos como un objeto
                field_value = getattr(item, field, None)

            # Si el campo es None o vacío, usar el valor definido en null si existe
            if not field_value and field in null:
                field_value = null[field]

            if field in image_fields:
                if field_value:
                    # Si es un objeto con un atributo `url`, obtén la URL
                    if hasattr(field_value, "url"):
                        field_value = field_value.url
                    table_html += f'<td><img src="{field_value}" alt="{field}" style="max-width: 100px; max-height: 100px;"></td>'
                else:
                    # Mostrar un mensaje si no hay imagen
                    table_html += "<td>(Sin imagen)</td>"
            else:
                # Asegurarse de que field_value sea representable como cadena
                field_value = str(field_value) if field_value is not None else ""
                table_html += f"<td>{field_value}</td>"

        # Si permiso es True, agregar los botones de editar y eliminar
        if permiso:
            try:
                url_update = reverse(
                    update_url,
                    args=[item["pk"]] if isinstance(item, dict) else [item.pk],
                )
                url_delete = reverse(
                    delete_url,
                    args=[item["pk"]] if isinstance(item, dict) else [item.pk],
                )
            except NoReverseMatch:
                url_update = "#"
                url_delete = "#"

            table_html += f"""
                <td>
                    <a href="{url_update}" class="button is-warning">Editar</a>
                    <a href="{url_delete}" class="button is-danger">Eliminar</a>
                </td>
            """
        table_html += "</tr>"
    table_html += "</tbody>"

    table_html += "</table>"

    return mark_safe(table_html)
