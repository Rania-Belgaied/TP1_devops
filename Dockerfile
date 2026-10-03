#image de base Slim
FROM python:3.12-slim

#éviter les fichiers inutiles .pyc
ENV PYTHONDONTWRITEBYTECODE=1

#afficher logs immédiats
ENV PYTHONUNBUFFERED=1

#Créer un utilisateur non-root
RUN useradd --create-home appuser

#définit le répertoire de travail
WORKDIR /app

#copie seulement les dépendances et les installer
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copie le code de l'application
COPY app/app.py .

#exécuter l'application avec un utilisateur non-root
USER appuser

#port utilisé par l'application
EXPOSE 5000

#Commande exécuté au démarrage du conteneur
CMD ["python", "app.py"]