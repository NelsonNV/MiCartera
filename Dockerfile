FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["bash", "-c", "python manage.py makemigrations wish cartera && \
                    python manage.py migrate && \
                    python generate_fixture.py &&\
                    python manage.py loaddata fixture.json && \
                    python manage.py runserver 0.0.0.0:8000"]
