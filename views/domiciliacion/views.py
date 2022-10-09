import re
from flask import Flask, render_template, redirect, url_for, request, abort, flash,\
    session, Response, Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required,\
    current_user
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, text
from app import api, day
import requests
import json
 #===================================================================[CONEKTA]===================================================================#
import conekta
from datetime import datetime, timedelta
from forms.forms import *
app = Flask(__name__)
app.config.from_object(api)

domiciliacion = Blueprint('domiciliacion', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

#===================================================================[ DOM ]===================================================================#
@domiciliacion.route("/domiciliacion/generar_cobro/fiserv", methods=['GET', 'POST'])
@login_required
def domiciliacion_inicio():
    from models.models import db
    dom_ = db.engine.execute(("SELECT * FROM domiciliacion"))
    dom = [row for row in dom_]
    Mes = datetime.now().strftime("%B")
    if request.method == 'POST' and request.form.get("tipo") == 'actualizar':
        url = day.url_api_app+'alpha/actualizarDomiciliacion'
        headers = {'Authorization':'Bearer '+ day.resp_api_token}
        r = requests.get(url, headers=headers)
        print(r)
        return redirect(url_for('domiciliacion.domiciliacion_inicio'))
    if request.method == 'POST' and request.form.get("tipo") == 'pagar':
        # LISTAS
        IDCliente = request.form.getlist('id_cliente')
        Monto = request.form.getlist('monto')
        # LISTA 
        url = day.url_api_app+'alpha/pagosDomiciliadosFiserv'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {"body":[{'domiciliados': [{'idCliente': a, 'monto': r} for a,r in zip(IDCliente,Monto)] }] }
        r = requests.post(url, headers=headers, json=datos_envio)
        if r.status_code == 200:
            try:
                # DESENCADENAR JSON
                dato_dom = r.json()
                print(dato_dom)
                dato = r.json()
                resp_api = dato['respuesta']
                flash(resp_api, category='alert alert-success')
                return redirect(url_for('domiciliacion.domiciliacion_inicio'))
            except ValueError:
                redirect(url_for('domiciliacion.domiciliacion_inicio'))
    return render_template('domiciliacion/consulta.html', dom=dom, Mes=Mes)

@domiciliacion.route("/domiciliacion/reporte/intentos", methods=['GET', 'POST'])
@login_required
def domiciliacion_reporte():
    from models.models import db
    # DATA FECHA
    fecha_inicio = request.form.get("Fecha_Inicio")
    fecha_fin = request.form.get("Fecha_Fin")
    club = request.form.get("Club")
    # CALL DATOS
    corte_a3_ = db.engine.execute(text("SELECT CC.*, to_char( RC.fecha_corte, 'HH24:MI:SS') AS fecha_corte_min FROM corte_caja AS CC \
                                        FULL OUTER JOIN Registro_cortes AS RC ON CC.folio = RC.id_corte \
                                        WHERE cc.club='Club Alpha 2' AND cc.fecha BETWEEN '12-09-2022' AND '27-09-2022'  ORDER BY cc.folio::integer"))
    corte_a3 = [row for row in corte_a3_]
    return render_template('domiciliacion/Corte/consulta.html', corte_a3=corte_a3)
