from flask import Flask, render_template, redirect, url_for, request, abort,\
    session, Response, Blueprint, flash
from flask_login import LoginManager, login_user, logout_user, login_required,\
    current_user
from sqlalchemy.sql.expression import asc
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, desc
from sqlalchemy.sql.functions import concat
from sqlalchemy import DateTime, select, distinct, tuple_, text
from app import api, day
from pyzbar.pyzbar import decode
from PIL import Image
from datetime import date, timedelta
import datetime
import requests
import qrcode
import hashlib
    # FORMULARIOS
from forms.forms import *

app = Flask(__name__)
app.config.from_object(api)

qr = Blueprint('qr', __name__, template_folder='templates', static_folder='static', static_url_path='%s/qr' % app.static_url_path)

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Routes:
    base_code_qr = BASE_DIR + '/static/qr/img/'

class Properties:
    base_filename_code_qr = 'code_qr.png'

from os import path

def file_exits(url_path):
    if path.isfile(url_path):
        return True
    return False

def generate_code_qr(text):
    """ Generar código QR. """
    image = qrcode.make(text)
    file_image = open(Routes.base_code_qr + Properties.base_filename_code_qr, 'wb')
    image.save(file_image)
    file_image.close()

def read_code_qr():
    """ Método para leer codigos QR. """
    img = Image.open(Routes.base_code_qr + Properties.base_filename_code_qr)
    result = decode(img)
    text = None
    for i in result:
        text = i.data.decode("utf-8")
    return text

@qr.route("/qr/generador", methods=['GET', 'POST'])
@login_required
def qr_busqueda():
    today = date.today() # DIA ACTUAL
    fecha_qr = today.strftime("%m/%d/%Y")
    if request.method == 'POST':
        id_qr = request.form.get("id_qr")
        # OBTENER DATOS API
        id_client = str(id_qr)
        url = 'http://XXX'+id_client
        headers = {'Content-type': 'application/json','Accept': 'application/json'}
        datos_envio = {"Token":"XXX"}
        r = requests.get(url, headers=headers, json=datos_envio)
        dato = r.json()
        mem = dato['NoMembresia']
        nom = dato['Nombre']
        ape = dato['ApellidoPaterno']
        ape_2 = dato['ApellidoMaterno']
        nombre_completo = nom+' '+ape+' '+ape_2
        # CREACION QR
        #md5 = hashlib.md5(str(nombre_completo+fecha_qr).encode('utf-8')).hexdigest()
        md5 = hashlib.md5(str(mem).encode('utf-8')).hexdigest()
        #text = 'USUARIO-'+id_qr+'-'+mem+'-'+nombre_completo+'-'+md5
        text = 'CLIENTE-'+id_qr+'-'+md5
        if text == "":
            flash("El campo texto es obligatorio(*)", category='is-danger')
        else:
            generate_code_qr(text)
            flash("El código QR se genero de manera exitosa!!", category='alert alert-success')
        return redirect(url_for('qr.qr_busqueda'))
    else:
        if file_exits(Routes.base_code_qr + Properties.base_filename_code_qr) is False:
            generate_code_qr('http://XXX')
        return render_template('qr/qr.html')

@qr.route("/qr/generador/pases", methods=['GET', 'POST'])
@login_required
def qr_generador_pases():
    if request.method == 'POST':
        id_qr = request.form.get("id_qr")
        id_client = str(id_qr)
        # OBTENER DATOS API
        url = day.url_api_app+'citas/obtenerPase/'+id_client
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r = requests.get(url, headers=headers)
        dato_api = r.json()
        # EN LISTA TODOS LOS OBJETOS
        for dato in dato_api:
            id_producto_servicio = dato['idProd']
            fecha_captura = dato['f_compra']
            venta_detalle = dato['idVentaDetalle']
            # CREACION DEL MD5
            md5 = hashlib.md5(str(id_producto_servicio+fecha_captura).encode('utf-8')).hexdigest()
            text = 'PASE-'+str(id_producto_servicio)+'-'+str(fecha_captura)+'-'+md5+'-'+str(venta_detalle)+'-'+id_client+'-IDUSUARIO'
            print(text)
        #if text == "":
        #    return redirect(url_for('qr.qr_generador_pases'))
        #else:
            # CREACION QR
            generate_code_qr(text)
            flash("El código QR se genero de manera exitosa!!", category='is-success')
        return render_template('qr/qr_pases.html', dato_qr=dato_api)
    else:
        return render_template('qr/qr_pases.html')

@qr.route("/qr/generador/pases/parking", methods=['GET', 'POST'])
@login_required
def qr_generador_pases_parking():
    if request.method == 'POST':
        id_qr = request.form.get("id_qr")
        id_client = str(id_qr)
        # OBTENER DATOS API
        url = day.url_api_app+'parking/obtenerPaseQR/'+id_client
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r = requests.get(url, headers=headers)
        dato_api = r.json()
        return render_template('qr/qr_pases_parking.html', dato_qr=dato_api)
    else:
        return render_template('qr/qr_pases_parking.html')

@qr.route("/qr/generador/pases/parking/empleado", methods=['GET', 'POST'])
@login_required
def qr_generador_pases_parking_empleados():
    if request.method == 'POST':
        id_qr = request.form.get("id_qr")
        id_client = str(id_qr)
        # OBTENER DATOS API
        url = day.url_api_app+'parking/obtenerPaseEmpleadoQR/'+id_client
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r = requests.get(url, headers=headers)
        dato_api = r.json()
        return render_template('qr/Empleados/qr_pases_parking_empleados.html', dato_qr=dato_api)
    else:
        return render_template('qr/Empleados/qr_pases_parking_empleados.html')

@qr.route("/qr/generador/pases/parking/cortesias", methods=['GET', 'POST'])
@login_required
def qr_generador_pases_parking_cortesias():
    if request.method == 'POST':
        id_qr = request.form.get("id_qr")
        id_client = str(id_qr)
        # OBTENER DATOS API
        url = day.url_api_app+'parking/cortesiaQR/SP'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r = requests.get(url, headers=headers)
        dato_api = r.json()
        return render_template('qr/Cortesias/qr_pases_parking_cortesias.html', dato_qr=dato_api)
    else:
        return render_template('qr/Cortesias/qr_pases_parking_cortesias.html')

@qr.route("/qr/generador/pases/qr", methods=['GET', 'POST'])
@login_required
def qr_generador_pases_qr():
    if request.method == 'POST' and request.form.get("parking") == 'Fitness':
        id_qr = request.form.get("cliente")
        ovd_qr = request.form.get("idVentaDetalle")
        id_prod_qr = request.form.get("idProd")
        f_qr = request.form.get("f_compra")
        id_client = str(id_qr)
        # CREACION DEL MD5
        md5 = hashlib.md5(str(id_prod_qr+f_qr).encode('utf-8')).hexdigest()
        codigo = 'PASE-'+str(id_prod_qr)+'-'+str(f_qr)+'-'+md5+'-'+str(ovd_qr)+'-'+id_client+'-IDUSUARIO'
        generate_code_qr(codigo)
        return render_template('qr/qr_imagen.html', codigo=codigo)
    if request.method == 'POST' and request.form.get("parking") == 'SP':
        id_qr = request.form.get("cliente")
        ovd_qr = request.form.get("idVentaDetalle")
        id_prod_qr = request.form.get("idProd")
        f_qr = request.form.get("f_compra")
        id_client = str(id_qr)
        # CREACION DEL MD5
        md5 = hashlib.md5(str(id_prod_qr+f_qr).encode('utf-8')).hexdigest()
        #codigo = 'PARKING-'+str(id_prod_qr)+'-'+str(f_qr)+'-'+md5+'-'+str(ovd_qr)+'-'+id_client+'-IDUSUARIO'
        codigo = 'PARKING-'+str(ovd_qr)+'-'+md5+'-'+f_qr+'-'+id_client+'-IDUSUARIO'
        generate_code_qr(codigo)
        return render_template('qr/qr_imagen.html', codigo=codigo)
    if request.method == 'POST' and request.form.get("parking") == 'EMP':
        id_qr = request.form.get("cliente")
        ovd_qr = request.form.get("idVentaDetalle")
        id_prod_qr = request.form.get("idProd")
        f_qr = request.form.get("f_compra")
        concep_qr = request.form.get("concepto")
        id_client = str(id_qr)
        # CREACION DEL MD5
        md5 = hashlib.md5(str(id_prod_qr+f_qr).encode('utf-8')).hexdigest()
        codigo = 'EMPLEADO-'+concep_qr+'-IDPROD'+ovd_qr+'-'+md5
        generate_code_qr(codigo)
        return render_template('qr/qr_imagen.html', codigo=codigo)
    if request.method == 'POST' and request.form.get("parking") == 'COR':
        id_qr = request.form.get("cliente")
        ovd_qr = request.form.get("idVentaDetalle")
        id_prod_qr = request.form.get("idProd")
        f_qr = request.form.get("f_compra")
        concep_qr = request.form.get("concepto")
        id_client = str(id_qr)
        # CREACION DEL MD5
        md5 = hashlib.md5(str(id_prod_qr+f_qr).encode('utf-8')).hexdigest()
        codigo = 'CORTESIA-'+f_qr+'-IDPRODUCT-'+ovd_qr
        generate_code_qr(codigo)
        return render_template('qr/qr_imagen.html', codigo=codigo)