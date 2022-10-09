from flask import Flask, render_template, redirect, url_for, request, abort,session, Response
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message, Mail
from sqlalchemy.sql import func
from datetime import timezone, timedelta, datetime
from app import config
from app import api, day
    # FORMS
from forms.forms import *
    # VIEWS
from views.apis.views import apis
from views.dashboard.views import dashboard
from views.aforo.views import aforo
from views.acceso.views import acceso
from views.qr.views import qr
from views.perfil.views import perfil
from views.configuracion.views import configuracion
from views.pagos.views import pagos
from views.reportes.views import reportes
from views.usuarios.views import usuarios
from views.parking.views import parking
from views.caseta.views import caseta
from views.rh.views import rh
from views.rutinas.views import rutinas
from views.registro.views import registro
from views.eudep.views import eudep
from views.factura.views import factura
from views.domiciliacion.views import domiciliacion
from views.scrum.views import scrum
    # DRIVER
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required,current_user
    # TOKEN
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
import os
import requests
    # MAIL
mail = Mail()
    # APP
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'XXX'
app.config['MAIL_PASSWORD'] = 'XXX'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
    # VIEWS
app.register_blueprint(apis)
app.register_blueprint(dashboard)
app.register_blueprint(aforo)
app.register_blueprint(acceso)
app.register_blueprint(qr)
app.register_blueprint(perfil)
app.register_blueprint(configuracion)
app.register_blueprint(pagos)
app.register_blueprint(reportes)
app.register_blueprint(usuarios)
app.register_blueprint(parking)
app.register_blueprint(caseta)
app.register_blueprint(rh)
app.register_blueprint(rutinas)
app.register_blueprint(registro)
app.register_blueprint(eudep)
app.register_blueprint(factura)
app.register_blueprint(domiciliacion)
app.register_blueprint(scrum)
    # SYSTEM
mail.init_app(app)
app.config.from_object(config)
db = SQLAlchemy(app)
    # TOKEN
app.config["JWT_SECRET_KEY"] = "XXX"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)
    # LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

### ------------------------------------------------------- INICIO  PAGES ----------------------------------------------------------####
@app.route('/login', methods=["GET", "POST"])
def login():
    from models.models import Usuarios
    # Control de permisos - cambiar pizarron para redirigir
    if current_user.is_authenticated:
        return redirect(url_for("aforo.aforo_club"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('aforo.aforo_club'))
        form.username.errors.append("Usuario o contraseña incorrectas.")
    return render_template('inicio/login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/registro", methods=["GET", "POST"])
@login_required
def registro():
    from models.models import Usuarios
    # Control de permisos
    #if current_user.is_authenticated:
    #    return redirect(url_for("dashboard.dashboard_inicio"))
    form = FormUsuario()
    if form.validate_on_submit():
        existe_usuario = Usuarios.query.filter_by(username=form.username.data).first()
        if existe_usuario is None:
            user = Usuarios()
            form.populate_obj(user)
            #user.admin = False
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("aforo.aforo_club"))
        form.username.errors.append("Nombre de usuario ya existe.")
    return render_template("inicio/registro.html", form=form)
### ------------------------------------------------------- FIN INICIO PAGES --------------------------------------------------------####

@login_manager.user_loader
def load_user(user_id):
    from models.models import Usuarios
    return Usuarios.query.get(int(user_id))

@app.errorhandler(404)
@login_required
def page_not_found(error):
    return render_template("inicio/error.html", error="Página no encontrada..."), 404
