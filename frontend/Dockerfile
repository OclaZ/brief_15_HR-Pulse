# frontend/Dockerfile
# Étape 1 : Construction
FROM node:18-alpine AS builder
WORKDIR /app

# On copie d'abord les fichiers de configuration npm
COPY package*.json ./

# 🔴 CORRECTION 1 : On remplace 'npm ci' par 'npm install'
# Cela évite les plantages si le package-lock.json généré sous Windows a des conflits avec l'environnement Linux Alpine.
RUN npm install

# On copie le reste du code source
COPY . .

# 🔴 CORRECTION 2 : On désactive la télémétrie de Next.js
# Cela empêche Next.js d'essayer de se connecter à ses serveurs de statistiques pendant le build, ce qui cause souvent des timeouts dans Docker.
ENV NEXT_TELEMETRY_DISABLED=1

# Lancement de la compilation
RUN npm run build

# Étape 2 : Exécution (Image allégée)
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED=1

# On ne copie que les fichiers nécessaires générés par le builder
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Exposer le port de Next.js
EXPOSE 3000

# Commande de lancement
CMD ["npm", "start"]