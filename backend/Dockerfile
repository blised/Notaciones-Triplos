FROM python:3.13

WORKDIR /app

COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Node.js y npm dentro del contenedor
RUN apt-get update && apt-get install -y nodejs npm

# Instalar TailwindCSS localmente dentro del proyecto
RUN npm init -y && npm install tailwindcss

# Copiar todos los archivos del proyecto después de instalar Tailwind
COPY . .

# Generar el CSS con TailwindCSS
RUN npx tailwindcss -i ./static/css/styles.css -o ./static/css/output.css --minify || true

EXPOSE 8000

CMD ["python", "main.py"]