# Utilise une image officielle avec Python + ffmpeg
FROM python:3.10-slim

# Installe ffmpeg + dépendances système
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Crée le répertoire de l’app
WORKDIR /app

# Copie les fichiers de l’app
COPY . .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Lance le serveur avec gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
