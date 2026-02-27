from flask import Flask, render_template
from funciones import (
    materias_mayor_reprobacion,
    carreras_mayor_promedio,
    tendencias_por_semestre,
    riesgos_academicos
)

app = Flask(__name__)

@app.route('/')
def dashboard():
    archivo = 'datos_rendimiento_universidad.csv'

    # Obtener datos desde tus funciones
    materias = materias_mayor_reprobacion(archivo)
    carreras = carreras_mayor_promedio(archivo)
    tendencias = tendencias_por_semestre(archivo)
    riesgos = riesgos_academicos(archivo)

    # Enviar datos al HTML
    return render_template(
        'code.html',
        materias=materias,
        carreras=carreras,
        tendencias=tendencias,
        riesgos=riesgos
    )

if __name__ == '__main__':
    app.run(debug=True)