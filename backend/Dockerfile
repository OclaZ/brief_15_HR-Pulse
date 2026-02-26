# backend/Dockerfile
FROM python:3.10-slim-bullseye

WORKDIR /app

# 1. Installation des dépendances système (ODBC pour Azure SQL)
RUN apt-get update && apt-get install -y \
    curl apt-transport-https gnupg2 build-essential unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean

# 2. Copie du fichier des dépendances
COPY requirements.txt .

# 3. Installation des librairies + outils de test
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest httpx

# 4. Copie de tout le code source
COPY . .

# 🔴 FIX DOCKER : On indique à Python que le dossier /app est la racine du projet
ENV PYTHONPATH=/app

# 🛡️ BARRIÈRE DE SÉCURITÉ (PHASE 6)
# Docker va exécuter les tests. Si un test échoue, la création de l'image est annulée !
RUN python -m pytest tests/

# 5. Configuration finale
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]