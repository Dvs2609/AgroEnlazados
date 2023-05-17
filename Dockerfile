# Selecciona la imagen base
FROM python:3.9

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crea y define el directorio de trabajo en el contenedor
WORKDIR /code

# Instala psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Actualiza pip
RUN pip install --upgrade pip

# Instala las dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia el proyecto
COPY . .

# Ejecuta el servidor web
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
