from flask import Flask, jsonify
import psycopg2
import redis
import time
import sys

app = Flask(__name__)

# Configuration
DB_CONFIG = {
    "host": "postgres-db",
    "database": "usersdb",
    "user": "postgres",
    "password": "postgres"
}

def wait_for_db():
    """Attendre que PostgreSQL soit prêt"""
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print("✅ Connexion à PostgreSQL établie")
            return True
        except psycopg2.OperationalError:
            retry_count += 1
            print(f"⏳ Tentative {retry_count}/{max_retries} - En attente de PostgreSQL...")
            time.sleep(2)
    
    print("❌ Impossible de se connecter à PostgreSQL")
    return False

def wait_for_redis():
    """Attendre que Redis soit prêt"""
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            r = redis.Redis(host='redis', port=6379)
            r.ping()
            print("✅ Connexion à Redis établie")
            return True
        except redis.ConnectionError:
            retry_count += 1
            print(f"⏳ Tentative {retry_count}/{max_retries} - En attente de Redis...")
            time.sleep(2)
    
    print("❌ Impossible de se connecter à Redis")
    return False

def init_database():
    """Initialiser la base de données et créer la table users"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Créer la table users si elle n'existe pas
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Vérifier si des utilisateurs existent
        cur.execute("SELECT COUNT(*) FROM users")
        count = cur.fetchone()[0]
        
        # Insérer des données de test si la table est vide
        if count == 0:
            print("📝 Insertion de données de test...")
            cur.execute("""
                INSERT INTO users (name, email) VALUES
                ('Alice Dupont', 'alice@example.com'),
                ('Bob Martin', 'bob@example.com'),
                ('Claire Dubois', 'claire@example.com')
            """)
            print("✅ Données de test insérées")
        
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Base de données initialisée")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation de la DB: {e}")
        return False

def get_db_connection():
    """Créer une nouvelle connexion PostgreSQL"""
    return psycopg2.connect(**DB_CONFIG)

def get_redis_connection():
    """Créer une nouvelle connexion Redis"""
    return redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/')
def index():
    try:
        # Connexion Redis
        cache = get_redis_connection()
        cache.incr('hits')
        hits = cache.get('hits')
        
        # Connexion PostgreSQL
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users;")
        users = cur.fetchall()
        cur.close()
        conn.close()
        
        # Formater les utilisateurs
        user_list = [
            {"id": user[0], "name": user[1], "email": user[2]} 
            for user in users
        ]
        
        return jsonify({
            "message": "Bienvenue FullStack App",
            "visits": hits,
            "users": user_list,
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "message": "Erreur",
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/health')
def health():
    """Endpoint de health check"""
    health_status = {
        "status": "healthy",
        "database": "unknown",
        "cache": "unknown"
    }
    
    # Vérifier PostgreSQL
    try:
        conn = get_db_connection()
        conn.close()
        health_status["database"] = "connected"
    except Exception as e:
        health_status["database"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Vérifier Redis
    try:
        cache = get_redis_connection()
        cache.ping()
        health_status["cache"] = "connected"
    except Exception as e:
        health_status["cache"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"
    
    status_code = 200 if health_status["status"] == "healthy" else 503
    return jsonify(health_status), status_code

if __name__ == '__main__':
    print("🚀 Démarrage de l'application Flask...")
    
    # Attendre que les services soient prêts
    if not wait_for_db():
        print("❌ Arrêt : PostgreSQL non disponible")
        sys.exit(1)
    
    if not wait_for_redis():
        print("❌ Arrêt : Redis non disponible")
        sys.exit(1)
    
    # Initialiser la base de données
    if not init_database():
        print("❌ Arrêt : Échec de l'initialisation de la DB")
        sys.exit(1)
    
    print("✅ Tous les services sont prêts")
    print("🌐 Application disponible sur http://localhost:5000")
    
    # Lancer l'application
    app.run(host='0.0.0.0', port=5000, debug=True)