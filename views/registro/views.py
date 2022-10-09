import re
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

registro = Blueprint('registro', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

@registro.route("/registro/consulta", methods=['GET', 'POST'])
@login_required
def registro_consulta():
    from models.models import db
    # CLUB ALPHA 2
    rh_vacaciones_a2_ = db.engine.execute(("SELECT * FROM rh_vacaciones_empleado WHERE club = 'Club Alpha 2'"))
    rh_vacaciones_a2 = [row for row in rh_vacaciones_a2_]
    # CONSULTA DATOS
    url_dos = day.url_api_app+'parking/obtenerTitulares'
    headers_dos = {'Authorization':'Bearer '+ day.resp_api_token}
    r_dos = requests.get(url_dos, headers=headers_dos)
    dato = r_dos.json()
    if request.method == 'POST':
        # DATOS
        Nombre = request.form.get("Nombre")
        Club = request.form.get("Club")
        Sexo = request.form.get("Sexo")
        Telefono = request.form.get("Telefono")
        Correo = request.form.get("Correo")
        Tipo = request.form.get("Tipo")
        Registro = request.form.get("Registro")
        Titular = request.form.get("Titular")
        # ENVIO DE DATOS
        url_envio = day.url_api_app+'parking/crearTitular'
        headers_envio = {'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'nombreCompleto': Nombre, "sexo": Sexo, "telefono":Telefono, "correoElectronico":Correo, "tipo":Tipo, "fechaRegistro":Registro, "club":Club}
        r_envio = requests.post(url_envio, headers=headers_envio, json=datos_envio)
        dato = r_envio.json()
        resp_api = dato['respuesta']
        flash(resp_api, category='alert alert-success')
        return redirect(url_for('registro.registro_consulta'))
    return render_template('Alpha_4/Consulta/consulta.html', rh_vacaciones_a2=rh_vacaciones_a2, dato=dato)

@registro.route("/registro/consulta/empleados/<id>", methods=['GET', 'POST'])
@login_required
def registro_consulta_usuario(id):
    id = id
    from models.models import db
    # DATO TITULAR
    url_titular = day.url_api_app+'parking/obtenerTitulares/'+id
    headers_titular = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
    r_titular = requests.get(url_titular, headers=headers_titular)
    dato_titular = r_titular.json()
    # DATO DEPENDIENTE
    url_con_dependiente = day.url_api_app+'parking/obtenerDependientes/'+id
    headers_con_dependiente = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
    r_con_dependiente = requests.get(url_con_dependiente, headers=headers_con_dependiente)
    dator_con_dependiente = r_con_dependiente.json()
    if request.method == 'POST':
        # DATOS
        Nombre = request.form.get("Nombre")
        Club = request.form.get("Club")
        Sexo = request.form.get("Sexo")
        Telefono = request.form.get("Telefono")
        Correo = request.form.get("Correo")
        Tipo = request.form.get("Tipo")
        Registro = request.form.get("Registro")
        Titular = request.form.get("Titular")
        # REGISTRO DE SOLICITUDES
        url_dependiente = day.url_api_app+'parking/crearDependiente'
        headers_dependiente = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio_dependiente = {'id':id,'nombreCompleto':Nombre,"sexo":Sexo,"telefono":Telefono,"correoElectronico":Correo,"tipo":Tipo,"fechaRegistro":Registro,"club":Club}
        r_dependiente = requests.post(url_dependiente, headers=headers_dependiente, json=datos_envio_dependiente)
        dato_api = r_dependiente.json()
        resp_api = dato_api['respuesta']
        flash(resp_api, category='alert alert-success')
        return redirect(url_for('registro.registro_consulta_usuario', id=id))
    return render_template('Alpha_4/Consulta/consulta_usuario.html', id=id, dato_titular=dato_titular, dator_con_dependiente=dator_con_dependiente)


#== EXTRA 

@registro.route("/registro/consulta/empleados/solicitud", methods=['GET', 'POST'])
@login_required
def registro_consulta_empleado_solicitud():
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

@registro.route("/registro/consulta/empleados/aprovacion", methods=['GET', 'POST'])
@login_required
def registro_consulta_empleado_aprovacion():
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
            print(dato)
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rh.rh_consulta_empleado', id=ID_Empleado))

@registro.route("/registro/consulta/empleados/firma", methods=['GET', 'POST'])
@login_required
def registro_consulta_empleado_firma():
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
            print(dato)
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rh.rh_consulta_empleado', id=ID_Empleado))

@registro.route("/registro/consulta/empleados/registro_completo/<id>", methods=['GET', 'POST'])
@login_required
def registro_consulta_empleado_registros(id):
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
    return render_template('Alpha_4/Consulta_id/consulta_usuario.html', rh_vacaciones=rh_vacaciones, dato_api=dato_api, id=id)

