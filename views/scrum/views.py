from flask import Flask, render_template, redirect, url_for, request, abort, flash,\
    session, Response, Blueprint, g
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

scrum = Blueprint('scrum', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

@scrum.route("/scrum/inicio", methods=["GET", "POST"])
@login_required
def scrum_inicio():
    from models.models import db, SCRUM_kanban
    g.user = current_user
    tasks = None
    error = None
    if request.form:
        try:
            # Ensure tasks are unique
            if request.form.get("title") in [task.title for task in SCRUM_kanban.query.all()]:
                error = "Esta tarea ya existe."
            else:
                task = SCRUM_kanban(title=request.form.get("title"), status=request.form.get("status"), user_id = g.user.id)
                tasks = SCRUM_kanban.query.all()

                db.session.add(task)
                db.session.commit()
        except Exception as e:
            print("No se pudo agregar la tarea")
            print(e)
    # Sort tasks according to their status
    tasks = SCRUM_kanban.query.filter_by(user_id=g.user.id).all()
    todo = SCRUM_kanban.query.filter_by(status='todo',user_id=g.user.id).all()
    doing = SCRUM_kanban.query.filter_by(status='doing',user_id=g.user.id).all()
    done = SCRUM_kanban.query.filter_by(status='done',user_id=g.user.id).all()
    return render_template("Scrum/inicio.html", error=error, tasks=tasks, todo=todo, doing=doing, done=done, myuser=current_user)

@scrum.route("/scrum/update", methods=["POST"])
def scrum_update():
    from models.models import db, SCRUM_kanban
    try:
        newstatus = request.form.get("newstatus")
        name = request.form.get("name")
        task = SCRUM_kanban.query.filter_by(title=name).first()
        task.status = newstatus
        db.session.commit()
    except Exception as e:
        print("No se pudo actualizar el estado de la tarea")
        print(e)
    return redirect(url_for("scrum.scrum_inicio"))

@scrum.route("/scrum/delete", methods=["POST"])
def scrum_delete():
    from models.models import db, SCRUM_kanban
    title = request.form.get("title")
    task = SCRUM_kanban.query.filter_by(title=title).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("scrum.scrum_inicio"))
