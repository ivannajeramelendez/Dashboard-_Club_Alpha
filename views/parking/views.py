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

parking = Blueprint('parking', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

#===================================================================[CLIENTES]===================================================================#
@parking.route("/parking/consulta_vehiculo/estado", methods=['GET', 'POST'])
@login_required
def parking_consulta_vehiculo():
    if request.method == 'POST':
        id_cliente = request.form.get("id")
        id_client = str(id_cliente)
        # CONSULTA VEHICULO VISTA
        url_dos = day.url_api_app+'parking/registro/'+id_client
        headers_dos = {'Authorization':'Bearer '+ day.resp_api_token}
        r_dos = requests.get(url_dos, headers=headers_dos)
        dato = r_dos.json()
        return render_template('parking/consulta.html', dato=dato)
    return render_template('parking/consulta.html')

@parking.route("/parking/registro_vehiculo/estado_de_cuenta", methods=['GET', 'POST'])
@login_required
def parking_registro_vehiculo():
    if request.method == 'POST':
        id_cliente = request.form.get("id") #EXTRAE EL DATO DEL INPUT
        id_client = str(id_cliente)
        # REGISTRO CLIENTE APP
        url_dos = day.url_api_app+'parking/nuevo/'+id_client
        headers_dos = {'Authorization':'Bearer '+ day.resp_api_token}
        r_dos = requests.get(url_dos, headers=headers_dos)
        if r_dos.status_code == 200:
            try:
                dato = r_dos.json()
                IDCliente = dato['cliente']['idCLiente']
                Nombre = dato['cliente']['nombre']
                Membresia = dato['cliente']['membresia']
                Clientetipo = dato['cliente']['clienteTipo']
                Club = dato['cliente']['club']
                Vigencia_ = datetime.now() + timedelta(days=365)
                Vigencia = Vigencia_.strftime('%Y-%m-%d')
                return render_template('parking/Usuarios/registro.html', IDCliente=IDCliente, Membresia=Membresia, Clientetipo=Clientetipo, Club=Club, Nombre=Nombre, Vigencia=Vigencia)
            except ValueError:
                redirect(url_for('parking.parking_registro_vehiculo'))
    return render_template('parking/Usuarios/registro.html')

@parking.route("/parking/registro_vehiculo/estado_de_cuenta/envio", methods=['GET', 'POST'])
@login_required
def envio_datos_registro():
    if request.method == 'POST':
        # DATOS
        Nombre = request.form.get('Nombre')
        Club = request.form.get('Club')
        Membresia = request.form.get('Membresia')
        IDCliente = request.form.get('IDCliente')
        Clientetipo = request.form.get('Clientetipo')
        Placa = request.form.get('Placa')
        Marca = request.form.get('Marca')
        Modelo = request.form.get('Modelo')
        Color = request.form.get('Color')
        Nserie = request.form.get('Nserie')
        Año = request.form.get('Año')
        Vigencia = request.form.get('Vigencia')
        # ENVIO CITA
        url = day.url_api_app+'parking/carroNuevo'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {
            'nombreCompleto': Nombre, 'club': Club, 'membresia': Membresia, 'idCliente': IDCliente, 'tipoCliente': Clientetipo, 'placa': Placa
            , 'color': Color, 'marca': Marca, 'noSerie': Nserie, 'anio': Año, 'vigencia': Vigencia, 'modelo': Modelo}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("Nombre")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            print(dato)
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('parking.parking_registro_vehiculo'))
    else:
        return redirect(url_for('parking.parking_registro_vehiculo'))

@parking.route("/parking/consulta_chips_activos", methods=['GET', 'POST'])
@login_required
def parking_consulta_chip():
    from models.models import db
    if request.method == 'POST' and request.form.get("club") == 'A3':
        # ALPHA 3
        chips_a3 = db.engine.execute(text("SELECT id,UPPER(club)as club,id_chip,id_parking,id_cliente,UPPER(marca)as marca,UPPER(modelo)as modelo,\
                                            UPPER(no_serie)as no_serie,UPPER(placa)as placa,vigencia,UPPER(color)as color, id_empleado FROM Chip_carro WHERE club = 'Club Alpha 3'"))
        dato_3 = [row for row in chips_a3]
        # COUNT
        chips_count_a3 = db.engine.execute(text("SELECT COUNT(ID) AS Total FROM REGISTRO_TAG WHERE CLUB='Club Alpha 3'"))
        dato_count_3 = [row for row in chips_count_a3]
        print(dato_count_3)
        return render_template('parking/consulta_chip.html', dato_3=dato_3, dato_count_3=dato_count_3)
    elif  request.method == 'POST' and request.form.get("club") == 'A2':
        # ALPHA 3
        chips_a3 = db.engine.execute(text("SELECT id,UPPER(club)as club,id_chip,id_parking,id_cliente,UPPER(marca)as marca,UPPER(modelo)as modelo,\
                                            UPPER(no_serie)as no_serie,UPPER(placa)as placa,vigencia,UPPER(color)as color, id_empleado FROM Chip_carro WHERE club = 'Club Alpha 2'"))
        dato_3 = [row for row in chips_a3]
        # COUNT
        chips_count_a3 = db.engine.execute(text("SELECT COUNT(ID) AS Total FROM REGISTRO_TAG WHERE CLUB='Club Alpha 2'"))
        dato_count_3 = [row for row in chips_count_a3]
        print(dato_count_3)
        return render_template('parking/consulta_chip.html', dato_3=dato_3, dato_count_3=dato_count_3)
    elif  request.method == 'POST' and request.form.get("club") == 'CIM':
        # CIMERA
        chips_a3 = db.engine.execute(text("SELECT id,UPPER(club)as club,id_chip,id_parking,id_cliente,UPPER(marca)as marca,UPPER(modelo)as modelo,\
                                            UPPER(no_serie)as no_serie,UPPER(placa)as placa,vigencia,UPPER(color)as color, id_empleado FROM Chip_carro \
                                                WHERE club = 'CIMERA' or club= 'Futbol City'"))
        dato_3 = [row for row in chips_a3]
        # COUNT
        chips_count_a3 = db.engine.execute(text("SELECT COUNT(ID) AS Total FROM REGISTRO_TAG WHERE club='CIMERA' or club='Futbol City'"))
        dato_count_3 = [row for row in chips_count_a3]
        return render_template('parking/consulta_chip.html', dato_3=dato_3, dato_count_3=dato_count_3)
    elif  request.method == 'POST' and request.form.get("club") == 'A4':
        # SPORTS PLAZA
        chips_a3 = db.engine.execute(text("SELECT id,UPPER(club)as club,id_chip,id_parking,id_cliente,UPPER(marca)as marca,UPPER(modelo)as modelo,\
                                            UPPER(no_serie)as no_serie,UPPER(placa)as placa,vigencia,UPPER(color)as color, id_empleado FROM Chip_carro WHERE club = 'Sports Plaza'"))
        dato_3 = [row for row in chips_a3]
        return render_template('parking/consulta_chip.html', dato_3=dato_3)
    return render_template('parking/Menu/club.html')

@parking.route("/parking/reporte_usuario/estado", methods=['GET', 'POST'])
@login_required
def parking_reporte_usuario():
    if request.method == 'POST':
        id_cliente = request.form.get("id")
        id_client = str(id_cliente)
        # INCIDENCIAS CLIENTE
        url_inc = day.url_api_app+'parking/amonestacionesUsuario/'+id_client
        headers_inc = {'Authorization':'Bearer '+ day.resp_api_token}
        r_inc = requests.get(url_inc, headers=headers_inc)
        dato_inc = r_inc.json()
        # ACCESOS CLIENTE
        url_acc = day.url_api_app+'parking/registroUsuario/'+id_client
        headers_acc = {'Authorization':'Bearer '+ day.resp_api_token}
        r_acc = requests.get(url_acc, headers=headers_acc)
        dato_acc = r_acc.json()
        return render_template('parking/Usuarios/reporte_usuario.html', dato_inc=dato_inc, dato_acc=dato_acc)
    return render_template('parking/Usuarios/reporte_usuario.html')

#===================================================================[EMPLEADOS]===================================================================#
@parking.route("/parking/consulta_vehiculo/empleado")
@parking.route("/parking/registro_vehiculo/estado/empleado", methods=['GET', 'POST'])
@login_required
def parking_registro_vehiculo_empleados():
    if request.method == 'POST':
        id_empleado = request.form.get("id") #EXTRAE EL DATO DEL INPUT
        id_client = str(id_empleado)
        # REGISTRO CLIENTE APP
        url_dos = day.url_api_app+'parking/obtenerEmpleado/'+id_client
        headers_dos = {'Authorization':'Bearer '+ day.resp_api_token}
        r_dos = requests.get(url_dos, headers=headers_dos)
        if r_dos.status_code == 200:
            try:
                dato = r_dos.json()
                IDEmpleado = dato['idEmpleado']
                Nombre = dato['empleado']
                Departamento = dato['departamento']
                Club = dato['club']
                Vigencia_ = datetime.now() + timedelta(days=365)
                Vigencia = Vigencia_.strftime('%Y-%m-%d')
                return render_template('parking/Empleados/registro.html', IDEmpleado=IDEmpleado, Departamento=Departamento, Club=Club, Nombre=Nombre, Vigencia=Vigencia)
            except ValueError:
                redirect(url_for('parking.parking_registro_vehiculo_empleados'))
    return render_template('parking/Empleados/registro.html')

@parking.route("/parking/registro_vehiculo/estado_de_cuenta/envio/empleado", methods=['GET', 'POST'])
@login_required
def envio_datos_registro_empleados():
    if request.method == 'POST':
        # DATOS
        Nombre = request.form.get('Nombre')
        Club = request.form.get('Club')
        Chip = request.form.get('Chip')
        IDEmpleado = request.form.get('IDEmpleado')
        Clientetipo = request.form.get('Clientetipo')
        Placa = request.form.get('Placa')
        Marca = request.form.get('Marca')
        Modelo = request.form.get('Modelo')
        Color = request.form.get('Color')
        Nserie = request.form.get('Nserie')
        Año = request.form.get('Año')
        Vigencia = request.form.get('Vigencia')
        # ENVIO CITA
        url = day.url_api_app+'parking/carroNuevoEmpleado'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {
            'nombreCompleto': Nombre, 'club': Club, 'idChip': Chip, 'idEmpleado': IDEmpleado, 'tipoCliente': Clientetipo, 'placa': Placa
            , 'color': Color, 'marca': Marca, 'noSerie': Nserie, 'anio': Año, 'vigencia': Vigencia, 'modelo': Modelo
            }
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("Nombre")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            print(dato)
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('parking.parking_registro_vehiculo_empleados'))
    else:
        return redirect(url_for('parking.parking_registro_vehiculo_empleados'))

#===================================================================[UPDATE]===================================================================#
@parking.route("/parking/update_vehiculo/cambio", methods=['GET', 'POST'])
@login_required
def parking_update_vehiculo():
    if request.method == 'POST':
        #EXTRAE EL DATO DEL INPUT
        id_cliente = request.form.get("id")
        id_client = str(id_cliente)
        # CONSULTA VEHICULO UPDATE
        url_update = day.url_api_app+'parking/consultarCliente/'+id_client
        headers_update = {'Authorization':'Bearer '+ day.resp_api_token}
        r_update = requests.get(url_update, headers=headers_update)
        if r_update.status_code == 200:
            try:
                dato = r_update.json()
                return render_template('parking/Update/update.html', dato=dato)
            except ValueError:
                redirect(url_for('parking.parking_update_vehiculo'))
    return render_template('parking/Update/update.html')

@parking.route("/parking/update_vehiculo/vehiculo/envio", methods=['GET', 'POST'])
@login_required
def envio_datos_update():
    if request.method == 'POST':
        # DATOS
        idVentaDetalle = request.form.get('idVentaDetalle')
        placa = request.form.get('placa')
        color = request.form.get('color')
        marca = request.form.get('marca')
        noSerie = request.form.get('noSerie')
        anio = request.form.get('anio')
        modelo = request.form.get('modelo')
        id = request.form.get('id')
        # ENVIO CAMBIOS
        url = day.url_api_app+'parking/actualizarCarro'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {
            'idVentaDetalle': idVentaDetalle, 'placa': placa, 'color': color, 'marca': marca, 'noSerie': noSerie, 'anio': anio, 'modelo': modelo, 'id': id}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("id")
        if text == "":
            flash("Todos los campos son obligatorios", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('parking.parking_update_vehiculo'))
    else:
        return redirect(url_for('parking.parking_update_vehiculo'))

#===================================================================[N° CHIP UPDATE]===================================================================#
@parking.route("/parking/update_chip_vehiculo/update", methods=['GET', 'POST'])
@login_required
def parking_update_chip():
    if request.method == 'POST':
        #EXTRAE EL DATO DEL INPUT
        id_cliente = request.form.get("id")
        id_client = str(id_cliente)
        # CONSULTA VEHICULO UPDATE
        url_update = day.url_api_app+'parking/consultarCliente/'+id_client
        headers_update = {'Authorization':'Bearer '+ day.resp_api_token}
        r_update = requests.get(url_update, headers=headers_update)
        if r_update.status_code == 200:
            try:
                dato = r_update.json()
                return render_template('parking/Cambio_Chip/update.html', dato=dato)
            except ValueError:
                redirect(url_for('parking.parking_update_chip'))
    return render_template('parking/Cambio_Chip/update.html')

@parking.route("/parking/update_chip_vehiculo/update/envio", methods=['GET', 'POST'])
@login_required
def parking_update_chip_update():
    if request.method == 'POST':
        # DATOS
        chip_anterior = request.form.get('chip_anterior')
        chip_nuevo = request.form.get('chip_nuevo')
        # ENVIO CAMBIOS
        url = day.url_api_app+'parking/actualizarChip'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'idChipAnterior': chip_anterior, 'idChipNuevo': chip_nuevo}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("id")
        if text == "":
            flash("Todos los campos son obligatorios", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('parking.parking_update_chip'))
    else:
        return redirect(url_for('parking.parking_update_chip'))

#===================================================================[N° CHIP UPDATE]===================================================================#
@parking.route("/parking/delete_chip_vehiculo/delete", methods=['GET', 'POST'])
@login_required
def parking_delete_chip():
    if request.method == 'POST':
        #EXTRAE EL DATO DEL INPUT
        id_cliente = request.form.get("id")
        id_client = str(id_cliente)
        # CONSULTA VEHICULO UPDATE
        url_update = day.url_api_app+'parking/consultarCliente/'+id_client
        headers_update = {'Authorization':'Bearer '+ day.resp_api_token}
        r_update = requests.get(url_update, headers=headers_update)
        if r_update.status_code == 200:
            try:
                dato = r_update.json()
                return render_template('parking/Eliminar_Chip/update.html', dato=dato)
            except ValueError:
                redirect(url_for('parking.parking_delete_chip'))
    return render_template('parking/Eliminar_Chip/update.html')

@parking.route("/parking/delete_chip_vehiculo/delete/envio", methods=['GET', 'POST'])
@login_required
def parking_delete_chip_update():
    if request.method == 'POST':
        # DATOS
        chip_anterior = request.form.get('chip_anterior')
        # ENVIO CAMBIOS
        url = day.url_api_app+'parking/desactivarChip/'+chip_anterior
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r = requests.get(url, headers=headers)
        text = request.form.get("id")
        if text == "":
            flash("Todos los campos son obligatorios", category='alert alert-danger')
        else:
            dato = r.json()
            print(dato)
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('parking.parking_delete_chip'))
    else:
        return redirect(url_for('parking.parking_delete_chip'))
