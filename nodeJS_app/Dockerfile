FROM node:18

# Informations sur l'image
LABEL maintainer="abdelmonaimahdoud3@gmail.com"
LABEL version="1.0"
LABEL description="Application Node.js avec Express"

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste du code
COPY . .

# Exposer le port
EXPOSE 3000

# Variable d'environnement
ENV NODE_ENV=production

# Commande de démarrage
CMD ["npm", "start"]
