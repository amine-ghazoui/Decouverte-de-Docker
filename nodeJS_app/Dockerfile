# Utiliser une image Alpine (plus légère)
FROM node:18-alpine

# Informations
LABEL maintainer="abdelmonaimahdoud3@gmail.com"
LABEL version="1.1"
LABEL description="Application Node.js optimisée"

# Créer un utilisateur non-root pour la sécurité
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installer uniquement les dépendances de production
RUN npm install --omit=dev && \
    npm cache clean --force

# Copier le code source
COPY --chown=nodejs:nodejs server.js ./

# Changer l'utilisateur
USER nodejs

# Exposer le port
EXPOSE 3000

# Variables d'environnement
ENV NODE_ENV=production \
    PORT=3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Commande de démarrage
CMD ["node", "server.js"]