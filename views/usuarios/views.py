from flask import Flask, render_template, redirect, url_for, request, abort, flash,\
    session, Response, Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required,\
    current_user
from sqlalchemy.sql.expression import asc
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, desc
from sqlalchemy.sql.functions import concat
from sqlalchemy import DateTime, false, select, distinct, true, tuple_, text
from app import api, day
from datetime import date, timedelta
import requests
import datetime
    # FORMULARIOS
from forms.forms import *
app = Flask(__name__)
app.config.from_object(api)
app.config.from_object(day)

usuarios = Blueprint('usuarios', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

@usuarios.route("/usuarios/perfil", methods=["GET", "POST"])
@login_required
def usuarios_perfil():
    from models.models import db
    # CIMERA
    usuarios_ = db.engine.execute(text("SELECT * FROM usuarios_pagina ORDER BY nombre"))
    usuarios = [row for row in usuarios_]
    return render_template('Usuarios/perfil.html', usuarios=usuarios)

@usuarios.route("/usuarios/delete/<id>", methods=["GET", "POST"])
@login_required
def usuarios_delete(id):
    from models.models import Usuarios, db
    user = Usuarios.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    Usuarios.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("usuarios.usuarios_perfil"))

@usuarios.route("/usuarios/edit/<id>", methods=["GET", "POST"])
@login_required
def usuarios_edit(id):
    from models.models import Usuarios, db
    art = Usuarios.query.get(id)
    form = FormUsuario(obj=art)
    if form.validate_on_submit():
        form.populate_obj(art)
        db.session.commit()
        return redirect(url_for("usuarios.usuarios_perfil"))
    return render_template('Usuarios/registro.html', usuarios=usuarios, form=form)

