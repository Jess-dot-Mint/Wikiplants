
@app.route('/')
def index():
    """Página de inicio"""
    db = get_db()
    
    # Obtener últimas 6 plantas agregadas
    plantas = db.execute('SELECT * FROM plantas ORDER BY created_at DESC LIMIT 6').fetchall()
    
    # Obtener últimos 3 artículos del blog
    articulos = db.execute('SELECT * FROM articulos ORDER BY created_at DESC LIMIT 3').fetchall()
    
    return render_template('index.html', plantas=plantas, articulos=articulos, current_time=datetime.utcnow())

@app.route('/plantas')
def plantas_lista():
    """Listado de todas las plantas"""
    db = get_db()
    plantas = db.execute('SELECT * FROM plantas ORDER BY nombre_comun').fetchall()
    return render_template('plantas.html', plantas=plantas)

@app.route('/planta/<int:id>')
def planta_detalle(id):
    """Ficha detallada de una planta"""
    db = get_db()
    planta = db.execute('SELECT * FROM plantas WHERE id = ?', (id,)).fetchone()
    
    if not planta:
        return "Planta no encontrada", 404
    
    # Buscar artículos relacionados con esta planta
    articulos_relacionados = db.execute(
        'SELECT * FROM articulos WHERE planta_id = ? OR contenido LIKE ? ORDER BY created_at DESC LIMIT 5',
        (id, f'%{planta["nombre_comun"]}%')
    ).fetchall()
    
    return render_template('planta_detalle.html', planta=planta, articulos_relacionados=articulos_relacionados)

@app.route('/buscar')
def buscar():
    """Búsqueda de plantas"""
    query = request.args.get('q', '').strip()
    filtro = request.args.get('filtro', '')  # medicinal, cosmetico, ambos
    
    db = get_db()
    
    if query:
        # Búsqueda por nombre común o científico
        plantas = db.execute(
            "SELECT * FROM plantas WHERE nombre_comun LIKE ? OR nombre_cientifico LIKE ?",
            (f'%{query}%', f'%{query}%')
        ).fetchall()
        
        # Si hay filtro adicional, filtrar en Python (más simple por ahora)
        if filtro == 'medicinal':
            plantas = [p for p in plantas if p['propiedades_medicinales'] and p['propiedades_medicinales'].strip()]
        elif filtro == 'cosmetico':
            plantas = [p for p in plantas if p['propiedades_cosmeticas'] and p['propiedades_cosmeticas'].strip()]
        elif filtro == 'ambos':
            plantas = [p for p in plantas if p['propiedades_medicinales'] and p['propiedades_cosmeticas']]
    else:
        plantas = []
    
    return render_template('plantas.html', plantas=plantas, busqueda=query, filtro_activo=filtro)

@app.route('/blog')
def blog():
    """Listado de artículos del blog"""
    db = get_db()
    articulos = db.execute('SELECT * FROM articulos ORDER BY created_at DESC').fetchall()
    return render_template('blog.html', articulos=articulos)

@app.route('/articulo/<int:id>')
def articulo_detalle(id):
    """Detalle de un artículo del blog"""
    db = get_db()
    articulo = db.execute('SELECT * FROM articulos WHERE id = ?', (id,)).fetchone()
    
    if not articulo:
        return "Artículo no encontrado", 404
    
    # Obtener planta relacionada si existe
    planta = None
    if articulo['planta_id']:
        planta = db.execute('SELECT * FROM plantas WHERE id = ?', (articulo['planta_id'],)).fetchone()
    
    return render_template('articulo_detalle.html', articulo=articulo, planta=planta)
