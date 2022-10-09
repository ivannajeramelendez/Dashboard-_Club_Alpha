from flask import Flask, render_template, redirect, url_for, request, abort, flash,\
    session, Response, Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required,\
    current_user
from sqlalchemy.sql.expression import asc
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, desc
from sqlalchemy.sql.functions import concat
from sqlalchemy import DateTime, select
from app import api, day
from datetime import date, timedelta
import requests
import datetime
    # FORMULARIOS
from forms.forms import *
app = Flask(__name__)
app.config.from_object(api)
app.config.from_object(day)

perfil = Blueprint('perfil', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

@perfil.route("/perfil/perfil")
@login_required
def perfil_perfil():
    return render_template('perfil/perfil.html')

@perfil.route('/perfil/perfil/changepassword/<username>', methods=["GET", "POST"])
@login_required
def perfil_changepassword(username):
    from models.models import Usuarios, db
    user = Usuarios.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    form = FormChangePassword()
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("perfil.perfil_perfil"))
    return render_template('perfil/perfil_2.html', form=form)