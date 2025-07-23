from flask import Flask, render_template, request, redirect, session, flash
from flask import get_flashed_messages

app = Flask(__name__)
app.secret_key = 'edufutura_secret_key'

# 🔐 Simulación de usuarios con roles
usuarios = {
    'docente@edufutura.com': {'rol': 'docente', 'nombre': 'Prof. Juan'},
    'ana@edufutura.com': {'rol': 'docente', 'nombre': 'Prof. Ana'},
    'mario@edufutura.com': {'rol': 'docente', 'nombre': 'Prof. Mario'},
    'estudiante@edufutura.com': {'rol': 'estudiante', 'nombre': 'Ronnie'},
    'luis@edufutura.com': {'rol': 'estudiante', 'nombre': 'Luis'},
    'carla@edufutura.com': {'rol': 'estudiante', 'nombre': 'Carla'},
    'admin@edufutura.com': {'rol': 'admin', 'nombre': 'Administrador Principal'}    
}

modulos_por_materia = {}

# 📘 Simulación de materias creadas por el administrador
materias = {
    1: {'nombre': 'Programación en Python'},
    2: {'nombre': 'Diseño UX para Plataformas Educativas'}
}

# 👨‍🏫 Asignación de docentes a materias
asignaciones_docentes = {
    1: 'docente@edufutura.com',  # Python → Prof. Juan
    2: 'docente@edufutura.com'   # UX → Prof. Juan
}

# 👨‍🎓 Asignación de estudiantes a materias con docente específico
asignaciones_estudiantes = {
    'estudiante@edufutura.com': [1]  # Ronnie está en Python con Prof. Juan
}

# 📋 Lista de docentes disponibles
docentes_disponibles = [
    'docente@edufutura.com',
    'ana@edufutura.com',
    'mario@edufutura.com'
]

estudiantes_disponibles = [
    'estudiante@edufutura.com',
    'luis@edufutura.com',
    'carla@edufutura.com'
]

@app.route('/')
def home():
    usuario = session.get('usuario')
    rol = session.get('rol')
    return render_template('home.html', usuario=usuario, rol=rol)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in usuarios and password == '123':
            session['usuario'] = email
            session['rol'] = usuarios[email]['rol']
            return redirect('/panel')
        else:
            return 'Credenciales incorrectas'
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        print("Nuevo usuario:", nombre, email)
        return redirect('/login')
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/panel')
def panel():
    if 'usuario' not in session:
        return redirect('/login')

    usuario = session['usuario']
    rol = session['rol']

    if rol == 'docente':
        # Mostrar materias asignadas al docente
        materias_docente = [id for id, correo in asignaciones_docentes.items() if correo == usuario]
        lista_materias = {id: materias[id] for id in materias_docente}
        return render_template('panel_docente.html',
                       usuario=usuario,
                       materias=lista_materias,
                       asignaciones_estudiantes=asignaciones_estudiantes)

    elif rol == 'estudiante':
        # Mostrar materias asignadas al estudiante
        materias_estudiante = asignaciones_estudiantes.get(usuario, [])
        lista_materias = {id: materias[id] for id in materias_estudiante}
        return render_template('panel_estudiante.html', usuario=usuario, materias=lista_materias)

    elif rol == 'admin':
        return redirect('/admin')
    else:
        return "Rol no reconocido", 403


@app.route('/admin')
def admin_panel():
    if 'usuario' in session and session.get('rol') == 'admin':
        print(get_flashed_messages())
        return render_template('panel_admin.html',
                       usuario=session['usuario'],
                       materias=materias,
                       asignaciones_docentes=asignaciones_docentes,
                       docentes_disponibles=docentes_disponibles,
                       estudiantes_disponibles=estudiantes_disponibles,
                       asignaciones_estudiantes=asignaciones_estudiantes)
    else:
        return "Acceso restringido", 403

@app.route('/asignar_docente', methods=['POST'])
def asignar_docente():
    if 'usuario' in session and session.get('rol') == 'admin':
        materia_id = int(request.form.get('materia_id'))
        correo = request.form.get('correo_docente')

        if correo in usuarios and usuarios[correo]['rol'] == 'docente':
            asignaciones_docentes[materia_id] = correo
            flash('✅ Docente asignado correctamente')

        return redirect('/admin')
    else:
        return "Acceso restringido", 403

@app.route('/crear_materia', methods=['POST'])
def crear_materia():
    if 'usuario' in session and session.get('rol') == 'admin':
        nombre = request.form.get('nombre_materia')

        if nombre:
            nuevo_id = max(materias.keys()) + 1 if materias else 1
            materias[nuevo_id] = {'nombre': nombre}
            print("Materia creada:", nombre)
        return redirect('/admin')
    else:
        return "Acceso restringido", 403

@app.route('/asignar_estudiantes', methods=['POST'])
def asignar_estudiantes():
    if 'usuario' in session and session.get('rol') == 'admin':
        materia_id = int(request.form.get('materia_id'))
        correo = request.form.get('correo_estudiante')

        if correo in usuarios and usuarios[correo]['rol'] == 'estudiante':
            if correo not in asignaciones_estudiantes:
                asignaciones_estudiantes[correo] = []
            if materia_id not in asignaciones_estudiantes[correo]:
                asignaciones_estudiantes[correo].append(materia_id)
                flash('✅ Estudiante asignado correctamente')
            else:
                flash('⚠️ El estudiante ya está asignado a esta materia')

        return redirect('/admin')
    else:
        return "Acceso restringido", 403


@app.route('/curso/<int:id>')
def curso(id):
    global modulos_por_materia

    if 'usuario' not in session:
        return redirect('/login')

    usuario = session['usuario']
    rol = session['rol']

    curso = materias.get(id)
    if not curso:
        return "Curso no encontrado", 404

    modulos = modulos_por_materia.get(id, [])
    curso['modulos'] = modulos

    notas = [85, 90, 75]
    promedio = round(sum(notas) / len(notas), 2)
    estado = "Aprobado ✅" if promedio >= 70 else "No aprobado ❌"

    return render_template("curso.html",
                           curso=curso,
                           usuario=usuario,
                           modulos=modulos,
                           promedio=promedio,
                           estado=estado,
                           id=id)



@app.route('/curso/<int:id>/evaluacion', methods=['GET', 'POST'])
def evaluacion(id):
    if 'usuario' not in session:
        return redirect('/login')

    curso = materias.get(id)
    if not curso:
        return "Curso no encontrado", 404

    resultado = None
    if request.method == 'POST':
        respuesta = request.form.get('respuesta')
        correcta = 'bucle'
        resultado = '¡Correcta! 🎉' if respuesta == correcta else 'Incorrecta ❌'

    return render_template("evaluacion.html",
                           curso=curso,
                           usuario=session['usuario'],
                           resultado=resultado,
                           id=id)


@app.route('/curso/<int:id>/quiz', methods=['POST'])
def quiz(id):
    if 'usuario' not in session:
        return redirect('/login')

    respuesta = request.form.get('respuesta')
    correcta = 'bucle'
    resultado = 'correcta 🎉' if respuesta == correcta else 'incorrecta ❌'

    curso = materias.get(id)
    if not curso:
        return "Curso no encontrado", 404

    modulos_por_materia = {
        1: ["Variables y Tipos", "Condicionales", "Funciones", "Manejo de archivos"],
        2: ["Principios UX", "Gamificación", "Diseño responsivo", "Testing con usuarios"]
    }

    modulos = modulos_por_materia.get(id, [])
    notas = [85, 90, 75]
    promedio = round(sum(notas) / len(notas), 2)
    estado = "Aprobado ✅" if promedio >= 70 else "No aprobado ❌"

    return render_template("curso.html",
                           curso=curso,
                           usuario=session['usuario'],
                           modulos=modulos,
                           promedio=promedio,
                           estado=estado,
                           resultado=resultado,
                           id=id)

@app.route('/quitar_estudiante', methods=['POST'])
def quitar_estudiante():
    if 'usuario' in session and session.get('rol') == 'admin':
        materia_id = int(request.form.get('materia_id'))
        correo = request.form.get('correo_estudiante')

        if correo in asignaciones_estudiantes and materia_id in asignaciones_estudiantes[correo]:
            asignaciones_estudiantes[correo].remove(materia_id)
            flash('🗑️ Estudiante quitado correctamente')

        return redirect('/admin')
    else:
        return "Acceso restringido", 403

@app.route('/eliminar_materia', methods=['POST'])
def eliminar_materia():
    if 'usuario' in session and session.get('rol') == 'admin':
        materia_id = int(request.form.get('materia_id'))
        if materia_id in materias:
            materias.pop(materia_id)
            asignaciones_docentes.pop(materia_id, None)
            for estudiante in asignaciones_estudiantes:
                if materia_id in asignaciones_estudiantes[estudiante]:
                    asignaciones_estudiantes[estudiante].remove(materia_id)
            flash('🗑️ Materia eliminada correctamente')
        return redirect('/admin')
    else:
        return "Acceso restringido", 403

def generar_id_modulo():
    from random import randint
    return randint(100000, 999999)

def buscar_modulo_por_id(modulo_id):
    for materia_id, lista_modulos in modulos_por_materia.items():
        for modulo in lista_modulos:
            if modulo['id'] == modulo_id:
                return modulo
    return None

def agregar_modulo_a_materia(materia_id, modulo):
    if materia_id in modulos_por_materia:
        modulos_por_materia[materia_id].append(modulo)
    else:
        modulos_por_materia[materia_id] = [modulo]

@app.route('/crear_modulo/<int:materia_id>')
def crear_modulo(materia_id):
    if 'usuario' not in session or session.get('rol') != 'docente':
        return "Acceso no autorizado", 403
    return render_template('crear_modulo.html', materia_id=materia_id, editar=False)

@app.route('/editar_modulo/<int:modulo_id>')
def editar_modulo(modulo_id):
    if 'usuario' not in session or session.get('rol') != 'docente':
        return "Acceso no autorizado", 403

    modulo = buscar_modulo_por_id(modulo_id)

    if modulo is None:
        return "⚠️ Módulo no encontrado", 404

    materia_id = modulo['materia_id']
    return render_template('crear_modulo.html', materia_id=materia_id, modulo=modulo, editar=True)

@app.route('/guardar_modulo', methods=['POST'])
def guardar_modulo():
    materia_id = int(request.form['materia_id'])
    nuevo_modulo = {
        'id': generar_id_modulo(),
        'titulo': request.form['titulo'],
        'descripcion': request.form.get('descripcion', ''),
        'recurso': request.form.get('recurso', ''),
        'inicio': request.form.get('inicio'),
        'cierre': request.form.get('cierre'),
        'etiquetas': request.form.getlist('etiquetas'),
        'materia_id': materia_id
    }
    agregar_modulo_a_materia(materia_id, nuevo_modulo)
    return redirect(f'/curso/{materia_id}')

@app.route('/actualizar_modulo', methods=['POST'])
def actualizar_modulo():
    modulo_id = int(request.form['modulo_id'])
    modulo = buscar_modulo_por_id(modulo_id)
    modulo['titulo'] = request.form['titulo']
    modulo['descripcion'] = request.form.get('descripcion', '')
    modulo['recurso'] = request.form.get('recurso', '')
    modulo['inicio'] = request.form.get('inicio')
    modulo['cierre'] = request.form.get('cierre')
    modulo['etiquetas'] = request.form.getlist('etiquetas')
    return redirect(f"/curso/{modulo['materia_id']}")

@app.route('/eliminar_modulo', methods=['POST'])
def eliminar_modulo():
    if 'usuario' not in session or session.get('rol') != 'docente':
        return "Acceso no autorizado", 403

    modulo_id = int(request.form['modulo_id'])

    # Buscar y eliminar el módulo en el diccionario
    for materia_id, lista_modulos in modulos_por_materia.items():
        nuevos_modulos = [m for m in lista_modulos if m['id'] != modulo_id]
        if len(nuevos_modulos) < len(lista_modulos):  # si se eliminó
            modulos_por_materia[materia_id] = nuevos_modulos
            return redirect(f"/curso/{materia_id}")

    return "Módulo no encontrado", 404

@app.route('/crear_evaluacion', methods=['POST'])
def crear_evaluacion():
    if 'usuario' not in session or session.get('rol') != 'docente':
        return "Acceso no autorizado", 403

    materia_id = int(request.form['materia_id'])
    modulo_id = int(request.form['modulo_id'])

    nueva_evaluacion = {
        'id': generar_id_modulo(),  # Usamos el mismo generador temporal
        'titulo': request.form['titulo_evaluacion'],
        'descripcion': request.form.get('descripcion_evaluacion', ''),
        'tipo': request.form.get('tipo_evaluacion', 'quiz'),
        'inicio': request.form.get('inicio_evaluacion'),
        'cierre': request.form.get('cierre_evaluacion'),
        'calificada': False,
        'nota': None,
        'modulo': modulo_id,
        'materia_id': materia_id,
        'estado': 'pendiente'
    }

    # Podés guardar esta evaluación como parte de un diccionario por materia y módulo
    if 'evaluaciones' not in session:
        session['evaluaciones'] = {}

    clave = f"{materia_id}_{modulo_id}"
    evaluaciones = session['evaluaciones'].get(clave, [])
    evaluaciones.append(nueva_evaluacion)
    session['evaluaciones'][clave] = evaluaciones

    flash('✅ Evaluación creada correctamente')
    return redirect(f'/curso/{materia_id}')

if __name__ == '__main__':
    app.run(debug=True)
