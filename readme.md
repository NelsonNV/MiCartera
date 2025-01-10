# instalar dependencias

```bash
pip install -r requirements.txt
```

# migraciones

```bash
python manage.py makemigrations wish cartera
python manage.py migrate
```
# crear superusuario

```bash
python manage.py createsuperuser
```

# generar fixture

```bash
python generate_fixture.py
```

# cargar fixture

```bash
python manage.py loaddata fixture.json
```

# ejecutar servidor

```bash
python manage.py runserver
```
