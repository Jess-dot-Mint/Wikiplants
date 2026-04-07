from flask import Blueprint, render_template, request
from datetime import date
from .db import get_db


año_actual = date.today().year


bp = Blueprint('views', __name__, url_prefix='/views')

@bp.route('/')
def home():
    return render_template("index.html", year=año_actual)

@bp.route('/plants')
def plants():
    return render_template("plants.html", year=año_actual)

@bp.route('/plant/<int:id>')
def plant_detail(id):
    db = get_db()
    planta = db.execute('SELECT * FROM plantas WHERE id = ?', (id,)).fetchone()
    if not planta:
        return "Planta no encontrada", 404
    relacionados = db.execute(
        'SELECT * FROM articulos WHERE planta_id = ? OR contenido LIKE ? LIMIT 5',
        (id, f'%{planta["nombre_comun"]}%')
    ).fetchall()
    return render_template('plant_detail.html', planta=planta, articulos_relacionados=relacionados)



@bp.route('/buscar')
def buscar():
    query = request.args.get('q', '').strip()
    filtro = request.args.get('filtro', '')
    db = get_db()
    if query:
        plantas = db.execute(
            "SELECT * FROM plantas WHERE nombre_comun LIKE ? OR nombre_cientifico LIKE ?",
            (f'%{query}%', f'%{query}%')
        ).fetchall()
        if filtro == 'medicinal':
            plantas = [p for p in plantas if p['propiedades_medicinales'] and p['propiedades_medicinales'].strip()]
        elif filtro == 'cosmetico':
            plantas = [p for p in plantas if p['propiedades_cosmeticas'] and p['propiedades_cosmeticas'].strip()]
        elif filtro == 'ambos':
            plantas = [p for p in plantas if p['propiedades_medicinales'] and p['propiedades_cosmeticas']]
    else:
        plantas = []
    return render_template('plants.html', plantas=plantas, busqueda=query, filtro_activo=filtro)


@bp.route('/articulo/<int:id>')
def articulo_detalle(id):
    db = get_db()
    articulo = db.execute('SELECT * FROM articulos WHERE id = ?', (id,)).fetchone()
    if not articulo:
        return "Artículo no encontrado", 404
    planta = None
    if articulo['planta_id']:
        planta = db.execute('SELECT * FROM plantas WHERE id = ?', (articulo['planta_id'],)).fetchone()
    return render_template('article_detalle.html', articulo=articulo, planta=planta)




"""
@bp.route('/detail')
def plant_det():
    return render_template("plant_detail.html")

"""

@bp.route('/blog')
def blog():
    return render_template("blog.html")

