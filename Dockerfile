# Usa una imagen base de Python
FROM python:3.8-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos primero, para aprovechar la caché de Docker
COPY generar_datos.py validar_datos.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de tu aplicación
COPY . .

# Expone el puerto 8000 para acceder a tu aplicación FastAPI
EXPOSE 8000

# Comando que ejecuta el script (por ejemplo, primero generamos datos y luego validamos)
CMD ["bash", "-c", "python generar_datos.py && python validar_datos.py"]
