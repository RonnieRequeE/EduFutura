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
        return f"Panel privado de EduFutura — Usuario activo: {session['usuario']}"
    else:
        return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)

