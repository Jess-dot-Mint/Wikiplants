import sqlite3
import os

db_path = 'instance/wikiplantas.db'

# Conectar a la BD existente
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Verificar si la tabla ya existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ingredientes'")
if not cursor.fetchone():
    cursor.execute('''
        CREATE TABLE ingredientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            planta_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            parte_planta TEXT,
            concentracion TEXT,
            vehiculo TEXT,
            propiedades TEXT,
            modo_uso TEXT,
            precauciones TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (planta_id) REFERENCES plantas (id) ON DELETE CASCADE
        )
    ''')
    print("Tabla 'ingredientes' creada exitosamente")
else:
    print("La tabla 'ingredientes' ya existe, no se hizo nada")

# Verificar que la tabla se creó
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ingredientes'")
if cursor.fetchone():
    print("Verificación: tabla 'ingredientes' presente en la BD")
    
    # Ver cuántas columnas tiene
    cursor.execute("PRAGMA table_info(ingredientes)")
    columnas = cursor.fetchall()
    print(f"📊 Columnas en ingredientes: {len(columnas)}")
else:
    print("Algo salió mal, la tabla no se creó")

conn.commit()
conn.close()
