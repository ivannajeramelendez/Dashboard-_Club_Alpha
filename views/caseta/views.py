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
import json
#===================================================================[QR]===================================================================#
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
import hashlib
#===================================================================[FORMULARIOS]===================================================================#
from forms.forms import *
app = Flask(__name__)
app.config.from_object(api)

#caseta = Blueprint('caseta', __name__, template_folder='templates', static_folder='static', static_url_path='%s/qr' % app.static_url_path)
caseta = Blueprint('caseta', __name__, template_folder='templates', static_folder='static', static_url_path='/qr/img')

#===================================================================[QR]===================================================================#
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Routes:
    base_code_qr = BASE_DIR + '/static/qr/img/'

class Properties:
    base_filename_code_qr = 'code_qr_parking.png'

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

#===================================================================[QR]===================================================================#
@caseta.route("/caseta/registro")
@caseta.route("/caseta/registro_qr", methods=['GET', 'POST'])
@login_required
def caseta_registro_qr():
    # BOTON HORARIO
    url_boton = day.url_api_app+'parking/turno'
    headers_boton = {'Authorization':'Bearer '+ day.resp_api_token}
    r_boton = requests.get(url_boton, headers=headers_boton)
    dato_boton = r_boton.json()
    if request.method == 'POST' and request.form.get("club") == 'A3':
        # LLAMADA DE DATOS
        url_dos = day.url_api_app+'parking/estacionamientoExterno/A3'
        headers_dos = {'Authorization':'Bearer '+ day.resp_api_token}
        r_dos = requests.get(url_dos, headers=headers_dos)
        dato = r_dos.json()
        Recibo = dato['idRegistro']
        UUID = dato['id']
        #Club = dato['club']
        Club = 'A3'
        Hora_Entrada = dato['horaEntrada']
        Hora_Salida = dato['horaSalida']
        Costo_Total = dato['costoTotal']
        # CREACION DE CODIGO QR
        Vigencia_ = datetime.now()
        Vigencia_time = datetime.timestamp(Vigencia_) # TIMESTAMP QR
        md5 = hashlib.md5(str(UUID).encode('utf-8')).hexdigest()
        codigo = 'RECIBO-'+str(Recibo)+'-UUID-'+md5+'-Entrada-'+str(Vigencia_time)+'-'+str(Club)
        qr_parking = codigo
        generate_code_qr(qr_parking)
        # ENVIO DE PING A PLUMA
        send_localhost_ = 'http://XXX/abrir?'+Recibo
        r_localhost = requests.get(send_localhost_)
        print(r_localhost)
        if Recibo == "":
            flash("¡El recibo se encuentra vacio!", category='is-danger')
        else:
            flash("El código QR se genero de manera exitosa!!", category='alert alert-success')
        return redirect(url_for('caseta.caseta_registro_qr'))
    elif  request.method == 'POST' and request.form.get("club") == 'CIM':
        # LLAMADA DE DATOS
        url_dos = day.url_api_app+'parking/estacionamientoExterno/CIM'
        headers_dos = {'Authorization':'Bearer '+ day.resp_api_token}
        r_dos = requests.get(url_dos, headers=headers_dos)
        dato = r_dos.json()
        Recibo = dato['idRegistro']
        UUID = dato['id']
        #Club = dato['club']
        Club = 'CIM'
        Hora_Entrada = dato['horaEntrada']
        Hora_Salida = dato['horaSalida']
        Costo_Total = dato['costoTotal']
        # CREACION DE CODIGO QR
        Vigencia_ = datetime.now()
        Vigencia_time = datetime.timestamp(Vigencia_) # TIMESTAMP QR 
        md5 = hashlib.md5(str(UUID).encode('utf-8')).hexdigest()
        codigo = 'RECIBO-'+str(Recibo)+'-UUID-'+md5+'-Entrada-'+str(Vigencia_time)+'-'+str(Club)
        qr_parking = codigo
        generate_code_qr(qr_parking)
        if Recibo == "":
            flash("¡El recibo se encuentra vacio!", category='is-danger')
        else:
            flash("El código QR se genero de manera exitosa!!", category='alert alert-success')
        return redirect(url_for('caseta.caseta_registro_qr'))
    else:
        if file_exits(Routes.base_code_qr + Properties.base_filename_code_qr) is False:
            generate_code_qr('http://XXX/')
        return render_template('caseta/qr.html', dato_boton=dato_boton)

@caseta.route("/caseta/registro_qr/caja", methods=['GET', 'POST'])
@login_required
def caseta_registro_qr_caja():
    # BOTON HORARIO
    url_boton = day.url_api_app+'parking/turno'
    headers_boton = {'Authorization':'Bearer '+ day.resp_api_token}
    r_boton = requests.get(url_boton, headers=headers_boton)
    dato_boton = r_boton.json()
    if request.method == 'POST':
        # LLAMADA DE DATOS
        url_dos = day.url_api_app+'parking/estacionamientoExterno/A3/caja'
        headers_dos = {'Authorization':'Bearer '+ day.resp_api_token}
        r_dos = requests.get(url_dos, headers=headers_dos)
        dato = r_dos.json()
        Recibo = dato['idRegistro']
        UUID = dato['id']
        #Club = dato['club']
        Club = 'A3'
        Hora_Entrada = dato['horaEntrada']
        Hora_Salida = dato['horaSalida']
        Costo_Total = dato['costoTotal']
        # CREACION DE CODIGO QR
        Vigencia_ = datetime.now()
        Vigencia_time = datetime.timestamp(Vigencia_) # TIMESTAMP QR 
        md5 = hashlib.md5(str(UUID).encode('utf-8')).hexdigest()
        codigo = 'RECIBO-'+str(Recibo)+'-UUID-'+md5+'-Entrada-'+str(Vigencia_time)+'-'+str(Club)
        qr_parking = codigo
        generate_code_qr(qr_parking)
        if Recibo == "":
            flash("¡El recibo se encuentra vacio!", category='is-danger')
        else:
            flash("El código QR se genero de manera exitosa!!", category='alert alert-success')
        return redirect(url_for('caseta.caseta_registro_qr'))
    else:
        if file_exits(Routes.base_code_qr + Properties.base_filename_code_qr) is False:
            generate_code_qr('http://XXX/')
        return render_template('caseta/qr.html', dato_boton=dato_boton)

@caseta.route("/caseta/registro_qr/caja/cortesia", methods=['GET', 'POST'])
@login_required
def caseta_registro_qr_caja_cortesia():
    # BOTON HORARIO
    url_boton = day.url_api_app+'parking/turno'
    headers_boton = {'Authorization':'Bearer '+ day.resp_api_token}
    r_boton = requests.get(url_boton, headers=headers_boton)
    dato_boton = r_boton.json()
    if request.method == 'POST':
        # LLAMADA DE DATOS
        url_dos = day.url_api_app+'parking/cortesiaQR/A3'
        headers_dos = {'Authorization':'Bearer '+ day.resp_api_token}
        r_dos = requests.get(url_dos, headers=headers_dos)
        dato = r_dos.json()
        Recibo = dato['idRegistro']
        UUID = dato['id']
        #Club = dato['club']
        Club = 'A3'
        Hora_Entrada = dato['horaEntrada']
        Hora_Salida = dato['horaSalida']
        Costo_Total = dato['costoTotal']
        # CREACION DE CODIGO QR
        Vigencia_ = datetime.now()
        Vigencia_time = datetime.timestamp(Vigencia_) # TIMESTAMP QR 
        md5 = hashlib.md5(str(UUID).encode('utf-8')).hexdigest()
        codigo = 'CORTESIA-'+str(Recibo)+'-UUID-'+md5+'-Entrada-'+str(Vigencia_time)+'-'+str(Club)
        qr_parking = codigo
        generate_code_qr(qr_parking)
        if Recibo == "":
            flash("¡El recibo se encuentra vacio!", category='is-danger')
        else:
            flash("El código QR se genero de manera exitosa!!", category='alert alert-success')
        return redirect(url_for('caseta.caseta_registro_qr'))
    else:
        if file_exits(Routes.base_code_qr + Properties.base_filename_code_qr) is False:
            generate_code_qr('http://XXX/')
        return render_template('caseta/qr.html', dato_boton=dato_boton)

#===================================================================[CORTE DE CAJA]===================================================================#
@caseta.route("/caseta/corte_de_caja", methods=['GET', 'POST'])
@login_required
def caseta_corte_de_caja():
    if request.method == 'POST' and request.form.get("club") == 'A3':
        # BOTON HORARIO
        url_boton = day.url_api_app+'parking/finalizarTurno/A3'
        headers_boton = {'Authorization':'Bearer '+ day.resp_api_token}
        r_boton = requests.get(url_boton, headers=headers_boton)
        dato_boton = r_boton.json()
        flash(dato_boton, category='alert alert-success')
        return redirect(url_for('caseta.caseta_consulta_chip'))
    elif  request.method == 'POST' and request.form.get("club") == 'A2':
        # BOTON HORARIO
        url_boton = day.url_api_app+'parking/finalizarTurno/A2'
        headers_boton = {'Authorization':'Bearer '+ day.resp_api_token}
        r_boton = requests.get(url_boton, headers=headers_boton)
        dato_boton = r_boton.json()
        flash(dato_boton, category='alert alert-success')
        return redirect(url_for('caseta.caseta_consulta_chip'))
    elif  request.method == 'POST' and request.form.get("club") == 'CIM':
        # BOTON HORARIO
        url_boton = day.url_api_app+'parking/finalizarTurno/CIM'
        headers_boton = {'Authorization':'Bearer '+ day.resp_api_token}
        r_boton = requests.get(url_boton, headers=headers_boton)
        dato_boton = r_boton.json()
        flash(dato_boton, category='alert alert-success')
        return redirect(url_for('caseta.caseta_consulta_chip'))
    else:
        return redirect(url_for('caseta.caseta_consulta_chip'))

@caseta.route("/caseta/corte_de_caja/caja", methods=['GET', 'POST'])
@login_required
def caseta_corte_de_caja_caja():
    if request.method == 'POST' and request.form.get("club") == 'A3':
        # BOTON HORARIO
        url_boton = day.url_api_app+'parking/finalizarTurno/A3/caja'
        headers_boton = {'Authorization':'Bearer '+ day.resp_api_token}
        r_boton = requests.get(url_boton, headers=headers_boton)
        dato_boton = r_boton.json()
        flash(dato_boton, category='alert alert-success')
        return redirect(url_for('caseta.caseta_consulta_chip'))
    elif  request.method == 'POST' and request.form.get("club") == 'A2':
        # BOTON HORARIO
        url_boton = day.url_api_app+'parking/finalizarTurno/A2/caja'
        headers_boton = {'Authorization':'Bearer '+ day.resp_api_token}
        r_boton = requests.get(url_boton, headers=headers_boton)
        dato_boton = r_boton.json()
        flash(dato_boton, category='alert alert-success')
        return redirect(url_for('caseta.caseta_consulta_chip'))
    elif  request.method == 'POST' and request.form.get("club") == 'CIM':
        # BOTON HORARIO
        url_boton = day.url_api_app+'parking/finalizarTurno/CIM/caja'
        headers_boton = {'Authorization':'Bearer '+ day.resp_api_token}
        r_boton = requests.get(url_boton, headers=headers_boton)
        dato_boton = r_boton.json()
        flash(dato_boton, category='alert alert-success')
        return redirect(url_for('caseta.caseta_consulta_chip'))
    else:
        return redirect(url_for('caseta.caseta_consulta_chip'))

#===================================================================[QR PERDIDA]===================================================================#
@caseta.route("/caseta/perdida_qr", methods=['GET', 'POST'])
@login_required
def caseta_perdida_qr():
    if request.method == 'POST':
        # LLAMADA DE DATOS
        url_dos = day.url_api_app+'parking/perdidaQR/A3'
        headers_dos = {'Authorization':'Bearer '+ day.resp_api_token}
        r_dos = requests.get(url_dos, headers=headers_dos)
        dato = r_dos.json()
        Recibo = dato['idRegistro']
        UUID = dato['id']
        #Club = dato['club']
        Club = 'A3'
        Hora_Entrada = dato['horaEntrada']
        Hora_Salida = dato['horaSalida']
        Costo_Total = dato['costoTotal']
        # CREACION DE CODIGO QR
        Vigencia_ = datetime.now()
        Vigencia_time = datetime.timestamp(Vigencia_) # TIMESTAMP QR 
        md5 = hashlib.md5(str(UUID).encode('utf-8')).hexdigest()
        codigo = 'RECIBO-'+str(Recibo)+'-UUID-'+md5+'-Entrada-'+str(Vigencia_time)+'-'+str(Club)
        qr_parking = codigo
        generate_code_qr(qr_parking)
        if Recibo == "":
            flash("¡El recibo se encuentra vacio!", category='is-danger')
        else:
            flash("El código QR se genero de manera exitosa!!", category='alert alert-success')
        return redirect(url_for('caseta.caseta_registro_qr'))
    else:
        if file_exits(Routes.base_code_qr + Properties.base_filename_code_qr) is False:
            generate_code_qr('http://XXX/')
        return redirect(url_for('caseta.caseta_registro_qr'))

@caseta.route("/caseta/perdida_qr/caja", methods=['GET', 'POST'])
@login_required
def caseta_perdida_qr_caja():
    if request.method == 'POST' and request.form.get("club") == 'A3':
        # LLAMADA DE DATOS
        url_dos = day.url_api_app+'parking/perdidaQR/A3/caja'
        headers_dos = {'Authorization':'Bearer '+ day.resp_api_token}
        r_dos = requests.get(url_dos, headers=headers_dos)
        dato = r_dos.json()
        Recibo = dato['idRegistro']
        UUID = dato['id']
        #Club = dato['club']
        Club = 'A3'
        Hora_Entrada = dato['horaEntrada']
        Hora_Salida = dato['horaSalida']
        Costo_Total = dato['costoTotal']
        # CREACION DE CODIGO QR
        Vigencia_ = datetime.now()
        Vigencia_time = datetime.timestamp(Vigencia_) # TIMESTAMP QR 
        md5 = hashlib.md5(str(UUID).encode('utf-8')).hexdigest()
        codigo = 'RECIBO-'+str(Recibo)+'-UUID-'+md5+'-Entrada-'+str(Vigencia_time)+'-'+str(Club)
        qr_parking = codigo
        generate_code_qr(qr_parking)
        if Recibo == "":
            flash("¡El recibo se encuentra vacio!", category='is-danger')
        else:
            flash("El código QR se genero de manera exitosa!!", category='alert alert-success')
        return redirect(url_for('caseta.caseta_registro_qr'))
    elif  request.method == 'POST' and request.form.get("club") == 'A2':
        # LLAMADA DE DATOS
        url_dos = day.url_api_app+'parking/perdidaQR/A2/caja'
        headers_dos = {'Authorization':'Bearer '+ day.resp_api_token}
        r_dos = requests.get(url_dos, headers=headers_dos)
        dato = r_dos.json()
        Recibo = dato['idRegistro']
        UUID = dato['id']
        #Club = dato['club']
        Club = 'A3'
        Hora_Entrada = dato['horaEntrada']
        Hora_Salida = dato['horaSalida']
        Costo_Total = dato['costoTotal']
        # CREACION DE CODIGO QR
        Vigencia_ = datetime.now()
        Vigencia_time = datetime.timestamp(Vigencia_) # TIMESTAMP QR 
        md5 = hashlib.md5(str(UUID).encode('utf-8')).hexdigest()
        codigo = 'RECIBO-'+str(Recibo)+'-UUID-'+md5+'-Entrada-'+str(Vigencia_time)+'-'+str(Club)
        qr_parking = codigo
        generate_code_qr(qr_parking)
        if Recibo == "":
            flash("¡El recibo se encuentra vacio!", category='is-danger')
        else:
            flash("El código QR se genero de manera exitosa!!", category='alert alert-success')
        return redirect(url_for('caseta.caseta_registro_qr'))
    else:
        if file_exits(Routes.base_code_qr + Properties.base_filename_code_qr) is False:
            generate_code_qr('http://XXX/')
        return redirect(url_for('caseta.caseta_registro_qr'))

#===================================================================[QR CONSULTA INGRESOS]===================================================================#
@caseta.route("/caseta/consulta_ingresos", methods=['GET', 'POST'])
@login_required
def caseta_consulta_chip():
    if request.method == 'POST':
        today = date.today() # DIA ACTUAL
        fecha_title = today.strftime("%d %B, %Y, %A")
        invoice_ = datetime.now()
        invoice = datetime.timestamp(invoice_)
        # DATA FECHA
        fecha_inicio = request.form.get("Fecha_Inicio")
        fecha_fin = request.form.get("Fecha_Fin")
        turno = request.form.get("Turno")
        club = request.form.get("Club")
        from models.models import db
        # ALPHA 3
        chips_eventos_a3 = db.engine.execute(text("SELECT id_registro,club,costo_total,hora_entrada,turno FROM estacionamiento_externo \
                                            WHERE hora_entrada between '"+fecha_inicio+" 00:00:00.000' and '"+fecha_fin+" 23:59:59.999' \
                                            AND club='"+club+"' ORDER BY id_registro ASC"))
        dato_3_eventos = [row for row in chips_eventos_a3]
        # ALPHA 3
        chips_a3 = db.engine.execute(text("SELECT id_registro,club,costo_total,hora_entrada,turno FROM estacionamiento_externo \
                                            WHERE hora_entrada between '"+fecha_inicio+" 00:00:00.000' and '"+fecha_fin+" 23:59:59.999' \
                                            AND club='"+club+"' and qr is false ORDER BY id_registro ASC"))
        dato_3 = [row for row in chips_a3]
        # ALPHA 3 PERDIDA
        chips_perdida_a3 = db.engine.execute(text("SELECT id_registro,club,costo_total,hora_entrada,turno FROM estacionamiento_externo\
                                            WHERE hora_entrada between '"+fecha_inicio+" 00:00:00.000' and '"+fecha_fin+" 23:59:59.999'\
                                            AND club='"+club+"' and qr is true ORDER BY id_registro ASC"))
        dato_3_perdida = [row for row in chips_perdida_a3]
        # ALPHA 3 SUMA
        chips_suma_a3 = db.engine.execute(text("SELECT sum(costo_total)as costo_total FROM estacionamiento_externo \
                                            WHERE hora_entrada between '"+fecha_inicio+" 00:00:00.000' and '"+fecha_fin+" 23:59:59.999'\
                                            AND club='"+club+"'"))
        dato_3_suma = [row for row in chips_suma_a3]
        return render_template('caseta/consulta_chip.html', dato_3=dato_3, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, turno=turno, fecha_title=fecha_title, \
                                invoice=invoice, dato_3_perdida=dato_3_perdida, dato_3_suma=dato_3_suma, dato_3_eventos=dato_3_eventos)
    return render_template('caseta/consulta_menu.html')

@caseta.route("/caseta/consulta_corte/ingresos", methods=['GET', 'POST'])
@login_required
def caseta_consulta_corte_ingresos():
    from models.models import db
    # DATA FECHA
    fecha_inicio = request.form.get("Fecha_Inicio")
    fecha_fin = request.form.get("Fecha_Fin")
    club = request.form.get("Club")
    # CALL DATOS
    corte_a3_ = db.engine.execute(text("SELECT CC.*, to_char( RC.fecha_corte, 'HH24:MI:SS') AS fecha_corte_min FROM corte_caja AS CC \
                                        FULL OUTER JOIN Registro_cortes AS RC ON CC.folio = RC.id_corte \
                                        WHERE cc.club='"+club+"' AND cc.fecha BETWEEN '"+fecha_inicio+"' AND '"+fecha_fin+"'  ORDER BY cc.folio::integer"))
    corte_a3 = [row for row in corte_a3_]
    return render_template('caseta/Corte/consulta.html', corte_a3=corte_a3)

@caseta.route("/caseta/consulta_corte/ingresos/view", methods=['GET', 'POST'])
@login_required
def caseta_consulta_corte_ingresos_view():
    if request.method == 'POST':
        from models.models import db
        # TITULOS
        today = date.today() # DIA ACTUAL
        fecha_title = today.strftime("%d %B, %Y, %A")
        invoice_ = datetime.now()
        invoice = datetime.timestamp(invoice_)
        # DATOS
        Club = request.form.get("Club")
        Fecha = request.form.get("Fecha")
        Folio = request.form.get("Folio")
        Tipo = request.form.get("Tipo")
        # ENDPOINT
        url = day.url_api_app+'parking/registroPorFolio'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'club': Club, 'folio':Folio}
        r = requests.post(url, headers=headers, json=datos_envio)
        respuesta = r.json()
        # ENDPOINT SUMA
        url_sum = day.url_api_app+'parking/datosQR'
        headers_sum = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio_sum = {'club': Club, 'folio':Folio}
        r_sum = requests.post(url_sum, headers=headers_sum, json=datos_envio_sum)
        respuesta_suma = r_sum.json()
        return render_template('caseta/Vista_Corte/consulta_corte.html', Folio=Folio, fecha_title=fecha_title, invoice=invoice, Fecha=Fecha,\
                                         Tipo=Tipo, respuesta=respuesta, respuesta_suma=respuesta_suma)
    return redirect(url_for('caseta.caseta_consulta_chip'))
    
