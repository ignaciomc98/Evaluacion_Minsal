# Usamos una imagen oficial de Python como base
FROM python:3.11-slim

# Variables de entorno para que pip no guarde cache (reduce tamaño)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crear y definir el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements.txt y luego instalar dependencias
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar todo el código fuente dentro del contenedor
COPY app/ app/

# Exponer el puerto donde correrá uvicorn
EXPOSE 8000

# Comando para ejecutar la app con uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
