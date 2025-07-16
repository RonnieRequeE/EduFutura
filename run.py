from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'edufutura_secret_key'


@app.route('/')
def home():
    usuario = session.get('usuario')
    return render_template('home.html', usuario=usuario)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == 'test@edufutura.com' and password == '123':
            session['usuario'] = email
            return redirect('/')
        else:
            return 'Credenciales incorrectas'
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        # Aquí puedes agregar validaciones básicas
        print("Nuevo usuario:", nombre, email)

        return redirect('/login')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')

@app.route('/panel')
def panel():
    if 'usuario' in session:
        return render_template('panel.html', usuario=session['usuario'])
    else:
        return redirect('/login')


@app.route('/curso/<int:id>')
def curso(id):
    if 'usuario' in session:
        cursos = {
            1: {
                "titulo": "Programación en Python",
                "descripcion": "Desde lo básico hasta lo avanzado. Aprende estructuras, funciones, y proyectos reales.",
                "modulos": ["Variables y Tipos", "Condicionales", "Funciones", "Manejo de archivos"]
            },
            2: {
                "titulo": "Diseño UX para Plataformas Educativas",
                "descripcion": "Conoce los principios de diseño intuitivo, accesibilidad, y usabilidad educativa.",
                "modulos": ["Principios UX", "Gamificación", "Diseño responsivo", "Testing con usuarios"]
            }
        }
        curso = cursos.get(id)
        if curso:
            # 🔢 Simulación de notas por módulo (esto luego será dinámico)
            notas = [85, 90, 75]
            promedio = round(sum(notas) / len(notas), 2)
            estado = "Aprobado ✅" if promedio >= 70 else "No aprobado ❌"

            return render_template("curso.html",
                       curso=curso,
                       usuario=session['usuario'],
                       promedio=promedio,
                       estado=estado,
                       id=id)  # 👈 Aquí agregas esto

        else:
            return "Curso no encontrado", 404
    else:
        return redirect('/login')

@app.route('/curso/<int:id>/quiz', methods=['POST'])
def quiz(id):
    if 'usuario' not in session:
        return redirect('/login')

    respuesta = request.form.get('respuesta')
    correcta = 'bucle'  # respuesta esperada
    resultado = 'correcta 🎉' if respuesta == correcta else 'incorrecta ❌'

    cursos = {
        1: {
            "titulo": "Programación en Python",
            "descripcion": "Desde lo básico hasta lo avanzado. Aprende estructuras, funciones, y proyectos reales.",
            "modulos": ["Variables y Tipos", "Condicionales", "Funciones", "Manejo de archivos"]
        },
        2: {
            "titulo": "Diseño UX para Plataformas Educativas",
            "descripcion": "Conoce los principios de diseño intuitivo, accesibilidad, y usabilidad educativa.",
            "modulos": ["Principios UX", "Gamificación", "Diseño responsivo", "Testing con usuarios"]
        }
    }

    curso = cursos.get(id)
    if not curso:
        return "Curso no encontrado", 404

    # Simulación de notas
    notas = [85, 90, 75]
    promedio = round(sum(notas) / len(notas), 2)
    estado = "Aprobado ✅" if promedio >= 70 else "No aprobado ❌"

    return render_template("curso.html", curso=curso, usuario=session['usuario'],
                           promedio=promedio, estado=estado, resultado=resultado, id=id)

@app.route('/curso/<int:id>/evaluacion', methods=['GET', 'POST'])
def evaluacion(id):
    if 'usuario' not in session:
        return redirect('/login')

    cursos = {
        1: {
            "titulo": "Programación en Python",
        },
        2: {
            "titulo": "Diseño UX para Plataformas Educativas",
        }
    }
    curso = cursos.get(id)
    if not curso:
        return "Curso no encontrado", 404

    resultado = None
    if request.method == 'POST':
        respuesta = request.form.get('respuesta')
        correcta = 'bucle'
        resultado = '¡Correcta! 🎉' if respuesta == correcta else 'Incorrecta ❌'

    return render_template("evaluacion.html", curso=curso, usuario=session['usuario'], resultado=resultado, id=id)


if __name__ == '__main__':
    app.run(debug=True)

