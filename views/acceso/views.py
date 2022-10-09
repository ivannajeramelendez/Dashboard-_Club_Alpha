from flask import Flask, render_template, redirect, url_for, request, abort, flash,\
    session, Response, Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required,\
    current_user
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from app import api, day
import requests
    # FORMULARIOS
from forms.forms import *
app = Flask(__name__)
app.config.from_object(api)

acceso = Blueprint('acceso', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

@acceso.route("/acceso/estado_del_cliente/estado_de_acceso", methods=['GET', 'POST'])
@login_required
def acceso_busqueda():
    form = FormAcceso()
    if request.method == 'POST':
        # REGISTRO CLASE
        id_cliente = request.form.get("id")
        id_client = str(id_cliente)
        url = 'http://XXX'+id_client
        headers = {'Content-type': 'application/json','Accept': 'application/json'}
        datos_envio = {"Token":"77D5BDD4-1FEE-4A47-86A0-1E7D19EE1C74"}
        r = requests.get(url, headers=headers, json=datos_envio)
        dato = r.json()
        # REGISTRO CLIENTE APP
        url_dos = day.url_api_app+'alpha/updateCliente/'+id_client
        headers_dos = {'Authorization':'Bearer '+ day.resp_api_token}
        r_dos = requests.get(url_dos, headers=headers_dos)
        # DATOS
        mem = dato['NoMembresia']
        nom = dato['Nombre']
        ape = dato['ApellidoPaterno']
        ape_2 = dato['ApellidoMaterno']
        club = dato['Club']['Nombre']
        tipo = dato['TipoMembresia']['Nombre']
        cate = dato['Categoria']['Nombre']
        esta = dato['EstatusCliente']['Nombre']
        # 2
        cob = dato['EstatusCobranza']['Nombre']
        acc = dato['EstatusAcceso']
        fot = dato['UrlFoto']
        mail = dato['EMail']
        fin = dato['FechaFinAcceso']
        nac = dato['FechaNacimiento']
        return render_template('acceso/acceso.html', form=form, dato=dato,mem=mem, nom=nom, ape=ape, ape_2=ape_2, club=club, tipo=tipo, cate=cate, esta=esta, cob=cob, acc=acc, fot=fot, mail=mail,
                                                fin=fin, nac=nac)
    else:
        redirect('acceso.acceso_busqueda')
    return render_template('acceso/acceso.html', form=form)

@acceso.route("/acceso/estado_de_cuenta/estado_de_cuenta", methods=['GET', 'POST'])
@login_required
def acceso_estado_de_cuenta():
    form = FormAcceso()
    if request.method == 'POST':
        id_cliente = request.form.get("id")
        id_client = str(id_cliente)
        url = 'http://XXX'
        headers = {'Content-type': 'application/json','Accept': 'application/json'}
        datos_envio = {"IdCliente":id_client, "Token":"77D5BDD4-1FEE-4A47-86A0-1E7D19EE1C74"}
        r = requests.post(url, headers=headers, json=datos_envio)
        dato = r.json()
        print(dato)
        return render_template('acceso/estado_de_cuenta.html', form=form, dato=dato)
    else:
        redirect('acceso.acceso_estado_de_cuenta')
    return render_template('acceso/estado_de_cuenta.html', form=form)
