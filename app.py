from flask import Flask, render_template, request
from funciones import materias_mayor_reprobacion, carreras_mayor_promedio, tendencias_por_semestre, riesgos_academicos

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/home/juander/HabilidadesDirectivas/AnalisisDeDatos/code.html')

@app.route('/reprobacion')
def reprobacion():
    datos = materias_mayor_reprobacion('datos_rendimiento_universidad.csv')
    return {'materias': datos}

@app.route('/promedios')
def promedios():
    datos = carreras_mayor_promedio('datos_rendimiento_universidad.csv')
    return {'carreras': datos}

@app.route('/tendencias')
def tendencias():
    datos = tendencias_por_semestre('datos_rendimiento_universidad.csv')
    return {'tendencias': datos}

@app.route('/riesgos')
def riesgos():
    datos = riesgos_academicos('datos_rendimiento_universidad.csv')
    return {'riesgos': datos}

if __name__ == '__main__':
    app.run(debug=True)