from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Simulación de usuarios y sus roles (estándar o premium)
usuarios = {
    'usuario_estandar': {'contraseña': 'contraseña_estandar', 'rol': 'estandar'},
    'usuario_premium': {'contraseña': 'contraseña_premium', 'rol': 'premium'}
}

@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    usuario = request.form['username']
    contraseña = request.form['password']

    # Verifica si el usuario y la contraseña coinciden
    if usuario in usuarios and usuarios[usuario]['contraseña'] == contraseña:
        # Establece el rol del usuario en la sesión
        session['rol'] = usuarios[usuario]['rol']
        # Redirige al usuario a la página correspondiente según su rol
        return redirect(url_for('inicio' if session['rol'] == 'estandar' else 'premium'))
    else:
        # Si las credenciales son incorrectas, redirige al usuario de vuelta al formulario de inicio de sesión
        return redirect(url_for('formulario_inicio_sesion'))

@app.route('/')
def formulario_inicio_sesion():
    return 'Formulario de inicio de sesión aquí'

@app.route('/inicio')
def inicio():
    return 'Página de inicio para usuarios estándar'

@app.route('/premium')
def premium():
    return 'Página de inicio para usuarios premium'

if __name__ == '__main__':
    app.run(debug=True)
