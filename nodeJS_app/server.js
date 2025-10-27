const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware pour logger les requêtes
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
    next();
});

// Route : Page d'accueil
app.get('/', (req, res) => {
    res.send(`
    <html>
      <head>
        <title>Node.js App</title>
        <style>
          body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
          h1 { color: #2196F3; }
          .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
          code { background: #e0e0e0; padding: 2px 6px; border-radius: 3px; }
        </style>
      </head>
      <body>
        <h1>🐳 Bienvenue sur Node-App</h1>
        <p>Application Node.js containerisée avec Docker</p>
        <h2>Endpoints disponibles :</h2>
        <div class="endpoint">
          <strong>GET /</strong> - Page d'accueil (vous êtes ici)
        </div>
        <div class="endpoint">
          <strong>GET /api/health</strong> - Status de l'application
        </div>
        <div class="endpoint">
          <strong>GET /api/info</strong> - Informations sur l'environnement
        </div>
        <div class="endpoint">
          <strong>GET /api/time</strong> - Heure actuelle du serveur
        </div>
      </body>
    </html>
  `);
});

// Route : Health check
app.get('/api/health', (req, res) => {
    res.json({
        status: 'OK',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        message: 'Application is running smoothly'
    });
});

// Route : Informations environnement
app.get('/api/info', (req, res) => {
    res.json({
        nodeVersion: process.version,
        platform: process.platform,
        architecture: process.arch,
        hostname: require('os').hostname(),
        memory: {
            total: `${Math.round(require('os').totalmem() / 1024 / 1024)} MB`,
            free: `${Math.round(require('os').freemem() / 1024 / 1024)} MB`,
            used: `${Math.round(process.memoryUsage().heapUsed / 1024 / 1024)} MB`
        },
        environment: process.env.NODE_ENV || 'development'
    });
});

// Route : Heure actuelle
app.get('/api/time', (req, res) => {
    const now = new Date();
    res.json({
        iso: now.toISOString(),
        locale: now.toLocaleString('fr-FR', {
            timeZone: 'Europe/Paris',
            dateStyle: 'full',
            timeStyle: 'long'
        }),
        unix: Math.floor(now.getTime() / 1000),
        timezone: 'Europe/Paris'
    });
});

// Gestion des routes non trouvées
app.use((req, res) => {
    res.status(404).json({
        error: 'Route not found',
        path: req.url,
        availableRoutes: ['/', '/api/health', '/api/info', '/api/time']
    });
});

// Démarrage du serveur
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server is running on port ${PORT}`);
    console.log(`Access the app at http://localhost:${PORT}`);
});