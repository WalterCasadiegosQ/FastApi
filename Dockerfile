FROM python:3.13-alpine

# Instalar dependencias del sistema
RUN apk add --no-cache gcc musl-dev postgresql-dev

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de la aplicación
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app

# Comando para iniciar la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
