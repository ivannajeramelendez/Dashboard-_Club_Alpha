from flask import Flask, render_template, redirect, url_for, request, abort, flash,\
    session, Response, Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required,\
    current_user
from sqlalchemy.sql.expression import asc
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, desc
from sqlalchemy.sql.functions import concat
from sqlalchemy import DateTime, select, distinct, tuple_, text
from app import api, day
from datetime import date, timedelta
import requests
import datetime
#===================================================================[CONEKTA]===================================================================#
import conekta
    # FORMULARIOS
from forms.forms import *
app = Flask(__name__)
app.config.from_object(api)
app.config.from_object(day)

factura = Blueprint('factura', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

@factura.route("/factura/revision", methods=["GET", "POST"])
def factura_consulta():
    if request.method == 'POST' and request.form.get("tipo") == 'consulta':
        # DATOS
        Recibo = request.form.get('recibo')
        Cliente = request.form.get('id_cliente')
        # ENVIO DATOS
        url = day.url_api_app+'alpha/facturarRecibo'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'recibo': Recibo, "usuario": Cliente}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("Nombre")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('factura.factura_oxxo'))
    if request.method == 'POST' and request.form.get("tipo") == 'global':
        # DATOS
        Recibo = request.form.get('recibo')
        Cliente = request.form.get('id_cliente')
        Solicita = request.form.get('solicita')
        # ENVIO DATOS
        url = day.url_api_app+'alpha/recibosMes/'+Solicita
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r = requests.get(url, headers=headers)
        text = request.form.get("Nombre")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('factura.factura_consulta'))
    return render_template('factura/consulta.html')
