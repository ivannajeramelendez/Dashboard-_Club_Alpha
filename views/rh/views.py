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
from datetime import datetime, timedelta
import requests
    # FORMULARIOS
from forms.forms import *
app = Flask(__name__)
app.config.from_object(api)

rh = Blueprint('rh', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

@rh.route("/rh/consulta", methods=['GET', 'POST'])
@login_required
def rh_consulta():
    from models.models import db
    # CLUB ALPHA 2
    rh_vacaciones_corp_ = db.engine.execute(("SELECT * FROM rh_vacaciones_empleado WHERE club = 'Corporativo'"))
    rh_vacaciones_corp = [row for row in rh_vacaciones_corp_]
    # CLUB ALPHA 2
    rh_vacaciones_a2_ = db.engine.execute(("SELECT * FROM rh_vacaciones_empleado WHERE club = 'Club Alpha 2'"))
    rh_vacaciones_a2 = [row for row in rh_vacaciones_a2_]
    # CLUB ALPHA 3
    rh_vacaciones_a3_ = db.engine.execute(("SELECT * FROM rh_vacaciones_empleado WHERE club = 'Club Alpha 3'"))
    rh_vacaciones_a3 = [row for row in rh_vacaciones_a3_]
    # SPORTS PLAZA
    rh_vacaciones_a4_ = db.engine.execute(("SELECT * FROM rh_vacaciones_empleado WHERE club = 'Sports Plaza'"))
    rh_vacaciones_a4 = [row for row in rh_vacaciones_a4_]
    # CIMERA
    rh_vacaciones_cim_ = db.engine.execute(("SELECT * FROM rh_vacaciones_empleado WHERE club = 'CIMERA'"))
    rh_vacaciones_cim = [row for row in rh_vacaciones_cim_]
    # DEPORTES
    rh_vacaciones_dep_ = db.engine.execute(("SELECT * FROM rh_vacaciones_empleado WHERE departamento = 'ACTIVIDADES DEPORTIVAS' OR  departamento = 'DEPORTES'"))
    rh_vacaciones_dep = [row for row in rh_vacaciones_dep_]
    if request.method == 'POST' and request.form.get("tipo") == 'reporte':
        # FECHA PARA EL DIA 
        incio = request.form.get('Fecha_Inicio')
        fin = request.form.get('Fecha_Fin')
        # REPORTE GENERAL
        rh_reporte_ = db.engine.execute(("SELECT rh_empleado.id_empleado,rh_empleado.empleado,rh_vacaciones_empleado.clave_externa,\
            rh_vacaciones_empleado.club,ingreso,ANTIGUEDAD,dias,dias_solicitados,dias_Restantes,SOLICITA,\
            to_char(fecha_solicitud, 'yyyy-MM-dd'::text) as fecha_solicitud,rh_solicitud.id as numero_solicitud,\
            to_char(rh_solicitud.fecha_inicio::timestamp with time zone AT TIME ZONE 'UTC', 'yyyy-MM-dd'::text)\
            as fechainicio,to_char(rh_solicitud.fecha_fin::timestamp with time zone AT TIME ZONE 'UTC', 'yyyy-MM-dd'::text) as fechafin\
            from rh_solicitud join rh_aprovados on id_solicitud=rh_solicitud.id join rh_empleado on\
            rh_solicitud.id_empleado=rh_empleado.id join rh_vacaciones_empleado on\
            rh_vacaciones_empleado.id_empleado=rh_empleado.id_empleado where rh_solicitud.fecha_inicio::timestamp with time zone AT TIME ZONE 'UTC'\
            between '"+incio+"' and '"+fin+"' and RH_empleado.activo='SI' and rh_aprovados.aprovado='SI' order by rh_solicitud.id"))
        rh_reporte = [row for row in rh_reporte_]
        return render_template('rh/Consulta/reporte_general.html', rh_reporte=rh_reporte, inicio=incio, fin=fin)
    return render_template('rh/Consulta/consulta.html', rh_vacaciones_a2=rh_vacaciones_a2, rh_vacaciones_a3=rh_vacaciones_a3, 
                                                        rh_vacaciones_a4=rh_vacaciones_a4, rh_vacaciones_cim=rh_vacaciones_cim,
                                                        rh_vacaciones_corp=rh_vacaciones_corp, rh_vacaciones_dep=rh_vacaciones_dep)

@rh.route("/rh/consulta/empleados/<id>", methods=['GET', 'POST'])
@login_required
def rh_consulta_empleado(id):
    id = id
    from models.models import db
    # VIEW
    rh_vacaciones_ = db.engine.execute(("SELECT * FROM rh_vacaciones_empleado WHERE id_empleado = "+id))
    rh_vacaciones = [row for row in rh_vacaciones_]
    # REGISTRO DE SOLICITUDES
    url = day.url_api_app+'rh/solicitudesPorEmpleado'
    headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
    datos_envio = {'empleado':id}
    r = requests.post(url, headers=headers, json=datos_envio)
    dato_api = r.json()
    return render_template('rh/Consulta/consulta_empleado.html', rh_vacaciones=rh_vacaciones, dato_api=dato_api, id=id)

@rh.route("/rh/consulta/empleados/solicitud", methods=['GET', 'POST'])
@login_required
def rh_consulta_empleado_solicitud():
    if request.method == 'POST':
        # DATOS
        Empleado = request.form.get('empleado')
        Dias_menos = request.form.get('dias_menos')
        Solicita = request.form.get('solicita')
        Fecha_inicio = request.form.get('fechaInicio')
        Fecha_fin = request.form.get('fechaFin')
        # ENVIO CITA
        url = day.url_api_app+'rh/crearSolicitud'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'empleado': Empleado, 'fechaInicio': Fecha_inicio, 'fechaFin': Fecha_fin, 'solicita': Solicita, 'diasMenos': Dias_menos}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("empleado")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rh.rh_consulta_empleado', id=Empleado))

@rh.route("/rh/consulta/empleados/aprovacion", methods=['GET', 'POST'])
@login_required
def rh_consulta_empleado_aprovacion():
    if request.method == 'POST':
        # DATOS
        ID_Solicitud = request.form.get('id_solicitud')
        ID_Empleado = request.form.get('id_empleado')
        Aprovacion = request.form.get('aprovacion')
        # ENVIO CITA
        url = day.url_api_app+'rh/setAprovado'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'idSolicitud': ID_Solicitud, "aprovado": Aprovacion}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("empleado")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rh.rh_consulta_empleado', id=ID_Empleado))

@rh.route("/rh/consulta/empleados/firma", methods=['GET', 'POST'])
@login_required
def rh_consulta_empleado_firma():
    if request.method == 'POST':
        # DATOS
        ID_Solicitud = request.form.get('id_solicitud')
        ID_Empleado = request.form.get('id_empleado')
        Documento = request.form.get('documento')
        Validacion = request.form.get('validacion')
        # ENVIO CITA
        url = day.url_api_app+'rh/firmaEmpleado'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'idSolicitud': ID_Solicitud, "entragaDocumento": Documento, "validacion":Validacion}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("empleado")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rh.rh_consulta_empleado', id=ID_Empleado))

@rh.route("/rh/consulta/empleados/registro_completo/<id>", methods=['GET', 'POST'])
@login_required
def rh_consulta_empleado_registros(id):
    id = id
    from models.models import db
    # VIEW
    rh_vacaciones_ = db.engine.execute(("SELECT * FROM rh_vacaciones_empleado WHERE id_empleado = "+id))
    rh_vacaciones = [row for row in rh_vacaciones_]
    # REGISTRO DE SOLICITUDES
    url = day.url_api_app+'rh/historicoEmpleado/'+id
    headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
    datos_envio = {'empleado':id}
    r = requests.get(url, headers=headers, json=datos_envio)
    dato_api = r.json()
    return render_template('rh/Consulta_id/consulta_empleado.html', rh_vacaciones=rh_vacaciones, dato_api=dato_api, id=id)

