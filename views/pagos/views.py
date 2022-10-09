from flask import Flask, render_template, redirect, url_for, request, abort, flash,\
    session, Response, Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required,\
    current_user
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from app import api, day
import requests
import json
 #===================================================================[CONEKTA]===================================================================#
import conekta
 #===================================================================[OPENPAY]===================================================================#
#import openpay
#openpay.api_key = "XXX" # PRUEBAS
#openpay.verify_ssl_certs = False
#openpay.merchant_id = "XXX"
 #===================================================================[FORMULARIOS]===================================================================#
from datetime import datetime, timedelta
from forms.forms import *
app = Flask(__name__)
app.config.from_object(api)

pagos = Blueprint('pagos', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

#===================================================================[OXXO]===================================================================#
@pagos.route("/pagos/generar_referencia")
@pagos.route("/pagos/generar_referencia/referencia", methods=['GET', 'POST'])
@login_required
def pagos_busqueda():
    form = FormAcceso()
    dias = FormDiasOxxo()
    if request.method == 'POST':
        id_cliente = request.form.get("id")
        id_client = str(id_cliente)
        # CONEXION DATAFLOW
        auth_data = {"IdCliente":id_client,"Token":"XXX"}
        r_dos = requests.get('http://XXX'+id_client, data=auth_data)
        resp_dataflow = requests.post('http://XXX', data=auth_data)
        if resp_dataflow.status_code == 200:
            try:
                # DESENCADENAR JSON
                dato_dataflow = resp_dataflow.json()
                resp_dos = r_dos.json()
                # DATOS DATAFLOW
                NoPedido = dato_dataflow['NoPedido']
                IDCliente = dato_dataflow['IDCliente']
                importe_total_api = sum(d['Importe'] for d in dato_dataflow['Detalle'] if d)
                importe = ('{0:.2f}'.format(float(importe_total_api)))
                correo_cliente = dato_dataflow['CorreoCliente']
                # DATOS CLIENTE
                nombre_cliente = resp_dos['Nombre']+' '+resp_dos['ApellidoPaterno']+' '+resp_dos['ApellidoMaterno']
                membresia = resp_dos['NoMembresia']
                return render_template('pagos/generador.html', form=form, dias=dias, NoPedido=NoPedido, importe=importe, correo_cliente=correo_cliente, IDCliente=IDCliente,
                                                            nombre_cliente=nombre_cliente, membresia=membresia)
            except ValueError:
                redirect(url_for('pagos.pagos_busqueda'))
    return render_template('pagos/generador.html', form=form, dias=dias)

@pagos.route("/pagos/generar_referencia/aplicar", methods=['GET', 'POST'])
@login_required
def pagos_aplicar():
    conekta.api_key = "XXX"    # Clave Privada
    conekta.locale = "es"
    # TOMA DE DATOS
    NoPedido = int(request.form.get("NoPedido"))
    IDCliente = int(request.form.get("IDCliente"))
    importe_data = (float(request.form.get("importe")))   # IMPORTE
    importe_fort = (importe_data*100)                     # IMPORTE
    importe_fin = ('{0:.0f}'.format(float(importe_fort))) # IMPORTE
    importe = int(importe_fin)                            # IMPORTE
    correo_cliente = str(request.form.get("correo_cliente"))
    dias_pago_oxxo = int(request.form.get("dias_para_pago"))
    # DATOS CLIENTE
    nombre_cliente = str(request.form.get("nombre_cliente"))
    membresia = int(request.form.get("membresia"))
    # DIAS DE PAGO
    thirty_days_from_now = int((datetime.now() + timedelta(days=dias_pago_oxxo)).timestamp())
    if IDCliente == '':
        redirect(url_for('pagos.pagos_busqueda'))
    else:
        # ENVIO A CONEKTA
        data = {
        "line_items": [
            {
                "name": "Pago Oxxo Club Alpha",
                "description": "Pago Oxxo Club Alpha",
                "unit_price": importe,
                "quantity": 1,
                "sku": "Pago Oxxo Club Alpha",
                "category": "Oxxo"
            }
        ],
        "shipping_lines":[
            {
            "amount": 0,
            "tracking_number": "OxxoPay",
            "carrier": "Fundacion Club Alpha Sports Plaza",
            "method": "Pago Oxxo Pay"
            }],
        "customer_info":{
            "name": nombre_cliente,
            "phone": "+525533445566",
            "email": correo_cliente
            },
        "shipping_contact":{
            "phone" : "2223953654",
            "receiver": "Fundacion Club Alpha",
            "between_streets": " Zona Sin Asignación de Nombre de Col 69",
            "address": {
                "street1": "Guadalupe Hidalgo",
                "state": "Puebla",
                "country": "MX",
                "postal_code": "72490"
            }
        },
        "charges": [{
            "payment_method":{
            "type":"oxxo_cash",
            "expires_at": thirty_days_from_now
            }
        }],
        "currency" : "mxn",
        "metadata" : 
            {
                "NoPedido": NoPedido,
                "Monto": importe,
                "IDCliente": IDCliente,
                "Membresia": membresia
            }
        }
        order = conekta.Order.create(data)
        order = order
        flash('¡Se genero exitosamente la referencia de pago OxxoPay!', category='alert alert-success')
        return redirect(url_for('pagos.pagos_busqueda'))

#===================================================================[OPEN PAY]===================================================================#
@pagos.route("/pagos/generar_referencia/openpay")
@pagos.route("/pagos/generar_referencia/referencia/_openpay", methods=['GET', 'POST'])
@login_required
def pagos_busqueda_openpay():
    form = FormAcceso()
    dias = FormDiasOxxo()
    if request.method == 'POST':
        id_cliente = request.form.get("id")
        id_client = str(id_cliente)
        # CONEXION DATAFLOW
        auth_data = {"IdCliente":id_client,"Token":"XXX"}
        resp_dataflow = requests.post('http://XXX', data=auth_data) #PRUEBAS
        #resp_dataflow = requests.post('http://XXX', data=auth_data) #PRODUCTIVO
        r_dos = requests.get('http://192.168.20.44/ServiciosClubAlpha/api/Miembro/'+id_client, data=auth_data)
        if resp_dataflow.status_code == 200:
            try:
                # DESENCADENAR JSON
                dato_dataflow = resp_dataflow.json()
                resp_dos = r_dos.json()
                # DATOS DATAFLOW
                NoPedido = dato_dataflow['NoPedido']
                IDCliente = dato_dataflow['IDCliente']
                importe_total_api = sum(d['Importe'] for d in dato_dataflow['Detalle'] if d)
                importe = ('{0:.2f}'.format(float(importe_total_api)))
                correo_cliente = dato_dataflow['CorreoCliente']
                # DATOS CLIENTE
                nombre_cliente = resp_dos['Nombre']+' '+resp_dos['ApellidoPaterno']+' '+resp_dos['ApellidoMaterno']
                membresia = resp_dos['NoMembresia']
                return render_template('pagos/generador_openpay.html', form=form, dias=dias, NoPedido=NoPedido, importe=importe, correo_cliente=correo_cliente, IDCliente=IDCliente,
                                                            nombre_cliente=nombre_cliente, membresia=membresia)
            except ValueError:
                redirect(url_for('pagos.pagos_busqueda_openpay'))
    return render_template('pagos/generador_openpay.html', form=form, dias=dias)

@pagos.route("/pagos/generar_referencia/aplicar/openpay", methods=['GET', 'POST'])
@login_required
def pagos_aplicar_openpay():
    # TOMA DE DATOS
    NoPedido = int(request.form.get("NoPedido"))
    IDCliente = int(request.form.get("IDCliente"))
    importe = (float(request.form.get("importe")))   # IMPORTE
    correo_cliente = str(request.form.get("correo_cliente"))
    #dias_pago_oxxo = int(request.form.get("dias_para_pago"))
    # DATOS CLIENTE
    nombre_cliente = str(request.form.get("nombre_cliente"))
    membresia = int(request.form.get("membresia"))
    # DIAS DE PAGO
    #thirty_days_from_now = int((datetime.now() + timedelta(days=dias_pago_oxxo)).timestamp())
    # TOKEN
    url_token = day.url_api_app+'auth/login'
    datos_token = {"nombreUsuario": "XXX", "password": "XXX"}
    r_token = requests.post(url_token, json=datos_token)
    resp_token = r_token.json()
    resp_api_token = resp_token['token']
    if IDCliente == '':
        redirect(url_for('pagos.pagos_busqueda_openpay'))
    else:
        #charge = openpay.Charge.create_as_merchant(
        #    method="store", 
        #    amount=importe, #CARGO
        #    description=NoPedido,
        #    customer={
        #        "name":nombre_cliente,
        #        "email":correo_cliente,
        #        "external_id": membresia,
        #    }
        #)
        # DATOS FROM
        #importe
        #thirty_days_from_now
        #NoPedido
        #importe
        #IDCliente
        #membresia
        #charge = charge
        #print(charge)
        #print(charge.operation_date)
        #print(charge.payment_method.reference)
        #print(charge.payment_method.barcode_url)
        #print(charge.operation_date)
        #print(charge.id)
        # REGISTRO CLIENTE APP
        url = day.url_api_app+'pagos/openpay'
        headers = {'Authorization':'Bearer '+resp_api_token}
        datos_envio = {'idcliente': IDCliente, 'monto': importe}
        r = requests.post(url, headers=headers, json=datos_envio)
        dato = r.json()
        print(dato)
        flash('¡Se genero exitosamente la referencia de pago OpenPay!', category='alert alert-success')
        return redirect(url_for('pagos.pagos_busqueda_openpay'))
