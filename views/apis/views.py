from flask import Flask, render_template, redirect, url_for, request, abort, flash,session, Response, Blueprint, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required,current_user
from sqlalchemy.sql.expression import asc
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, desc, text
from sqlalchemy.sql.functions import concat
from sqlalchemy import DateTime, select
from app import api, day
import requests
from datetime import timezone, timedelta, datetime
    # APIS REQUERIMETS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, get_jwt, set_access_cookies
    # FORMULARIOS
from forms.forms import *

app = Flask(__name__)
app.config.from_object(api)
app.config.from_object(day)

apis = Blueprint('apis', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

@apis.route("/api/auth/login", methods=["POST"])
def login():
    from models.models import Usuarios
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = Usuarios.query.filter_by(username=username).first()
    if user is not None and user.verify_password(password):
        access_token = create_access_token(identity=username, fresh=True)
        return jsonify(token=access_token)
    else:
        return jsonify({"msg": "Error en Usuario o Contraseña"}), 401

@apis.route("/api/auth/user", methods=["GET"])
@jwt_required(fresh=True)
def protected():
    from models.models import db
    result = db.engine.execute(text("SELECT * FROM usuarios_pagina"))
    return jsonify([dict(row) for row in result]), 200

@apis.route("/api/auth/parking/tag_vigente", methods=["POST"])
@jwt_required(fresh=True)
def api_parking_tag_vigente():
    from models.models import db
    fecha = request.json.get("desde", None)
    if len(fecha) == 10:
        result = db.engine.execute(text("SELECT * FROM registro_tag WHERE fecha_fin >= '"+fecha+"'"))
        return jsonify([dict(row) for row in result]), 200
    else:
        return jsonify({"msg": "Error en peticion, verifica la fecha de nuevo (YYYY-MM-DD)"}), 401