import json
import random
from datetime import datetime, timedelta

def generate_fixture(output_file="fixture.json", num_records=500):
    """
    Genera un archivo fixture.json con datos ficticios para Django.

    :param output_file: Nombre del archivo de salida.
    :param num_records: Número total de registros de ingresos y gastos.
    """
    data = []
    current_pk = 1
    categorias = [
    "Servicios", "Consumo Diario", "Entretenimiento", "Tecnología",
    "Educación", "Donaciones", "Transporte", "Salud", "Hogar", "Finanzas"
    ]

    subcategorias = {
    "Servicios": [
        "Copilot", "Figma", "Netflix", "Spotify", 
        "Amazon Prime", "Disney+", "HBO Max", "Canva", 
        "Google Workspace", "Microsoft 365"
    ],
    "Consumo Diario": [
        "Supermercado", "Panadería", "Verdulería", "Carnicería", 
        "Comida rápida", "Snacks", "Bebidas", "Cafetería"
    ],
    "Entretenimiento": [
        "Cine", "Conciertos", "Videojuegos", "Libros", 
        "Streaming de música", "Eventos deportivos", "Parques temáticos"
    ],
    "Tecnología": [
        "Software", "Hardware", "Periféricos", "Suscripciones de apps", 
        "Reparaciones", "Domótica", "Gadgets"
    ],
    "Educación": [
        "Cursos online", "Libros académicos", "Membresías educativas", 
        "Tutores", "Conferencias", "Material de estudio"
    ],
    "Donaciones": [
        "ONGs", "Causas sociales", "Eventos de caridad", 
        "Donaciones a individuos", "Campañas de crowdfunding"
    ],
    "Transporte": [
        "Transporte público", "Gasolina", "Peajes", 
        "Reparación de vehículo", "Estacionamiento", "Alquiler de vehículos"
    ],
    "Salud": [
        "Consultas médicas", "Medicamentos", "Hospitalización", 
        "Seguros de salud", "Terapias", "Cuidado dental"
    ],
    "Hogar": [
        "Muebles", "Electrodomésticos", "Decoración", 
        "Servicios básicos (agua, luz, gas)", 
        "Herramientas", "Jardinería"
    ],
    "Finanzas": [
        "Pagos de préstamos", "Intereses bancarios", "Transferencias", 
        "Inversiones", "Seguros de vida", "Tarjetas de crédito"
    ]
    }
    # Crear categorías
    for cat_pk, cat in enumerate(categorias, start=1):
        data.append({"model": "cartera.categoria", "pk": cat_pk, "fields": {"nombre": cat}})
    categoria_ids = list(range(1, len(categorias) + 1))

    # Crear subcategorías
    subcat_pk = 1
    for cat_pk, cat in enumerate(categorias, start=1):
        for subcat in subcategorias[cat]:
            data.append({"model": "cartera.subcategoria", "pk": subcat_pk, "fields": {"nombre": subcat, "categoria": cat_pk}})
            subcat_pk += 1
    subcategoria_ids = list(range(1, subcat_pk))

    # Fuentes de ingreso
    fuentes = ["Sueldo", "Regalos", "Pago de deudas", "Transferencia personal"]
    for fuente_pk, fuente in enumerate(fuentes, start=1):
        data.append({"model": "cartera.fuente", "pk": fuente_pk, "fields": {"nombre": fuente}})
    fuente_ids = list(range(1, len(fuentes) + 1))

    # Métodos de pago
    metodos = ["Banco estado", "Efectivo", "Mach"]
    for metodo_pk, metodo in enumerate(metodos, start=1):
        data.append({"model": "cartera.metodopago", "pk": metodo_pk, "fields": {"metodo": metodo}})
    metodo_ids = list(range(1, len(metodos) + 1))

    # Calcular rango de fechas (últimos 12 meses hasta el mes actual)
    today = datetime.today()
    start_date = today.replace(day=1) - timedelta(days=365)

    # Generar ingresos
    for i in range(num_records // 2):
        fecha = start_date + timedelta(days=random.randint(0, (today - start_date).days))
        fuente = random.choice(fuente_ids)
        cantidad = round(random.uniform(1000, 1000000), 2)
        descripcion = f"Ingreso generado automáticamente {i + 1}"
        tarjeta = random.choice(metodo_ids)
        data.append({
            "model": "cartera.ingreso",
            "pk": current_pk,
            "fields": {
                "fecha": fecha.strftime('%Y-%m-%d'),
                "fuente": fuente,
                "cantidad": f"{cantidad:.2f}",
                "descripcion": descripcion,
                "tarjeta": tarjeta
            }
        })
        current_pk += 1

    # Generar gastos
    for i in range(num_records // 2):
        fecha = start_date + timedelta(days=random.randint(0, (today - start_date).days))
        categoria = random.choice(categoria_ids)
        subcategoria = random.choice(subcategoria_ids)
        cantidad = round(random.uniform(500, 200000), 2)
        metodo_pago = random.choice(metodo_ids)
        descripcion = f"Gasto generado automáticamente {i + 1}"
        data.append({
            "model": "cartera.gasto",
            "pk": current_pk,
            "fields": {
                "fecha": fecha.strftime('%Y-%m-%d'),
                "categoria": categoria,
                "subcategoria": subcategoria,
                "cantidad": f"{cantidad:.2f}",
                "metodo_pago": metodo_pago,
                "descripcion": descripcion
            }
        })
        current_pk += 1

    # Guardar el archivo JSON
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Fixture generado exitosamente en {output_file}")


if __name__ == "__main__":
    generate_fixture(output_file="fixture.json", num_records=1000)
