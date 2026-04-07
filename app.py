from flask import Flask, render_template
from flask_moment import Moment
from datetime import date




año_actual = date.today().year
print(año_actual)


app = Flask(__name__)
moment = Moment(app)

 


@app.route('/')
def home():
    return render_template("base.html", year=año_actual)


@app.route('/index')
def index():
    return render_template("index.html", year=año_actual)


@app.route('/plants')
def plants():
    return render_template("plants.html", year=año_actual)


@app.route('/detail')
def plant_det():
    return render_template("plant_detail.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

