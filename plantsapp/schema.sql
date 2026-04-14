
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;


-- Tabla de plantas
CREATE TABLE plantas (
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
);

-- Tabla de artículos del blog
CREATE TABLE articulos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    contenido TEXT NOT NULL,
    planta_id INTEGER, -- opcional: si el artículo habla de una planta específica
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (planta_id) REFERENCES plantas (id)
);

-- Tabla de comentarios 
CREATE TABLE comentarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    articulo_id INTEGER,
    autor TEXT,
    contenido TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (articulo_id) REFERENCES articulos (id)
);



-- Tabla ingredientes:


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
);