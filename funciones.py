import csv

def materias_mayor_reprobacion(nombre_archivo):
    reprobaciones = {}

    with open(nombre_archivo, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            materia = fila['materia']
            calificacion = float(fila['calificacion'])  # convertir a número

            if calificacion < 6:
                # Si no existe la materia en el diccionario, se inicializa en 0
                reprobaciones[materia] = reprobaciones.get(materia, 0) + 1

    # Ordenar de mayor a menor reprobaciones
    # materias_ordenadas = sorted(reprobaciones.items(), key=lambda x: x[1], reverse=True)
    return sorted(reprobaciones.items(), key=lambda x: x[1], reverse=True)

    '''
    print("Materias con mayor índice de reprobación:")
    for materia, cantidad in materias_ordenadas:
        print(f"{materia}: {cantidad} reprobados")
    '''

def carreras_mayor_promedio(nombre_archivo):
    promedios = {}

    with open(nombre_archivo, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            carrera = fila['carrera']
            calificacion = float(fila['calificacion'])

            # Si la carrera no está en el diccionario, la inicializamos
            if carrera not in promedios:
                promedios[carrera] = {'suma': 0, 'count': 0}

            promedios[carrera]['suma'] += calificacion
            promedios[carrera]['count'] += 1

    # Calcular el promedio real de cada carrera
    resultados = {}
    for carrera, datos in promedios.items():
        promedio = datos['suma'] / datos['count']
        resultados[carrera] = promedio

    # Ordenar de mayor a menor promedio
    # carreras_ordenadas = sorted(resultados.items(), key=lambda x: x[1], reverse=True)
    return sorted(resultados.items(), key=lambda x: x[1], reverse=True)

    '''
    print("Carreras con mayor promedio:")
    for carrera, promedio in carreras_ordenadas:
        print(f"{carrera}: {promedio:.2f}")
    '''

def tendencias_por_semestre(nombre_archivo):
    tendencias = {}

    with open(nombre_archivo, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            semestre = int(fila['semestre'])
            calificacion = float(fila['calificacion'])

            if semestre not in tendencias:
                tendencias[semestre] = {'suma': 0, 'count': 0}

            tendencias[semestre]['suma'] += calificacion
            tendencias[semestre]['count'] += 1

    # Calcular promedios
    promedios_semestre = {}
    for semestre, datos in tendencias.items():
        promedio = datos['suma'] / datos['count']
        promedios_semestre[semestre] = promedio

    # Ordenar por semestre (menor a mayor)
    # semestres_ordenados = sorted(promedios_semestre.items())
    return sorted(promedios_semestre.items())

    '''
    print("Tendencias por semestre:")
    for semestre, promedio in semestres_ordenados:
        print(f"Semestre {semestre}: promedio {promedio:.2f}")

    # (Opcional) Detectar tendencia general
    if len(semestres_ordenados) > 1:
        primero = semestres_ordenados[0][1]
        ultimo = semestres_ordenados[-1][1]
        if ultimo > primero:
            print("Tendencia general: en aumento")
        elif ultimo < primero:
            print("Tendencia general: en descenso")
        else:
            print("Tendencia general: estable")
    '''

def riesgos_academicos(nombre_archivo):
    estudiantes = {}

    with open(nombre_archivo, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            id_estudiante = fila['id_estudiante']
            carrera = fila['carrera']
            calificacion = float(fila['calificacion'])

            if id_estudiante not in estudiantes:
                estudiantes[id_estudiante] = {'suma': 0, 'count': 0, 'carrera': carrera}

            estudiantes[id_estudiante]['suma'] += calificacion
            estudiantes[id_estudiante]['count'] += 1

    # Calcular promedios
    promedios = {}
    for id_estudiante, datos in estudiantes.items():
        promedio = datos['suma'] / datos['count']
        promedios[id_estudiante] = {
            'promedio': promedio,
            'carrera': datos['carrera']
        }

    # Filtrar los que están en riesgo
    riesgos = {id_: info for id_, info in promedios.items() if info['promedio'] < 6}

    # Ordenar de menor a mayor promedio
    # riesgos_ordenados = sorted(riesgos.items(), key=lambda x: x[1]['promedio'])
    return sorted(riesgos.items(), key=lambda x: x[1]['promedio'])

    '''
    print("Posibles riesgos académicos (promedio < 6):")
    if not riesgos_ordenados:
        print("No hay estudiantes en riesgo.")
    else:
        for id_estudiante, info in riesgos_ordenados:
            print(f"ID: {id_estudiante} | Carrera: {info['carrera']} | Promedio: {info['promedio']:.2f}")
    '''

# Imprimir resultados
'''
riesgos_academicos('datos_rendimiento_universidad.csv')
print("\n")
tendencias_por_semestre('datos_rendimiento_universidad.csv')
print("\n")
carreras_mayor_promedio('datos_rendimiento_universidad.csv')
print("\n")
materias_mayor_reprobacion('datos_rendimiento_universidad.csv')
'''