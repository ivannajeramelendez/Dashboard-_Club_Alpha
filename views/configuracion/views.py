from flask import Flask, render_template, redirect, url_for, request, abort, flash,\
    session, Response, Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required,\
    current_user
from sqlalchemy.sql.expression import asc
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, desc
from sqlalchemy.sql.functions import concat
from sqlalchemy import DateTime, select
from app import api, day
from datetime import date, timedelta
import requests
import datetime
    # FORMULARIOS
from forms.forms import *
app = Flask(__name__)
app.config.from_object(api)
app.config.from_object(day)

configuracion = Blueprint('configuracion', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

# ===========================================================================[MENU]=========================================================================== #
@configuracion.route("/configuracion/club")
@login_required
def configuracion_menu():
    return render_template('config/Menu/menu.html')

# ===========================================================================[CONFIGURACION]=========================================================================== #
@configuracion.route("/configuracion/inicio/cancelar_sala", methods=['GET', 'POST'])
@login_required
def configuracion_cancelar_sala():
    from models.models import db
    # DIAS
    dias_dash_ = db.engine.execute(("SELECT nombre,fecha FROM dias_semana"))
    dias_dash = [row for row in dias_dash_]
    lunes_dash = dias_dash[0]['fecha']
    martes_dash = dias_dash[1]['fecha']
    miercoles_dash = dias_dash[2]['fecha']
    jueves_dash = dias_dash[3]['fecha']
    viernes_dash = dias_dash[4]['fecha']
    sabado_dash = dias_dash[5]['fecha']
    domingo_dash = dias_dash[6]['fecha']
    # DIAS TITULOS
    lunes_day = lunes_dash
    martes_day = martes_dash
    miercoles_day = miercoles_dash
    jueves_day = jueves_dash
    viernes_day = viernes_dash
    sabado_day = sabado_dash
    domingo_day = domingo_dash
    # OBTENER DATOS API
    url = day.url_api_app+'citas/obtenerClases'
    headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
    if current_user.alpha_2 == 1 and current_user.user_configuracion == 1:
        # CLUB
        club = 'Club Alpha 2'
        # DIAS
        parametros_lunes = {'club':'Club Alpha 2', 'dia':lunes_day}
        parametros_martes = {'club':'Club Alpha 2', 'dia':martes_day}
        parametros_miercoles = {'club':'Club Alpha 2', 'dia':miercoles_day}
        parametros_jueves = {'club':'Club Alpha 2', 'dia':jueves_day}
        parametros_viernes = {'club':'Club Alpha 2', 'dia':viernes_day}
        parametros_sabado = {'club':'Club Alpha 2', 'dia':sabado_day}
        parametros_domingo = {'club':'Club Alpha 2', 'dia':domingo_day}
        # RESPUESTA
        lunes = requests.get(url, headers=headers, params=parametros_lunes)
        martes = requests.get(url, headers=headers, params=parametros_martes)
        miercoles = requests.get(url, headers=headers, params=parametros_miercoles)
        jueves = requests.get(url, headers=headers, params=parametros_jueves)
        viernes = requests.get(url, headers=headers, params=parametros_viernes)
        sabado = requests.get(url, headers=headers, params=parametros_sabado)
        domingo = requests.get(url, headers=headers, params=parametros_domingo)
        # SERIALIZACION
        lunes_api = lunes.json()
        martes_api = martes.json()
        miercoles_api = miercoles.json()
        jueves_api = jueves.json()
        viernes_api = viernes.json()
        sabado_api = sabado.json()
        domingo_api = domingo.json()
        # REGISTRO CLASE
        if request.method == 'POST':
            # DATOS
            Apartado_agenda = request.form.get('dia_apartado')
            Apartado_act = request.form.get('sala_apartado')
            # ENVIO CITA
            url = day.url_api_app+'citas/cancelarClase'
            headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
            datos_envio = {'id': Apartado_act, 'dia':Apartado_agenda}
            r = requests.post(url, headers=headers, json=datos_envio)
            text = request.form.get("dia_apartado")
            if text == "":
                flash("El campo texto es obligatorio(*)", category='alert alert-danger')
            else:
                dato = r.json()
                resp_api = dato['Respuesta']
                flash(resp_api, category='alert alert-success')
                r.json()
                return redirect(url_for('configuracion.configuracion_cancelar_sala'))
        else:
            return render_template('config/Cancelar/clase.html', lunes_api=lunes_api, martes_api=martes_api, miercoles_api=miercoles_api, 
                                        jueves_api=jueves_api, viernes_api=viernes_api, sabado_api=sabado_api, domingo_api=domingo_api,
                                        lunes_day=lunes_day, martes_day=martes_day, miercoles_day=miercoles_day, jueves_day=jueves_day, 
                                        viernes_day=viernes_day, sabado_day=sabado_day, domingo_day=domingo_day, club=club)
    elif current_user.alpha_3 == 1 and current_user.user_configuracion == 1:
        # CLUB
        club = 'Club Alpha 3'
        # DIAS
        parametros_lunes = {'club':'Club Alpha 3', 'dia':lunes_day}
        parametros_martes = {'club':'Club Alpha 3', 'dia':martes_day}
        parametros_miercoles = {'club':'Club Alpha 3', 'dia':miercoles_day}
        parametros_jueves = {'club':'Club Alpha 3', 'dia':jueves_day}
        parametros_viernes = {'club':'Club Alpha 3', 'dia':viernes_day}
        parametros_sabado = {'club':'Club Alpha 3', 'dia':sabado_day}
        parametros_domingo = {'club':'Club Alpha 3', 'dia':domingo_day}
        # RESPUESTA
        lunes = requests.get(url, headers=headers, params=parametros_lunes)
        martes = requests.get(url, headers=headers, params=parametros_martes)
        miercoles = requests.get(url, headers=headers, params=parametros_miercoles)
        jueves = requests.get(url, headers=headers, params=parametros_jueves)
        viernes = requests.get(url, headers=headers, params=parametros_viernes)
        sabado = requests.get(url, headers=headers, params=parametros_sabado)
        domingo = requests.get(url, headers=headers, params=parametros_domingo)
        # SERIALIZACION
        lunes_api = lunes.json()
        martes_api = martes.json()
        miercoles_api = miercoles.json()
        jueves_api = jueves.json()
        viernes_api = viernes.json()
        sabado_api = sabado.json()
        domingo_api = domingo.json()
        # REGISTRO CLASE
        if request.method == 'POST':
            # DATOS
            Apartado_agenda = request.form.get('dia_apartado')
            Apartado_act = request.form.get('sala_apartado')
            # ENVIO CITA
            url = day.url_api_app+'citas/cancelarClase'
            headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
            datos_envio = {'id': Apartado_act, 'dia':Apartado_agenda}
            r = requests.post(url, headers=headers, json=datos_envio)
            text = request.form.get("dia_apartado")
            if text == "":
                flash("El campo texto es obligatorio(*)", category='alert alert-danger')
            else:
                dato = r.json()
                resp_api = dato['Respuesta']
                flash(resp_api, category='alert alert-success')
                r.json()
                return redirect(url_for('configuracion.configuracion_cancelar_sala'))
        else:
            return render_template('config/Cancelar/clase.html', lunes_api=lunes_api, martes_api=martes_api, miercoles_api=miercoles_api, 
                                        jueves_api=jueves_api, viernes_api=viernes_api, sabado_api=sabado_api, domingo_api=domingo_api,
                                        lunes_day=lunes_day, martes_day=martes_day, miercoles_day=miercoles_day, jueves_day=jueves_day, 
                                        viernes_day=viernes_day, sabado_day=sabado_day, domingo_day=domingo_day, club=club)
    elif current_user.alpha_4 == 1 and current_user.user_configuracion == 1:
        # CLUB
        club = 'Sports Plaza'
        # DIAS
        parametros_lunes = {'club':'Sports Plaza', 'dia':lunes_day}
        parametros_martes = {'club':'Sports Plaza', 'dia':martes_day}
        parametros_miercoles = {'club':'Sports Plaza', 'dia':miercoles_day}
        parametros_jueves = {'club':'Sports Plaza', 'dia':jueves_day}
        parametros_viernes = {'club':'Sports Plaza', 'dia':viernes_day}
        parametros_sabado = {'club':'Sports Plaza', 'dia':sabado_day}
        parametros_domingo = {'club':'Sports Plaza', 'dia':domingo_day}
        # RESPUESTA
        lunes = requests.get(url, headers=headers, params=parametros_lunes)
        martes = requests.get(url, headers=headers, params=parametros_martes)
        miercoles = requests.get(url, headers=headers, params=parametros_miercoles)
        jueves = requests.get(url, headers=headers, params=parametros_jueves)
        viernes = requests.get(url, headers=headers, params=parametros_viernes)
        sabado = requests.get(url, headers=headers, params=parametros_sabado)
        domingo = requests.get(url, headers=headers, params=parametros_domingo)
        # SERIALIZACION
        lunes_api = lunes.json()
        martes_api = martes.json()
        miercoles_api = miercoles.json()
        jueves_api = jueves.json()
        viernes_api = viernes.json()
        sabado_api = sabado.json()
        domingo_api = domingo.json()
        # REGISTRO CLASE
        if request.method == 'POST':
            # DATOS
            Apartado_agenda = request.form.get('dia_apartado')
            Apartado_act = request.form.get('sala_apartado')
            # ENVIO CITA
            url = day.url_api_app+'citas/cancelarClase'
            headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
            datos_envio = {'id': Apartado_act, 'dia':Apartado_agenda}
            r = requests.post(url, headers=headers, json=datos_envio)
            text = request.form.get("dia_apartado")
            if text == "":
                flash("El campo texto es obligatorio(*)", category='alert alert-danger')
            else:
                dato = r.json()
                resp_api = dato['Respuesta']
                flash(resp_api, category='alert alert-success')
                r.json()
                return redirect(url_for('configuracion.configuracion_cancelar_sala'))
        else:
            return render_template('config/Cancelar/clase.html', lunes_api=lunes_api, martes_api=martes_api, miercoles_api=miercoles_api, 
                                        jueves_api=jueves_api, viernes_api=viernes_api, sabado_api=sabado_api, domingo_api=domingo_api,
                                        lunes_day=lunes_day, martes_day=martes_day, miercoles_day=miercoles_day, jueves_day=jueves_day, 
                                        viernes_day=viernes_day, sabado_day=sabado_day, domingo_day=domingo_day, club=club)
    elif current_user.cimera == 1 and current_user.user_configuracion == 1:
        # CLUB
        club = 'CIMERA'
        # DIAS
        parametros_lunes = {'club':'CIMERA', 'dia':lunes_day}
        parametros_martes = {'club':'CIMERA', 'dia':martes_day}
        parametros_miercoles = {'club':'CIMERA', 'dia':miercoles_day}
        parametros_jueves = {'club':'CIMERA', 'dia':jueves_day}
        parametros_viernes = {'club':'CIMERA', 'dia':viernes_day}
        parametros_sabado = {'club':'CIMERA', 'dia':sabado_day}
        parametros_domingo = {'club':'CIMERA', 'dia':domingo_day}
        # RESPUESTA
        lunes = requests.get(url, headers=headers, params=parametros_lunes)
        martes = requests.get(url, headers=headers, params=parametros_martes)
        miercoles = requests.get(url, headers=headers, params=parametros_miercoles)
        jueves = requests.get(url, headers=headers, params=parametros_jueves)
        viernes = requests.get(url, headers=headers, params=parametros_viernes)
        sabado = requests.get(url, headers=headers, params=parametros_sabado)
        domingo = requests.get(url, headers=headers, params=parametros_domingo)
        # SERIALIZACION
        lunes_api = lunes.json()
        martes_api = martes.json()
        miercoles_api = miercoles.json()
        jueves_api = jueves.json()
        viernes_api = viernes.json()
        sabado_api = sabado.json()
        domingo_api = domingo.json()
        # REGISTRO CLASE
        if request.method == 'POST':
            # DATOS
            Apartado_agenda = request.form.get('dia_apartado')
            Apartado_act = request.form.get('sala_apartado')
            # ENVIO CITA
            url = day.url_api_app+'citas/cancelarClase'
            headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
            datos_envio = {'id': Apartado_act, 'dia':Apartado_agenda}
            r = requests.post(url, headers=headers, json=datos_envio)
            text = request.form.get("dia_apartado")
            if text == "":
                flash("El campo texto es obligatorio(*)", category='alert alert-danger')
            else:
                dato = r.json()
                resp_api = dato['Respuesta']
                flash(resp_api, category='alert alert-success')
                r.json()
                return redirect(url_for('configuracion.configuracion_cancelar_sala'))
        else:
            return render_template('config/Cancelar/clase.html', lunes_api=lunes_api, martes_api=martes_api, miercoles_api=miercoles_api, 
                                        jueves_api=jueves_api, viernes_api=viernes_api, sabado_api=sabado_api, domingo_api=domingo_api,
                                        lunes_day=lunes_day, martes_day=martes_day, miercoles_day=miercoles_day, jueves_day=jueves_day, 
                                        viernes_day=viernes_day, sabado_day=sabado_day, domingo_day=domingo_day, club=club)

@configuracion.route("/configuracion/inicio/sports_plaza/restablecer_sala", methods=['GET', 'POST'])
@login_required
def configuracion_restablecer_sala():
    from models.models import db
    # DIAS
    dias_dash_ = db.engine.execute(("SELECT nombre,fecha FROM dias_semana"))
    dias_dash = [row for row in dias_dash_]
    lunes_dash = dias_dash[0]['fecha']
    martes_dash = dias_dash[1]['fecha']
    miercoles_dash = dias_dash[2]['fecha']
    jueves_dash = dias_dash[3]['fecha']
    viernes_dash = dias_dash[4]['fecha']
    sabado_dash = dias_dash[5]['fecha']
    domingo_dash = dias_dash[6]['fecha']
    # DIAS TITULOS
    lunes_day = lunes_dash
    martes_day = martes_dash
    miercoles_day = miercoles_dash
    jueves_day = jueves_dash
    viernes_day = viernes_dash
    sabado_day = sabado_dash
    domingo_day = domingo_dash
    # OBTENER DATOS API
    url = day.url_api_app+'citas/obtenerClasesCanceladas'
    headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
    if current_user.alpha_2 == 1 and current_user.user_configuracion == 1:
        # CLUB
        club = 'Club Alpha 2'
        # DIAS
        parametros_lunes = {'club':'Club Alpha 2', 'dia':lunes_day}
        parametros_martes = {'club':'Club Alpha 2', 'dia':martes_day}
        parametros_miercoles = {'club':'Club Alpha 2', 'dia':miercoles_day}
        parametros_jueves = {'club':'Club Alpha 2', 'dia':jueves_day}
        parametros_viernes = {'club':'Club Alpha 2', 'dia':viernes_day}
        parametros_sabado = {'club':'Club Alpha 2', 'dia':sabado_day}
        parametros_domingo = {'club':'Club Alpha 2', 'dia':domingo_day}
        # RESPUESTA
        lunes = requests.get(url, headers=headers, params=parametros_lunes)
        martes = requests.get(url, headers=headers, params=parametros_martes)
        miercoles = requests.get(url, headers=headers, params=parametros_miercoles)
        jueves = requests.get(url, headers=headers, params=parametros_jueves)
        viernes = requests.get(url, headers=headers, params=parametros_viernes)
        sabado = requests.get(url, headers=headers, params=parametros_sabado)
        domingo = requests.get(url, headers=headers, params=parametros_domingo)
        # SERIALIZACION
        lunes_api = lunes.json()
        martes_api = martes.json()
        miercoles_api = miercoles.json()
        jueves_api = jueves.json()
        viernes_api = viernes.json()
        sabado_api = sabado.json()
        domingo_api = domingo.json()
        # REGISTRO CLASE
        if request.method == 'POST':
            # DATOS
            Apartado_agenda = request.form.get('dia_apartado')
            Apartado_act = request.form.get('sala_apartado')
            # ENVIO CITA
            url = day.url_api_app+'citas/restablecerClase'
            headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
            datos_envio = {'id': Apartado_act, 'dia':Apartado_agenda}
            r = requests.post(url, headers=headers, json=datos_envio)
            text = request.form.get("dia_apartado")
            if text == "":
                flash("El campo texto es obligatorio(*)", category='alert alert-danger')
            else:
                dato = r.json()
                resp_api = dato['Respuesta']
                flash(resp_api, category='alert alert-success')
                r.json()
                return redirect(url_for('configuracion.configuracion_restablecer_sala'))
        else:
            return render_template('config/Restablecer/clase.html', lunes_api=lunes_api, martes_api=martes_api, miercoles_api=miercoles_api, 
                                        jueves_api=jueves_api, viernes_api=viernes_api, sabado_api=sabado_api, domingo_api=domingo_api,
                                        lunes_day=lunes_day, martes_day=martes_day, miercoles_day=miercoles_day, jueves_day=jueves_day, 
                                        viernes_day=viernes_day, sabado_day=sabado_day, domingo_day=domingo_day, club=club)
    elif current_user.alpha_3 == 1 and current_user.user_configuracion == 1:
        # CLUB
        club = 'Club Alpha 3'
        # DIAS
        parametros_lunes = {'club':'Club Alpha 3', 'dia':lunes_day}
        parametros_martes = {'club':'Club Alpha 3', 'dia':martes_day}
        parametros_miercoles = {'club':'Club Alpha 3', 'dia':miercoles_day}
        parametros_jueves = {'club':'Club Alpha 3', 'dia':jueves_day}
        parametros_viernes = {'club':'Club Alpha 3', 'dia':viernes_day}
        parametros_sabado = {'club':'Club Alpha 3', 'dia':sabado_day}
        parametros_domingo = {'club':'Club Alpha 3', 'dia':domingo_day}
        # RESPUESTA
        lunes = requests.get(url, headers=headers, params=parametros_lunes)
        martes = requests.get(url, headers=headers, params=parametros_martes)
        miercoles = requests.get(url, headers=headers, params=parametros_miercoles)
        jueves = requests.get(url, headers=headers, params=parametros_jueves)
        viernes = requests.get(url, headers=headers, params=parametros_viernes)
        sabado = requests.get(url, headers=headers, params=parametros_sabado)
        domingo = requests.get(url, headers=headers, params=parametros_domingo)
        # SERIALIZACION
        lunes_api = lunes.json()
        martes_api = martes.json()
        miercoles_api = miercoles.json()
        jueves_api = jueves.json()
        viernes_api = viernes.json()
        sabado_api = sabado.json()
        domingo_api = domingo.json()
        # REGISTRO CLASE
        if request.method == 'POST':
            # DATOS
            Apartado_agenda = request.form.get('dia_apartado')
            Apartado_act = request.form.get('sala_apartado')
            # ENVIO CITA
            url = day.url_api_app+'citas/restablecerClase'
            headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
            datos_envio = {'id': Apartado_act, 'dia':Apartado_agenda}
            r = requests.post(url, headers=headers, json=datos_envio)
            text = request.form.get("dia_apartado")
            if text == "":
                flash("El campo texto es obligatorio(*)", category='alert alert-danger')
            else:
                dato = r.json()
                resp_api = dato['Respuesta']
                flash(resp_api, category='alert alert-success')
                r.json()
                return redirect(url_for('configuracion.configuracion_restablecer_sala'))
        else:
            return render_template('config/Restablecer/clase.html', lunes_api=lunes_api, martes_api=martes_api, miercoles_api=miercoles_api, 
                                        jueves_api=jueves_api, viernes_api=viernes_api, sabado_api=sabado_api, domingo_api=domingo_api,
                                        lunes_day=lunes_day, martes_day=martes_day, miercoles_day=miercoles_day, jueves_day=jueves_day, 
                                        viernes_day=viernes_day, sabado_day=sabado_day, domingo_day=domingo_day, club=club)
    elif current_user.alpha_4 == 1 and current_user.user_configuracion == 1:
        # CLUB
        club = 'Sports Plaza'
        # DIAS
        parametros_lunes = {'club':'Sports Plaza', 'dia':lunes_day}
        parametros_martes = {'club':'Sports Plaza', 'dia':martes_day}
        parametros_miercoles = {'club':'Sports Plaza', 'dia':miercoles_day}
        parametros_jueves = {'club':'Sports Plaza', 'dia':jueves_day}
        parametros_viernes = {'club':'Sports Plaza', 'dia':viernes_day}
        parametros_sabado = {'club':'Sports Plaza', 'dia':sabado_day}
        parametros_domingo = {'club':'Sports Plaza', 'dia':domingo_day}
        # RESPUESTA
        lunes = requests.get(url, headers=headers, params=parametros_lunes)
        martes = requests.get(url, headers=headers, params=parametros_martes)
        miercoles = requests.get(url, headers=headers, params=parametros_miercoles)
        jueves = requests.get(url, headers=headers, params=parametros_jueves)
        viernes = requests.get(url, headers=headers, params=parametros_viernes)
        sabado = requests.get(url, headers=headers, params=parametros_sabado)
        domingo = requests.get(url, headers=headers, params=parametros_domingo)
        # SERIALIZACION
        lunes_api = lunes.json()
        martes_api = martes.json()
        miercoles_api = miercoles.json()
        jueves_api = jueves.json()
        viernes_api = viernes.json()
        sabado_api = sabado.json()
        domingo_api = domingo.json()
        # REGISTRO CLASE
        if request.method == 'POST':
            # DATOS
            Apartado_agenda = request.form.get('dia_apartado')
            Apartado_act = request.form.get('sala_apartado')
            # ENVIO CITA
            url = day.url_api_app+'citas/restablecerClase'
            headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
            datos_envio = {'id': Apartado_act, 'dia':Apartado_agenda}
            r = requests.post(url, headers=headers, json=datos_envio)
            text = request.form.get("dia_apartado")
            if text == "":
                flash("El campo texto es obligatorio(*)", category='alert alert-danger')
            else:
                dato = r.json()
                resp_api = dato['Respuesta']
                flash(resp_api, category='alert alert-success')
                r.json()
                return redirect(url_for('configuracion.configuracion_restablecer_sala'))
        else:
            return render_template('config/Restablecer/clase.html', lunes_api=lunes_api, martes_api=martes_api, miercoles_api=miercoles_api, 
                                        jueves_api=jueves_api, viernes_api=viernes_api, sabado_api=sabado_api, domingo_api=domingo_api,
                                        lunes_day=lunes_day, martes_day=martes_day, miercoles_day=miercoles_day, jueves_day=jueves_day, 
                                        viernes_day=viernes_day, sabado_day=sabado_day, domingo_day=domingo_day, club=club)
    elif current_user.cimera == 1 and current_user.user_configuracion == 1:
        # CLUB
        club = 'CIMERA'
        # DIAS
        parametros_lunes = {'club':'CIMERA', 'dia':lunes_day}
        parametros_martes = {'club':'CIMERA', 'dia':martes_day}
        parametros_miercoles = {'club':'CIMERA', 'dia':miercoles_day}
        parametros_jueves = {'club':'CIMERA', 'dia':jueves_day}
        parametros_viernes = {'club':'CIMERA', 'dia':viernes_day}
        parametros_sabado = {'club':'CIMERA', 'dia':sabado_day}
        parametros_domingo = {'club':'CIMERA', 'dia':domingo_day}
        # RESPUESTA
        lunes = requests.get(url, headers=headers, params=parametros_lunes)
        martes = requests.get(url, headers=headers, params=parametros_martes)
        miercoles = requests.get(url, headers=headers, params=parametros_miercoles)
        jueves = requests.get(url, headers=headers, params=parametros_jueves)
        viernes = requests.get(url, headers=headers, params=parametros_viernes)
        sabado = requests.get(url, headers=headers, params=parametros_sabado)
        domingo = requests.get(url, headers=headers, params=parametros_domingo)
        # SERIALIZACION
        lunes_api = lunes.json()
        martes_api = martes.json()
        miercoles_api = miercoles.json()
        jueves_api = jueves.json()
        viernes_api = viernes.json()
        sabado_api = sabado.json()
        domingo_api = domingo.json()
        # REGISTRO CLASE
        if request.method == 'POST':
            # DATOS
            Apartado_agenda = request.form.get('dia_apartado')
            Apartado_act = request.form.get('sala_apartado')
            # ENVIO CITA
            url = day.url_api_app+'citas/restablecerClase'
            headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+day.resp_api_token}
            datos_envio = {'id': Apartado_act, 'dia':Apartado_agenda}
            r = requests.post(url, headers=headers, json=datos_envio)
            text = request.form.get("dia_apartado")
            if text == "":
                flash("El campo texto es obligatorio(*)", category='alert alert-danger')
            else:
                dato = r.json()
                resp_api = dato['Respuesta']
                flash(resp_api, category='alert alert-success')
                r.json()
                return redirect(url_for('configuracion.configuracion_restablecer_sala'))
        else:
            return render_template('config/Restablecer/clase.html', lunes_api=lunes_api, martes_api=martes_api, miercoles_api=miercoles_api, 
                                        jueves_api=jueves_api, viernes_api=viernes_api, sabado_api=sabado_api, domingo_api=domingo_api,
                                        lunes_day=lunes_day, martes_day=martes_day, miercoles_day=miercoles_day, jueves_day=jueves_day, 
                                        viernes_day=viernes_day, sabado_day=sabado_day, domingo_day=domingo_day, club=club)
