from flask import Flask, render_template, jsonify, request
import csv

app = Flask(__name__)

NOMBRE_ARCHIVO = 'datos_rendimiento_universidad.csv'

def procesar_csv(carrera_filtro=None, año_filtro=None):
    """Función principal que procesa el CSV y devuelve todos los datos"""
    materias = {}
    carreras = {}
    estudiantes = {}
    total_calif = 0
    suma_calif = 0
    reprobados = 0
    
    try:
        with open(NOMBRE_ARCHIVO, newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                # Aplicar filtros
                if carrera_filtro and carrera_filtro != 'Todas' and fila['carrera'] != carrera_filtro:
                    continue
                if año_filtro and fila['año'] != año_filtro:
                    continue
                
                # Obtener datos
                materia = fila['materia']
                carrera = fila['carrera']
                id_est = fila['id_estudiante']
                calif = float(fila['calificacion'])
                
                # Métricas generales
                total_calif += 1
                suma_calif += calif
                if calif < 6:
                    reprobados += 1
                
                # Materias (reprobación)
                if materia not in materias:
                    materias[materia] = {'total': 0, 'reprobados': 0}
                materias[materia]['total'] += 1
                if calif < 6:
                    materias[materia]['reprobados'] += 1
                
                # Carreras (promedio)
                if carrera not in carreras:
                    carreras[carrera] = {'suma': 0, 'count': 0}
                carreras[carrera]['suma'] += calif
                carreras[carrera]['count'] += 1
                
                # Estudiantes (riesgo)
                if id_est not in estudiantes:
                    estudiantes[id_est] = {
                        'suma': 0,
                        'count': 0,
                        'carrera': carrera,
                        'materias': []
                    }
                estudiantes[id_est]['suma'] += calif
                estudiantes[id_est]['count'] += 1
                estudiantes[id_est]['materias'].append({
                    'nombre': materia,
                    'calificacion': calif
                })
    
    except Exception as e:
        print(f"Error: {e}")
        return None
    
    # Calcular resultados
    resultado = {
        'metricas': {
            'promedio_general': round(suma_calif / total_calif if total_calif > 0 else 0, 2),
            'tasa_reprobacion': round((reprobados / total_calif * 100) if total_calif > 0 else 0, 1),
            'estudiantes_riesgo': 0,
            'materia_mayor_reprobacion': 'N/A',
            'porcentaje_materia_mayor': 0
        },
        'materias': [],
        'carreras': [],
        'riesgos': []
    }
    
    # Materias con mayor reprobación
    materias_list = []
    for m, d in materias.items():
        porcentaje = (d['reprobados'] / d['total'] * 100) if d['total'] > 0 else 0
        materias_list.append((m, round(porcentaje, 1)))
    
    resultado['materias'] = sorted(materias_list, key=lambda x: x[1], reverse=True)
    
    if resultado['materias']:
        resultado['metricas']['materia_mayor_reprobacion'] = resultado['materias'][0][0]
        resultado['metricas']['porcentaje_materia_mayor'] = resultado['materias'][0][1]
    
    # Carreras con mayor promedio
    carreras_list = []
    for c, d in carreras.items():
        promedio = d['suma'] / d['count'] if d['count'] > 0 else 0
        carreras_list.append((c, round(promedio, 1)))
    
    resultado['carreras'] = sorted(carreras_list, key=lambda x: x[1], reverse=True)
    
    # Estudiantes en riesgo
    riesgos_list = []
    for id_est, d in estudiantes.items():
        promedio = d['suma'] / d['count'] if d['count'] > 0 else 0
        if promedio < 6:
            peor_materia = min(d['materias'], key=lambda x: x['calificacion'])
            riesgos_list.append({
                'id': id_est,
                'carrera': d['carrera'],
                'promedio': round(promedio, 1),
                'peor_materia': peor_materia['nombre'],
                'calificacion_peor': round(peor_materia['calificacion'], 1)
            })
    
    resultado['riesgos'] = sorted(riesgos_list, key=lambda x: x['promedio'])
    resultado['metricas']['estudiantes_riesgo'] = len(resultado['riesgos'])
    
    return resultado

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/datos')
def api_datos():
    carrera = request.args.get('carrera', 'Todas')
    año = request.args.get('año', '2024')
    
    print(f"\n📊 Solicitando datos para: Carrera={carrera}, Año={año}")
    
    datos = procesar_csv(carrera, año)
    
    if datos:
        print(f"✅ Datos encontrados:")
        print(f"   - Materias: {len(datos['materias'])}")
        print(f"   - Carreras: {len(datos['carreras'])}")
        print(f"   - Riesgos: {len(datos['riesgos'])}")
        return jsonify(datos)
    else:
        print(f"❌ Error procesando CSV")
        return jsonify({'error': 'No se pudieron procesar los datos'}), 500

if __name__ == '__main__':
    app.run(debug=True)