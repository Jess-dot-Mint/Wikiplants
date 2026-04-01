from flask import Flask, render_template, request, redirect, url_for, session
from flask_moment import Moment
from datetime import datetime
import sqlite3
import os
from functools import wraps
from plants_db import get_db

app = Flask(__name__)
moment= Moment(app)

# Configuración de la base de datosç
# En config
#DATABASE = os.path.join(app.instance_path, 'wikiplantas.db')

"""
def get_db():
    #Conecta a la base de datos
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
    return conn
"""
    

""" En schema
def init_db():
    #Crea las tablas si no existen
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Tabla de plantas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plantas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_comun TEXT NOT NULL,
                nombre_cientifico TEXT,
                familia TEXT,
                propiedades_medicinales TEXT,
                propiedades_cosmeticas TEXT,
                partes_usadas TEXT,
                formas_uso TEXT,
                contraindicaciones TEXT,
                historia TEXT,
                imagen_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de artículos del blog
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articulos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                contenido TEXT NOT NULL,
                planta_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (planta_id) REFERENCES plantas (id)
            )
        ''')
        
        db.commit()
        print("✅ Base de datos inicializada correctamente")
"""

""" LOGIN


# Decorador para proteger rutas de admin (simple pero efectivo)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
"""
# ==================== RUTAS PRINCIPALES ====================

@app.route('/')
def base():
    """Página de inicio"""
  
    return render_template('index.html')



# ==================== INICIALIZACIÓN ====================
"""
if __name__ == '__main__':
    # Crear la carpeta instance si no existe
    os.makedirs(app.instance_path, e∫xist_ok=True)
    # Inicializar la base de datos
    init_db()
    # Ejecutar la aplicación
    app.run(debug=True)
    """