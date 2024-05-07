from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, current_user, logout_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '7af32be7f2f18aa5046c6c3d068427dd7d95b4e5d3242725'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)


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
    return render_template("inicio.html")

@app.route('/inicio_sesion', methods=['GET', 'POST'])
def login():
    db.create_all()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Has iniciado sesión correctamente.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Usuario o contraseña inválidos.', 'danger')
    return render_template('inicio_sesion.html', form=form)

# Ruta para el registro de usuarios
@app.route('/registro', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, role=form.role.data)
        user.set_password(form.password.data) 
        db.session.add(user)
        db.session.commit()
        flash('Te has registrado correctamente.', 'success')
        return redirect(url_for('inicio'))
    return render_template('registro.html', form=form)

@app.route('/cerrar-sesion')
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('inicio'))

@app.route('/inicio')
def inicio():
    if current_user.is_authenticated:
        return 'Página de inicio para usuarios estándar'
    else:
        flash('Debe iniciar sesión para acceder a esta página.', 'warning')
        return redirect(url_for('inicio_sesion'))

@app.route('/premium')
def premium():
    if current_user.is_authenticated and current_user.role == 'premium':
        return 'Página de inicio para usuarios premium'
    else:
        flash('Debe iniciar sesión como usuario premium para acceder a esta página.', 'warning')
        return redirect(url_for('inicio_sesion'))

if __name__ == '__main__':
    app.run(debug=True)
