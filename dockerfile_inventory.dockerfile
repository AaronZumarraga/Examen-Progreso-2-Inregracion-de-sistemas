# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de tu proyecto al contenedor
COPY . /app

# Instalar las dependencias necesarias
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean

# Exponer el puerto que usará Flask
EXPOSE 5000

# Establecer el comando para ejecutar la aplicación
CMD ["python", "app.py"]
