
from functools import wraps
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
#from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('auth.login'))  # o 'login' según tu ruta
        return f(*args, **kwargs)
    return decorated_function



@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Panel de login simple"""
    if request.method == 'POST':
        password = request.form.get('password')
        # Cambia esta contraseña por una que solo tú sepas
        if password == '123':
            session['logged_in'] = True
            return redirect(url_for('auth.admin'))
        else:
            return render_template('login.html', error='Contraseña incorrecta')
    return render_template('login.html')



@bp.route('/logout')
def logout():
    """Cerrar sesión"""
    session.pop('logged_in', None)
    return redirect(url_for('auth.login'))

@bp.route('/admin')
@login_required
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    
    """Panel de administración"""
    db = get_db()
    plantas = db.execute('SELECT * FROM plantas ORDER BY created_at DESC').fetchall()
    articulos = db.execute('SELECT * FROM articulos ORDER BY created_at DESC').fetchall()
    return render_template('admin.html', plantas=plantas, articulos=articulos)

@bp.route('/admin/planta/nueva', methods=['GET', 'POST'])
@login_required
def admin_planta_nueva():
    """Agregar nueva planta"""
    if request.method == 'POST':
      
        db = get_db()
        db.execute('''
            INSERT INTO plantas (
                nombre_comun, nombre_cientifico, familia,
                propiedades_medicinales, propiedades_cosmeticas,
                partes_usadas, formas_uso, contraindicaciones, historia, imagen_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.form.get('nombre_comun'),
            request.form.get('nombre_cientifico'),
            request.form.get('familia'),
            request.form.get('propiedades_medicinales'),
            request.form.get('propiedades_cosmeticas'),
            request.form.get('partes_usadas'),
            request.form.get('formas_uso'),
            request.form.get('contraindicaciones'),
            request.form.get('historia'),
            request.form.get('imagen_url')
        ))
        db.commit()
        return redirect(url_for('auth.admin'))
    
    
    return render_template('admin_plant_form.html', planta=None)





@bp.route('/admin/planta/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def admin_planta_editar(id):
    """Editar planta existente"""
    db = get_db()
    planta = db.execute('SELECT * FROM plantas WHERE id = ?', (id,)).fetchone()
    
    if not planta:
        return "Planta no encontrada", 404
    
    if request.method == 'POST':
        db.execute('''
            UPDATE plantas SET
                nombre_comun = ?, nombre_cientifico = ?, familia = ?,
                propiedades_medicinales = ?, propiedades_cosmeticas = ?,
                partes_usadas = ?, formas_uso = ?, contraindicaciones = ?, historia = ?, imagen_url = ?
            WHERE id = ?
        ''', (
            request.form.get('nombre_comun'),
            request.form.get('nombre_cientifico'),
            request.form.get('familia'),
            request.form.get('propiedades_medicinales'),
            request.form.get('propiedades_cosmeticas'),
            request.form.get('partes_usadas'),
            request.form.get('formas_uso'),
            request.form.get('contraindicaciones'),
            request.form.get('historia'),
            request.form.get('imagen_url'),
            id
        ))
        db.commit()
        return redirect(url_for('auth.admin'))
    
    return render_template('admin_plant_form.html', planta=planta)

@bp.route('/admin/planta/<int:id>/eliminar')
@login_required
def admin_planta_eliminar(id):
    """Eliminar planta"""
    db = get_db()
    db.execute('DELETE FROM plantas WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('auth.admin'))

@bp.route('/admin/articulo/nuevo', methods=['GET', 'POST'])
@login_required
def admin_articulo_nuevo():
    """Agregar nuevo artículo"""
    db = get_db()
    plantas = db.execute('SELECT id, nombre_comun FROM plantas ORDER BY nombre_comun').fetchall()
    
    if request.method == 'POST':
        db.execute('''
            INSERT INTO articulos (titulo, contenido, planta_id)
            VALUES (?, ?, ?)
        ''', (
            request.form.get('titulo'),
            request.form.get('contenido'),
            request.form.get('planta_id') or None
        ))
        db.commit()
        return redirect(url_for('auth.admin'))
    
    return render_template('admin_article_form.html', articulo=None, plantas=plantas)

@bp.route('/admin/articulo/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def admin_articulo_editar(id):
    """Editar artículo existente"""
    db = get_db()
    articulo = db.execute('SELECT * FROM articulos WHERE id = ?', (id,)).fetchone()
    plantas = db.execute('SELECT id, nombre_comun FROM plantas ORDER BY nombre_comun').fetchall()
    
    if not articulo:
        return "Artículo no encontrado", 404
    
    if request.method == 'POST':
        db.execute('''
            UPDATE articulos SET
                titulo = ?, contenido = ?, planta_id = ?
            WHERE id = ?
        ''', (
            request.form.get('titulo'),
            request.form.get('contenido'),
            request.form.get('planta_id') or None,
            id
        ))
        db.commit()
        return redirect(url_for('auth.admin'))
    
    return render_template('admin_article_form.html', articulo=articulo, plantas=plantas)

@bp.route('/admin/articulo/<int:id>/eliminar')
@login_required
def admin_articulo_eliminar(id):
    """Eliminar artículo"""
    db = get_db()
    db.execute('DELETE FROM articulos WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('auth.admin'))
