from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, current_user, logout_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '7af32be7f2f18aa5046c6c3d068427dd7d95b4e5d3242725'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

jsnfile = 'data.json'


# Clase Película para almacenar datos de películas
class Pelicula:
    def __init__(self, titulo, resumen, caratula, categoria, precio_alquiler):
        self.titulo = titulo
        self.resumen = resumen
        self.caratula = caratula
        self.precio_alquiler = precio_alquiler
        self.categoria = categoria

    def to_dict(self):
        return {
            'titulo': self.titulo,
            'resumen': self.resumen,
            'caratula': self.caratula,
            'categoria': self.categoria,
            'precio_alquiler': self.precio_alquiler
        }

# Cargar datos de películas desde data.json
def cargar_peliculas():
    # Verificar si el archivo JSON existe
    if not os.path.exists(jsnfile):
        # Archivo no encontrado, crear el archivo con datos iniciales
        datos_iniciales = [
            {
                "titulo": "Star Wars",
                "resumen": "En una galaxia muy, muy lejana...",
                "caratula": "static/img/star_wars.jpg",
                "categoria": "ciencia_ficcion",
                "precio_alquiler": 5.99
            },
            {
                "titulo": "Jurassic Park",
                "resumen": "Un parque temático con dinosaurios...",
                "caratula": "static/img/jurassic_park.jpg",
                "categoria": "aventura",
                "precio_alquiler": 4.99
            },
            {
                "titulo": "Titanic",
                "resumen": "Un romance épico en alta mar...",
                "caratula": "static/img/titanic.jpg",
                "categoria": "romance",
                "precio_alquiler": 6.99
            }
]

        # Escribir los datos iniciales en el archivo JSON
        with open(jsnfile, 'w') as file:
            json.dump(datos_iniciales, file, indent=4)

        return []  # Devolver lista vacía si se crea el archivo por primera vez

    # El archivo JSON existe, cargar las películas
    with open(jsnfile, 'r') as json_file:
        peliculas_data = json.load(json_file)
        peliculas = []
        for pelicula_data in peliculas_data:
            pelicula = Pelicula(**pelicula_data)
            peliculas.append(pelicula)
        return peliculas

# Ejemplo de uso
peliculas = cargar_peliculas()
print(peliculas)

# Guardar datos de películas en data.json
def guardar_peliculas(peliculas):
    peliculas_data = [pelicula.to_dict() for pelicula in peliculas]
    with open(jsnfile, 'w') as json_file:
        json.dump(peliculas_data, json_file, indent=4)

# Formulario para agregar una nueva película
class NuevaPeliculaForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    resumen = StringField('Resumen', validators=[DataRequired()])
    caratula = StringField('URL de Carátula', validators=[DataRequired()])
    precio_alquiler = StringField('Precio de Alquiler', validators=[DataRequired()])
    categoria = StringField('Categoría', validators=[DataRequired()])
    inventario = StringField('Inventario', validators=[DataRequired()])
    submit = SubmitField('Agregar')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('manager', 'Manager'), ('cliente', 'Cliente')], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose a different one.')
        
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'manager' or 'cliente'
    
    def __init__(self, username, role):
        self.username = username
        self.role = role
        
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

login_manager = LoginManager(app)
login_manager.login_view = 'inicio'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('inicio.html', peliculas=peliculas)

@app.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    db.create_all()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index', peliculas=peliculas))
        else:
            flash('Usuario o contraseña inválidos.', 'danger')
    return render_template('inicio_sesion.html', form=form)

# Ruta para el registro de usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, role=form.role.data)
        user.set_password(form.password.data) 
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('registro.html', form=form)

@app.route('/cerrar_sesion')
def cerrar_sesion():
    logout_user()
    return redirect(url_for('index'))



@app.route('/consola', methods=['GET', 'POST'])
def consola():
    form = NuevaPeliculaForm()
    if form.validate_on_submit():
        titulo = form.titulo.data
        resumen = form.resumen.data
        caratula = form.caratula.data
        categoria = form.categoria.data
        precio_alquiler = form.precio_alquiler.data

        pelicula = Pelicula(titulo, resumen, caratula, categoria, precio_alquiler)

        # Cargar películas existentes
        peliculas = cargar_peliculas()
        peliculas.append(pelicula)

        # Guardar películas actualizadas en data.json
        guardar_peliculas(peliculas)
        return redirect(url_for('index'))

    return render_template('consola.html', form=form)



@app.route('/categoria/<tipo>', methods=['GET'])
def categoria(tipo):
    peliculas = cargar_peliculas()
    peliculas_tipo = [p for p in peliculas if p.categoria == tipo]
    return render_template('categoria.html', peliculas=peliculas_tipo, tipo=tipo)


if __name__ == '__main__':
    app.run(debug=True)
