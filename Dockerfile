# image Python
FROM python:3.11

# répertoire de travail
WORKDIR /app

# Installer les dépendances
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copier les fichiers du projet dans le conteneur
COPY . .

# Exposer le port utilisé par FastAPI
EXPOSE 8000

# Lancer l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
