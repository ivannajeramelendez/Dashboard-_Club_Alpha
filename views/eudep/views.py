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

eudep = Blueprint('eudep', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

@eudep.route("/eudep/oxoo", methods=["GET", "POST"])
def eudep_oxxo():
    return render_template('Eudep/oxxo.html')

@eudep.route("/eudep/oxoo/enviar", methods=["GET", "POST"])
def eudep_oxxo_enviar():
    #conekta.api_key = "XXX"    # Clave Privada  PRUEBAS
    conekta.api_key = "XXX"    # Clave Privada PRODUCTIVO 
    conekta.locale = "es"
    # TOMA DE DATOS
    importe_data = (float(request.form.get("monto")))   # IMPORTE
    importe_fort = (importe_data*100)                     # IMPORTE
    importe_fin = ('{0:.0f}'.format(float(importe_fort))) # IMPORTE
    importe = int(importe_fin)                 # IMPORTE
    Tipo_de_pago = str(request.form.get("tipo_pago"))
    Cliente = str(request.form.get("cliente"))
    Telefono = str(request.form.get("telefono"))
    Direccion = str(request.form.get("direccion"))
    Correo_cliente = str(request.form.get("correo"))
    dias_pago_oxxo = int(request.form.get("dias_pago"))
    # DIAS DE PAGO
    thirty_days_from_now = int((datetime.now() + timedelta(days=dias_pago_oxxo)).timestamp())
    if Cliente == '':
        redirect(url_for('eudep.eudep_oxxo'))
    else:
        # ENVIO A CONEKTA
        data = {
        "line_items": [
            {
                "name": "Pago Oxxo EUDEP",
                "description": "Pago Oxxo EUDEP",
                "unit_price": importe,
                "quantity": 1,
                "sku": "Pago Oxxo EUDEP",
                "category": "Oxxo"
            }
        ],
        "shipping_lines":[
            {
            "amount": 0,
            "tracking_number": "OxxoPay",
            "carrier": "Fundacion Club Alpha",
            "method": "Pago Oxxo Pay"
            }],
        "customer_info":{
            "name": Cliente,
            "phone": "+525533445566",
            "email": Correo_cliente
            },
        "shipping_contact":{
            "phone" : "2223953654",
            "receiver": "EUDEP",
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
        "currency" : "mxn"
        }
        order = conekta.Order.create(data)
        order = order
        datos_tipo = (order.charges[0].payment_method.service_name)
        datos_referencia = (order.charges[0].payment_method.reference)
        datos_monto = (str(order.amount/100), order.currency)
        flash('Referencia creada con exito:'+datos_referencia, category='alert alert-success')
    return redirect(url_for('eudep.eudep_oxxo'))
