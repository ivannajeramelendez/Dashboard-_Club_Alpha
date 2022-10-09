from cgi import print_arguments
from flask import Flask, render_template, redirect, url_for, request, abort, flash,\
    session, Response, Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required,\
    current_user
from sqlalchemy.sql.expression import asc
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, desc
from sqlalchemy.sql.functions import concat
from sqlalchemy import DateTime, select, distinct, true, tuple_, text
from wtforms.compat import text_type
from app import api, day
from datetime import date, timedelta
import requests
import datetime
import os
    # FORMULARIOS
from forms.forms import *
app = Flask(__name__)
app.config.from_object(api)
app.config.from_object(day)

aforo = Blueprint('aforo', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

#===================================================================[MENU]===================================================================#
@aforo.route("/")
@aforo.route("/aforo/club", methods=['GET', 'POST'])
@login_required
def aforo_club():
    if request.method == 'POST' and request.form.get("restablecer") == 'restablecer':
         # TOKEN
        url_token = day.url_api_app+'auth/login'
        datos_token = {"nombreUsuario": "XXX", "password": "XXX"}
        r_token = requests.post(url_token, json=datos_token)
        resp_token = r_token.json()
        resp_api_token = resp_token['token']
        # DATOS
        ID_cliente = request.form.get("ID_Cliente")
        # ENVIO CITA
        url = day.url_api_app+'auth/reset-password/'+ID_cliente
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+resp_api_token}
        r = requests.get(url, headers=headers)
        dato = r.json()
        resp_api = dato['respuesta']
        flash(resp_api, category='alert alert-success')
        return redirect(url_for('aforo.aforo_club'))
    else:
        redirect('aforo.aforo_club')
    return render_template('aforo/Menu/club.html')

#=====================================================================================================================================================#

#===================================================================[CLUB ALPHA 2]===================================================================#
@aforo.route("/aforo/inicio/club_alpha_2", methods=['GET', 'POST'])
@login_required
def aforo_inicio_club_alpha_2():
    from models.models import db
    form = ClienteForm()
    today = date.today() # DIA ACTUAL
    fecha_title = today.strftime("%d %B, %Y, %A")
    # SPORTS PLAZA
    dias_dash_ = db.engine.execute(("SELECT nombre,fecha FROM dias_semana"))
    dias_dash = [row for row in dias_dash_]
    lunes_dash = dias_dash[0]['fecha']
    martes_dash = dias_dash[1]['fecha']
    miercoles_dash = dias_dash[2]['fecha']
    jueves_dash = dias_dash[3]['fecha']
    viernes_dash = dias_dash[4]['fecha']
    sabado_dash = dias_dash[5]['fecha']
    domingo_dash = dias_dash[6]['fecha']
    # CLUB
    club = 'Club Alpha 2'
    # DIAS TITULOS
    lunes = lunes_dash
    martes = martes_dash
    miercoles = miercoles_dash
    jueves = jueves_dash
    viernes = viernes_dash
    sabado = sabado_dash
    domingo = domingo_dash
    # LLAMADA HORARIOS CALENDARIO
    lun_ = db.engine.execute(("SELECT * FROM clases where dia between '"+lunes+"' and '"+lunes+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    lun = [row for row in lun_]
    mar_ = db.engine.execute(("SELECT * FROM clases where dia between '"+martes+"' and '"+martes+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    mar = [row for row in mar_]
    mie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+miercoles+"' and '"+miercoles+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    mie = [row for row in mie_]
    jue_ = db.engine.execute(("SELECT * FROM clases where dia between '"+jueves+"' and '"+jueves+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    jue = [row for row in jue_]
    vie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+viernes+"' and '"+viernes+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    vie = [row for row in vie_]
    sab_ = db.engine.execute(("SELECT * FROM clases where dia between '"+sabado+"' and '"+sabado+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    sab = [row for row in sab_]
    dom_ = db.engine.execute(("SELECT * FROM clases where dia between '"+domingo+"' and '"+domingo+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    dom = [row for row in dom_]
    all_ = db.engine.execute(("SELECT distinct nombre, color, tipo_actividad, segmentacion FROM clases where dia between '"+lunes+"' and '"+domingo+"' and club='"+club+"' AND segmentacion = false AND disponible = true"))
    all = [row for row in all_]
    if request.method == 'POST' and request.form.get("tipo") == 'canchas':
        # LLAMADA HORARIOS CALENDARIO
        lun_ = db.engine.execute(("SELECT * FROM clases where dia between '"+lunes+"' and '"+lunes+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        lun = [row for row in lun_]
        mar_ = db.engine.execute(("SELECT * FROM clases where dia between '"+martes+"' and '"+martes+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        mar = [row for row in mar_]
        mie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+miercoles+"' and '"+miercoles+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        mie = [row for row in mie_]
        jue_ = db.engine.execute(("SELECT * FROM clases where dia between '"+jueves+"' and '"+jueves+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        jue = [row for row in jue_]
        vie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+viernes+"' and '"+viernes+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        vie = [row for row in vie_]
        sab_ = db.engine.execute(("SELECT * FROM clases where dia between '"+sabado+"' and '"+sabado+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        sab = [row for row in sab_]
        dom_ = db.engine.execute(("SELECT * FROM clases where dia between '"+domingo+"' and '"+domingo+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        dom = [row for row in dom_]
        all_ = db.engine.execute(("SELECT distinct nombre, color, tipo_actividad, segmentacion FROM clases where dia between '"+lunes+"' and '"+domingo+"' and club='"+club+"' AND segmentacion = true AND disponible = true"))
        all = [row for row in all_]
        return render_template('aforo/Club_alpha_2/aforo_semana.html', lun=lun, mar=mar, mie=mie, jue=jue, vie=vie, sab=sab, dom=dom, fecha_title=fecha_title,
        lunes=lunes, martes=martes, miercoles=miercoles, jueves=jueves, viernes=viernes, sabado=sabado, domingo=domingo, all=all, club=club, form=form)
    if request.method == 'POST':
        # DATOS
        ID_Cliente = request.form.get('id')
        Apartado_agenda = request.form.get('dia_apartado')
        Apartado_act = request.form.get('actividad')
        # ENVIO CITA
        url = day.url_api_app+'citas/crearApartados'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente, 'club': 'Club Alpha 2', 'dia': Apartado_agenda, 'id': Apartado_act}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_club_alpha_2'))
    else:
        return render_template('aforo/Club_alpha_2/aforo_semana.html', lun=lun, mar=mar, mie=mie, jue=jue, vie=vie, sab=sab, dom=dom, fecha_title=fecha_title,
        lunes=lunes, martes=martes, miercoles=miercoles, jueves=jueves, viernes=viernes, sabado=sabado, domingo=domingo, all=all, club=club, form=form)

@aforo.route("/aforo/inicio/club_alpha_2/dia", methods=['GET', 'POST'])
@login_required
def aforo_inicio_club_alpha_2_dia_sala():
    if request.method == 'POST' and request.form.get("dia_salas") == 'dia':
        from models.models import db
        today = date.today() # DIA ACTUAL
        fecha_title = today.strftime("%d %B, %Y, %A")
        # FECHA PARA EL DIA 
        dato_dia = request.form.get('Fecha_Inicio')
        # CLUB
        club = 'Club Alpha 2'
        # DIAS TITULOS
        dia = dato_dia
        # LLAMADA HORARIOS CALENDARIO
        aforo_ = db.engine.execute(("SELECT * FROM clases where dia between '"+dato_dia+"' and '"+dato_dia+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
        aforo = [row for row in aforo_]
        return render_template('aforo/Club_alpha_2/aforo_dia.html', aforo=aforo, fecha_title=fecha_title, dia=dia, club=club)
    if request.method == 'POST' and request.form.get("dia_salas") == 'dia_canchas':
        from models.models import db
        today = date.today() # DIA ACTUAL
        fecha_title = today.strftime("%d %B, %Y, %A")
        # FECHA PARA EL DIA 
        dato_dia = request.form.get('Fecha_Inicio')
        # CLUB
        club = 'Club Alpha 2'
        # DIAS TITULOS
        dia = dato_dia
        # LLAMADA HORARIOS CALENDARIO
        aforo_ = db.engine.execute(("SELECT * FROM clases where dia between '"+dato_dia+"' and '"+dato_dia+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        aforo = [row for row in aforo_]
        return render_template('aforo/Club_alpha_2/aforo_dia.html', aforo=aforo, fecha_title=fecha_title, dia=dia, club=club)
    if request.method == 'POST' and request.form.get("apartado_dia") == 'dia_apartado':
        # REGRESO
        dias_salas_ret = 'dia'
        # DATOS
        ID_Cliente = request.form.get('id')
        Apartado_agenda = request.form.get('dia_apartado')
        Apartado_act = request.form.get('actividad')
        # ENVIO CITA
        url = day.url_api_app+'citas/crearApartados'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente, 'club': 'Club Alpha 2', 'dia': Apartado_agenda, 'id': Apartado_act}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_club_alpha_2_dia_sala', dias_salas_ret=dias_salas_ret, Apartado_agenda=Apartado_agenda))
    if request.args.get("dias_salas_ret") == 'dia':
        from models.models import db
        today = date.today() # DIA ACTUAL
        fecha_title = today.strftime("%d %B, %Y, %A")
        # FECHA PARA EL DIA 
        dato_dia = request.args.get('Apartado_agenda')
        # CLUB
        club = 'Club Alpha 2'
        # DIAS TITULOS
        dia = dato_dia
        # LLAMADA HORARIOS CALENDARIO
        aforo_ = db.engine.execute(("SELECT * FROM clases where dia between '"+dato_dia+"' and '"+dato_dia+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
        aforo = [row for row in aforo_]
        return render_template('aforo/Club_alpha_2/aforo_dia.html', aforo=aforo, fecha_title=fecha_title, dia=dia, club=club)
    else:
        return redirect(url_for('aforo.aforo_club'))

@aforo.route("/aforo/inicio/club_alpha_2/informacion_sala", methods=['GET', 'POST'])
@login_required
def aforo_inicio_club_alpha_2_informacion_sala():
    # GET
    Ver_sala = request.form.get("ver_apartado")
    Dia_sala = request.form.get("dia_apartado")
    ID_sala = request.form.get("id_apartado")
    Nombre_sala = request.form.get("nombre_apartado")
    Horario_sala = request.form.get("horario_apartado")
    # ARG
    Dia_id_apartado = request.args.get("Dia_apartado")
    Act_id_apartado = request.args.get('Actividad_apartado')
    tipo_envio = request.args.get('envio_nuevo')
    if request.method == 'POST' and request.form.get("ver_apartado") == 'vista':
        # DATA SALA
        sala = request.form.get("sala_apartado")
        # ENVIO CITA
        url = day.url_api_app+'citas/obtenerUsuariosByClase'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'id': sala}
        r = requests.get(url, headers=headers, json=datos_envio)
        resp = r.json()
        return render_template('aforo/Club_alpha_2/aforo_informes.html', resp=resp, sala=sala, Dia_sala=Dia_sala, ID_sala=ID_sala, Nombre_sala=Nombre_sala, Horario_sala=Horario_sala)
    if request.args.get("envio_nuevo") == 'validacion':
        Dia_id_apartado = request.args.get("Dia_apartado")
        Dia_sala = Dia_id_apartado
        # DATA SALA
        sala = request.args.get('ID_Sala_apartado')
        Nombre_sala = request.args.get('Nombre_sala')
        Horario_sala = request.args.get('Horario_sala')
        # ENVIO CITA
        url = day.url_api_app+'citas/obtenerUsuariosByClase'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'id': sala}
        r = requests.get(url, headers=headers, json=datos_envio)
        resp = r.json()
        return render_template('aforo/Club_alpha_2/aforo_informes.html', resp=resp, sala=sala, Dia_sala=Dia_sala, ID_sala=ID_sala, Nombre_sala=Nombre_sala, Horario_sala=Horario_sala)
    if request.method == 'POST' and request.form.get("validacion") == 'validacion':
        # DATOS
        Horario_sala_can = request.form.get('horario_apartado')
        Nombre_sala_can = request.form.get('nombre_apartado')
        Dia_apartado = request.form.get('dia_apartado')
        Actividad_apartado = request.form.get('actividad')
        envio_nuevo = 'validacion'
        # DATOS
        ID_Cliente_apartado = request.form.get("id_cliente_apartado")
        ID_Sala_apartado = request.form.get("clase_apartado")
        Sala = request.form.get("clase_apartado")
        # ENVIO CITA
        url = day.url_api_app+'citas/confirmarAsistencia'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente_apartado, 'id': ID_Sala_apartado}
        r = requests.post(url, headers=headers, json=datos_envio)
        r.json()
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_club_alpha_2_informacion_sala', Dia_apartado=Dia_apartado, Actividad_apartado=Actividad_apartado, envio_nuevo=envio_nuevo,
                                    ID_Sala_apartado=ID_Sala_apartado, Nombre_sala=Nombre_sala_can, Horario_sala=Horario_sala_can, Sala=Sala))
    if request.method == 'POST' and request.form.get("validacion") == 'cancelar':
        # DATOS
        Horario_sala_can = request.form.get('horario_apartado')
        Nombre_sala_can = request.form.get('nombre_apartado')
        Dia_apartado = request.form.get('dia_apartado')
        Actividad_apartado = request.form.get('actividad')
        envio_nuevo = 'nuevo'
        # DATOS PARA CANCELAR 
        ID_Cliente_apartado = request.form.get("id_cliente_apartado")
        ID_Sala_apartado = request.form.get("clase_apartado")
        Sala = request.form.get("clase_apartado")
        # ENVIO CITA
        url = day.url_api_app+'citas/cancelarApartados'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente_apartado, 'id': ID_Sala_apartado}
        r = requests.post(url, headers=headers, json=datos_envio)
        r.json()
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_club_alpha_2_informacion_sala', Dia_apartado=Dia_apartado, Actividad_apartado=Actividad_apartado, envio_nuevo=envio_nuevo,
                                    ID_Sala_apartado=ID_Sala_apartado, Nombre_sala=Nombre_sala_can, Horario_sala=Horario_sala_can, Sala=Sala))
    if request.args.get("envio_nuevo") == 'nuevo':
        # DATA SALA
        sala_id = request.args.get("Sala")
        sala = request.args.get("Actividad_apartado")
        Nombre_sala = request.args.get("Nombre_sala")
        Horario_sala = request.args.get("Horario_sala")
        # ENVIO CITA
        url = day.url_api_app+'citas/obtenerUsuariosByClase'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'id': sala, 'dia': Dia_id_apartado}
        r = requests.get(url, headers=headers, json=datos_envio)
        resp = r.json()
        return render_template('aforo/Club_alpha_2/aforo_informes.html', resp=resp, sala=sala_id, Dia_sala=Dia_id_apartado, ID_sala=Act_id_apartado, Nombre_sala=Nombre_sala, 
                                Horario_sala=Horario_sala)
    if request.method == 'POST' and request.form.get("envio_sala_apartado") == 'apartado':
        # DATOS
        ID_Cliente = request.form.get('id')
        Dia_apartado = request.form.get('dia_apartado')
        Actividad_apartado = request.form.get('actividad')
        envio_nuevo = 'nuevo'
        Horario_sala_can = request.form.get('horario_apartado')
        Nombre_sala_can = request.form.get('nombre_apartado')
        Sala = request.form.get("clase_apartado")
        # ENVIO CITA
        url = day.url_api_app+'citas/crearApartados'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente, 'club': 'Club Alpha 2', 'dia': Dia_apartado, 'id': Actividad_apartado}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_club_alpha_2_informacion_sala', Dia_apartado=Dia_apartado, Actividad_apartado=Actividad_apartado, envio_nuevo=envio_nuevo,
                                     Horario_sala=Horario_sala_can, Nombre_sala=Nombre_sala_can, Sala=Sala))
    else:
        return redirect(url_for('aforo.aforo_inicio_club_alpha_2'))

#=====================================================================================================================================================#

#===================================================================[CLUB ALPHA 3]===================================================================#
@aforo.route("/aforo/inicio/club_alpha_3", methods=['GET', 'POST'])
@login_required
def aforo_inicio_club_alpha_3():
    from models.models import db
    form = ClienteForm()
    today = date.today() # DIA ACTUAL
    fecha_title = today.strftime("%d %B, %Y, %A")
    # SPORTS PLAZA
    dias_dash_ = db.engine.execute(("SELECT nombre,fecha FROM dias_semana"))
    dias_dash = [row for row in dias_dash_]
    lunes_dash = dias_dash[0]['fecha']
    martes_dash = dias_dash[1]['fecha']
    miercoles_dash = dias_dash[2]['fecha']
    jueves_dash = dias_dash[3]['fecha']
    viernes_dash = dias_dash[4]['fecha']
    sabado_dash = dias_dash[5]['fecha']
    domingo_dash = dias_dash[6]['fecha']
    # CLUB
    club = 'Club Alpha 3'
    # DIAS TITULOS
    lunes = lunes_dash
    martes = martes_dash
    miercoles = miercoles_dash
    jueves = jueves_dash
    viernes = viernes_dash
    sabado = sabado_dash
    domingo = domingo_dash
    # LLAMADA HORARIOS CALENDARIO
    lun_ = db.engine.execute(("SELECT * FROM clases where dia between '"+lunes+"' and '"+lunes+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    lun = [row for row in lun_]
    mar_ = db.engine.execute(("SELECT * FROM clases where dia between '"+martes+"' and '"+martes+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    mar = [row for row in mar_]
    mie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+miercoles+"' and '"+miercoles+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    mie = [row for row in mie_]
    jue_ = db.engine.execute(("SELECT * FROM clases where dia between '"+jueves+"' and '"+jueves+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    jue = [row for row in jue_]
    vie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+viernes+"' and '"+viernes+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    vie = [row for row in vie_]
    sab_ = db.engine.execute(("SELECT * FROM clases where dia between '"+sabado+"' and '"+sabado+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    sab = [row for row in sab_]
    dom_ = db.engine.execute(("SELECT * FROM clases where dia between '"+domingo+"' and '"+domingo+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    dom = [row for row in dom_]
    all_ = db.engine.execute(("SELECT distinct nombre, color, tipo_actividad, segmentacion FROM clases where dia between '"+lunes+"' and '"+domingo+"' and club='"+club+"' AND segmentacion = false AND disponible = true"))
    all = [row for row in all_]
    if request.method == 'POST' and request.form.get("tipo") == 'canchas':
        # LLAMADA HORARIOS CALENDARIO
        lun_ = db.engine.execute(("SELECT * FROM clases where dia between '"+lunes+"' and '"+lunes+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        lun = [row for row in lun_]
        mar_ = db.engine.execute(("SELECT * FROM clases where dia between '"+martes+"' and '"+martes+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        mar = [row for row in mar_]
        mie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+miercoles+"' and '"+miercoles+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        mie = [row for row in mie_]
        jue_ = db.engine.execute(("SELECT * FROM clases where dia between '"+jueves+"' and '"+jueves+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        jue = [row for row in jue_]
        vie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+viernes+"' and '"+viernes+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        vie = [row for row in vie_]
        sab_ = db.engine.execute(("SELECT * FROM clases where dia between '"+sabado+"' and '"+sabado+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        sab = [row for row in sab_]
        dom_ = db.engine.execute(("SELECT * FROM clases where dia between '"+domingo+"' and '"+domingo+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        dom = [row for row in dom_]
        all_ = db.engine.execute(("SELECT distinct nombre, color, tipo_actividad, segmentacion FROM clases where dia between '"+lunes+"' and '"+domingo+"' and club='"+club+"' AND segmentacion = true AND disponible = true"))
        all = [row for row in all_]
        return render_template('aforo/Club_alpha_3/aforo_semana.html', lun=lun, mar=mar, mie=mie, jue=jue, vie=vie, sab=sab, dom=dom, fecha_title=fecha_title,
        lunes=lunes, martes=martes, miercoles=miercoles, jueves=jueves, viernes=viernes, sabado=sabado, domingo=domingo, all=all, club=club, form=form)
    if request.method == 'POST':
        # DATOS
        ID_Cliente = request.form.get('id')
        Apartado_agenda = request.form.get('dia_apartado')
        Apartado_act = request.form.get('actividad')
        # ENVIO CITA
        url = day.url_api_app+'citas/crearApartados'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente, 'club': 'Club Alpha 3', 'dia': Apartado_agenda, 'id': Apartado_act}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_club_alpha_3'))
    else:
        return render_template('aforo/Club_alpha_3/aforo_semana.html', lun=lun, mar=mar, mie=mie, jue=jue, vie=vie, sab=sab, dom=dom, fecha_title=fecha_title,
        lunes=lunes, martes=martes, miercoles=miercoles, jueves=jueves, viernes=viernes, sabado=sabado, domingo=domingo, all=all, club=club, form=form)

@aforo.route("/aforo/inicio/club_alpha_3/dia", methods=['GET', 'POST'])
@login_required
def aforo_inicio_club_alpha_3_dia_sala():
    if request.method == 'POST' and request.form.get("dia_salas") == 'dia':
        from models.models import db
        today = date.today() # DIA ACTUAL
        fecha_title = today.strftime("%d %B, %Y, %A")
        # FECHA PARA EL DIA 
        dato_dia = request.form.get('Fecha_Inicio')
        # CLUB
        club = 'Club Alpha 3'
        # DIAS TITULOS
        dia = dato_dia
        # LLAMADA HORARIOS CALENDARIO
        aforo_ = db.engine.execute(("SELECT * FROM clases where dia between '"+dato_dia+"' and '"+dato_dia+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
        aforo = [row for row in aforo_]
        return render_template('aforo/Club_alpha_3/aforo_dia.html', aforo=aforo, fecha_title=fecha_title, dia=dia, club=club)
    if request.method == 'POST' and request.form.get("dia_salas") == 'dia_canchas':
        from models.models import db
        today = date.today() # DIA ACTUAL
        fecha_title = today.strftime("%d %B, %Y, %A")
        # FECHA PARA EL DIA 
        dato_dia = request.form.get('Fecha_Inicio')
        # CLUB
        club = 'Club Alpha 3'
        # DIAS TITULOS
        dia = dato_dia
        # LLAMADA HORARIOS CALENDARIO
        aforo_ = db.engine.execute(("SELECT * FROM clases where dia between '"+dato_dia+"' and '"+dato_dia+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        aforo = [row for row in aforo_]
        return render_template('aforo/Club_alpha_3/aforo_dia.html', aforo=aforo, fecha_title=fecha_title, dia=dia, club=club)
    if request.method == 'POST' and request.form.get("apartado_dia") == 'dia_apartado':
        # REGRESO
        dias_salas_ret = 'dia'
        # DATOS
        ID_Cliente = request.form.get('id')
        Apartado_agenda = request.form.get('dia_apartado')
        Apartado_act = request.form.get('actividad')
        # ENVIO CITA
        url = day.url_api_app+'citas/crearApartados'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente, 'club': 'Club Alpha 3', 'dia': Apartado_agenda, 'id': Apartado_act}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_club_alpha_3_dia_sala', dias_salas_ret=dias_salas_ret, Apartado_agenda=Apartado_agenda))
    if request.args.get("dias_salas_ret") == 'dia':
        from models.models import db
        today = date.today() # DIA ACTUAL
        fecha_title = today.strftime("%d %B, %Y, %A")
        # FECHA PARA EL DIA 
        dato_dia = request.args.get('Apartado_agenda')
        # CLUB
        club = 'Club Alpha 3'
        # DIAS TITULOS
        dia = dato_dia
        # LLAMADA HORARIOS CALENDARIO
        aforo_ = db.engine.execute(("SELECT * FROM clases where dia between '"+dato_dia+"' and '"+dato_dia+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
        aforo = [row for row in aforo_]
        return render_template('aforo/Club_alpha_3/aforo_dia.html', aforo=aforo, fecha_title=fecha_title, dia=dia, club=club)
    else:
        return redirect(url_for('aforo.aforo_club'))

@aforo.route("/aforo/inicio/club_alpha_3/informacion_sala", methods=['GET', 'POST'])
@login_required
def aforo_inicio_club_alpha_3_informacion_sala():
    # GET
    Ver_sala = request.form.get("ver_apartado")
    Dia_sala = request.form.get("dia_apartado")
    ID_sala = request.form.get("id_apartado")
    Nombre_sala = request.form.get("nombre_apartado")
    Horario_sala = request.form.get("horario_apartado")
    # ARG
    Dia_id_apartado = request.args.get("Dia_apartado")
    Act_id_apartado = request.args.get('Actividad_apartado')
    tipo_envio = request.args.get('envio_nuevo')
    if request.method == 'POST' and request.form.get("ver_apartado") == 'vista':
        # DATA SALA
        sala = request.form.get("sala_apartado")
        # ENVIO CITA
        url = day.url_api_app+'citas/obtenerUsuariosByClase'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'id': sala}
        r = requests.get(url, headers=headers, json=datos_envio)
        resp = r.json()
        return render_template('aforo/Club_alpha_3/aforo_informes.html', resp=resp, sala=sala, Dia_sala=Dia_sala, ID_sala=ID_sala, Nombre_sala=Nombre_sala, Horario_sala=Horario_sala)
    if request.args.get("envio_nuevo") == 'validacion':
        Dia_id_apartado = request.args.get("Dia_apartado")
        Dia_sala = Dia_id_apartado
        # DATA SALA
        sala = request.args.get('ID_Sala_apartado')
        Nombre_sala = request.args.get('Nombre_sala')
        Horario_sala = request.args.get('Horario_sala')
        # ENVIO CITA
        url = day.url_api_app+'citas/obtenerUsuariosByClase'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'id': sala}
        r = requests.get(url, headers=headers, json=datos_envio)
        resp = r.json()
        return render_template('aforo/Club_alpha_3/aforo_informes.html', resp=resp, sala=sala, Dia_sala=Dia_sala, ID_sala=ID_sala, Nombre_sala=Nombre_sala, Horario_sala=Horario_sala)
    if request.method == 'POST' and request.form.get("validacion") == 'validacion':
        # DATOS
        Horario_sala_can = request.form.get('horario_apartado')
        Nombre_sala_can = request.form.get('nombre_apartado')
        Dia_apartado = request.form.get('dia_apartado')
        Actividad_apartado = request.form.get('actividad')
        envio_nuevo = 'validacion'
        # DATOS
        ID_Cliente_apartado = request.form.get("id_cliente_apartado")
        ID_Sala_apartado = request.form.get("clase_apartado")
        Sala = request.form.get("clase_apartado")
        # ENVIO CITA
        url = day.url_api_app+'citas/confirmarAsistencia'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente_apartado, 'id': ID_Sala_apartado}
        r = requests.post(url, headers=headers, json=datos_envio)
        r.json()
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_club_alpha_3_informacion_sala', Dia_apartado=Dia_apartado, Actividad_apartado=Actividad_apartado, envio_nuevo=envio_nuevo,
                                    ID_Sala_apartado=ID_Sala_apartado, Nombre_sala=Nombre_sala_can, Horario_sala=Horario_sala_can, Sala=Sala))
    if request.method == 'POST' and request.form.get("validacion") == 'cancelar':
        # DATOS
        Horario_sala_can = request.form.get('horario_apartado')
        Nombre_sala_can = request.form.get('nombre_apartado')
        Dia_apartado = request.form.get('dia_apartado')
        Actividad_apartado = request.form.get('actividad')
        envio_nuevo = 'nuevo'
        # DATOS PARA CANCELAR 
        ID_Cliente_apartado = request.form.get("id_cliente_apartado")
        ID_Sala_apartado = request.form.get("clase_apartado")
        Sala = request.form.get("clase_apartado")
        # ENVIO CITA
        url = day.url_api_app+'citas/cancelarApartados'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente_apartado, 'id': ID_Sala_apartado}
        r = requests.post(url, headers=headers, json=datos_envio)
        r.json()
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_club_alpha_3_informacion_sala', Dia_apartado=Dia_apartado, Actividad_apartado=Actividad_apartado, envio_nuevo=envio_nuevo,
                                    ID_Sala_apartado=ID_Sala_apartado, Nombre_sala=Nombre_sala_can, Horario_sala=Horario_sala_can, Sala=Sala))
    if request.args.get("envio_nuevo") == 'nuevo':
        # DATA SALA
        sala_id = request.args.get("Sala")
        sala = request.args.get("Actividad_apartado")
        Nombre_sala = request.args.get("Nombre_sala")
        Horario_sala = request.args.get("Horario_sala")
        # ENVIO CITA
        url = day.url_api_app+'citas/obtenerUsuariosByClase'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'id': sala, 'dia': Dia_id_apartado}
        r = requests.get(url, headers=headers, json=datos_envio)
        resp = r.json()
        return render_template('aforo/Club_alpha_3/aforo_informes.html', resp=resp, sala=sala_id, Dia_sala=Dia_id_apartado, ID_sala=Act_id_apartado, Nombre_sala=Nombre_sala, 
                                Horario_sala=Horario_sala)
    if request.method == 'POST' and request.form.get("envio_sala_apartado") == 'apartado':
        # DATOS
        ID_Cliente = request.form.get('id')
        Dia_apartado = request.form.get('dia_apartado')
        Actividad_apartado = request.form.get('actividad')
        envio_nuevo = 'nuevo'
        Horario_sala_can = request.form.get('horario_apartado')
        Nombre_sala_can = request.form.get('nombre_apartado')
        Sala = request.form.get("clase_apartado")
        # ENVIO CITA
        url = day.url_api_app+'citas/crearApartados'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente, 'club': 'Club Alpha 3', 'dia': Dia_apartado, 'id': Actividad_apartado}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_club_alpha_3_informacion_sala', Dia_apartado=Dia_apartado, Actividad_apartado=Actividad_apartado, envio_nuevo=envio_nuevo,
                                     Horario_sala=Horario_sala_can, Nombre_sala=Nombre_sala_can, Sala=Sala))
    else:
        return redirect(url_for('aforo.aforo_inicio_club_alpha_3'))

#=====================================================================================================================================================#

#===================================================================[CIMERA]===================================================================#
@aforo.route("/aforo/inicio/cimera", methods=['GET', 'POST'])
@login_required
def aforo_inicio_cimera():
    from models.models import db
    form = ClienteForm()
    today = date.today() # DIA ACTUAL
    fecha_title = today.strftime("%d %B, %Y, %A")
    # SPORTS PLAZA
    dias_dash_ = db.engine.execute(("SELECT nombre,fecha FROM dias_semana"))
    dias_dash = [row for row in dias_dash_]
    lunes_dash = dias_dash[0]['fecha']
    martes_dash = dias_dash[1]['fecha']
    miercoles_dash = dias_dash[2]['fecha']
    jueves_dash = dias_dash[3]['fecha']
    viernes_dash = dias_dash[4]['fecha']
    sabado_dash = dias_dash[5]['fecha']
    domingo_dash = dias_dash[6]['fecha']
    # CLUB
    club = 'CIMERA'
    # DIAS TITULOS
    lunes = lunes_dash
    martes = martes_dash
    miercoles = miercoles_dash
    jueves = jueves_dash
    viernes = viernes_dash
    sabado = sabado_dash
    domingo = domingo_dash
    # LLAMADA HORARIOS CALENDARIO
    lun_ = db.engine.execute(("SELECT * FROM clases where dia between '"+lunes+"' and '"+lunes+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    lun = [row for row in lun_]
    mar_ = db.engine.execute(("SELECT * FROM clases where dia between '"+martes+"' and '"+martes+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    mar = [row for row in mar_]
    mie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+miercoles+"' and '"+miercoles+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    mie = [row for row in mie_]
    jue_ = db.engine.execute(("SELECT * FROM clases where dia between '"+jueves+"' and '"+jueves+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    jue = [row for row in jue_]
    vie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+viernes+"' and '"+viernes+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    vie = [row for row in vie_]
    sab_ = db.engine.execute(("SELECT * FROM clases where dia between '"+sabado+"' and '"+sabado+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    sab = [row for row in sab_]
    dom_ = db.engine.execute(("SELECT * FROM clases where dia between '"+domingo+"' and '"+domingo+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    dom = [row for row in dom_]
    all_ = db.engine.execute(("SELECT distinct nombre, color, tipo_actividad, segmentacion FROM clases where dia between '"+lunes+"' and '"+domingo+"' and club='"+club+"' AND segmentacion = false AND disponible = true"))
    all = [row for row in all_]
    if request.method == 'POST' and request.form.get("tipo") == 'canchas':
        # LLAMADA HORARIOS CALENDARIO
        lun_ = db.engine.execute(("SELECT * FROM clases where dia between '"+lunes+"' and '"+lunes+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        lun = [row for row in lun_]
        mar_ = db.engine.execute(("SELECT * FROM clases where dia between '"+martes+"' and '"+martes+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        mar = [row for row in mar_]
        mie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+miercoles+"' and '"+miercoles+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        mie = [row for row in mie_]
        jue_ = db.engine.execute(("SELECT * FROM clases where dia between '"+jueves+"' and '"+jueves+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        jue = [row for row in jue_]
        vie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+viernes+"' and '"+viernes+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        vie = [row for row in vie_]
        sab_ = db.engine.execute(("SELECT * FROM clases where dia between '"+sabado+"' and '"+sabado+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        sab = [row for row in sab_]
        dom_ = db.engine.execute(("SELECT * FROM clases where dia between '"+domingo+"' and '"+domingo+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        dom = [row for row in dom_]
        all_ = db.engine.execute(("SELECT distinct nombre, color, tipo_actividad, segmentacion FROM clases where dia between '"+lunes+"' and '"+domingo+"' and club='"+club+"' AND segmentacion = true AND disponible = true"))
        all = [row for row in all_]
        return render_template('aforo/Cimera/aforo_semana.html', lun=lun, mar=mar, mie=mie, jue=jue, vie=vie, sab=sab, dom=dom, fecha_title=fecha_title,
        lunes=lunes, martes=martes, miercoles=miercoles, jueves=jueves, viernes=viernes, sabado=sabado, domingo=domingo, all=all, club=club, form=form)
    if request.method == 'POST':
        # DATOS
        ID_Cliente = request.form.get('id')
        Apartado_agenda = request.form.get('dia_apartado')
        Apartado_act = request.form.get('actividad')
        # ENVIO CITA
        url = day.url_api_app+'citas/crearApartados'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente, 'club': 'CIMERA', 'dia': Apartado_agenda, 'id': Apartado_act}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_cimera'))
    else:
        return render_template('aforo/Cimera/aforo_semana.html', lun=lun, mar=mar, mie=mie, jue=jue, vie=vie, sab=sab, dom=dom, fecha_title=fecha_title,
        lunes=lunes, martes=martes, miercoles=miercoles, jueves=jueves, viernes=viernes, sabado=sabado, domingo=domingo, all=all, club=club, form=form)

@aforo.route("/aforo/inicio/cimera/dia", methods=['GET', 'POST'])
@login_required
def aforo_inicio_cimera_dia_sala():
    if request.method == 'POST' and request.form.get("dia_salas") == 'dia':
        from models.models import db
        today = date.today() # DIA ACTUAL
        fecha_title = today.strftime("%d %B, %Y, %A")
        # FECHA PARA EL DIA 
        dato_dia = request.form.get('Fecha_Inicio')
        # CLUB
        club = 'CIMERA'
        # DIAS TITULOS
        dia = dato_dia
        # LLAMADA HORARIOS CALENDARIO
        aforo_ = db.engine.execute(("SELECT * FROM clases where dia between '"+dato_dia+"' and '"+dato_dia+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
        aforo = [row for row in aforo_]
        return render_template('aforo/Cimera/aforo_dia.html', aforo=aforo, fecha_title=fecha_title, dia=dia, club=club)
    if request.method == 'POST' and request.form.get("dia_salas") == 'dia_canchas':
        from models.models import db
        today = date.today() # DIA ACTUAL
        fecha_title = today.strftime("%d %B, %Y, %A")
        # FECHA PARA EL DIA 
        dato_dia = request.form.get('Fecha_Inicio')
        # CLUB
        club = 'CIMERA'
        # DIAS TITULOS
        dia = dato_dia
        # LLAMADA HORARIOS CALENDARIO
        aforo_ = db.engine.execute(("SELECT * FROM clases where dia between '"+dato_dia+"' and '"+dato_dia+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        aforo = [row for row in aforo_]
        return render_template('aforo/Cimera/aforo_dia.html', aforo=aforo, fecha_title=fecha_title, dia=dia, club=club)
    if request.method == 'POST' and request.form.get("apartado_dia") == 'dia_apartado':
        # REGRESO
        dias_salas_ret = 'dia'
        # DATOS
        ID_Cliente = request.form.get('id')
        Apartado_agenda = request.form.get('dia_apartado')
        Apartado_act = request.form.get('actividad')
        # ENVIO CITA
        url = day.url_api_app+'citas/crearApartados'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente, 'club': 'CIMERA', 'dia': Apartado_agenda, 'id': Apartado_act}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_cimera_dia_sala', dias_salas_ret=dias_salas_ret, Apartado_agenda=Apartado_agenda))
    if request.args.get("dias_salas_ret") == 'dia':
        from models.models import db
        today = date.today() # DIA ACTUAL
        fecha_title = today.strftime("%d %B, %Y, %A")
        # FECHA PARA EL DIA 
        dato_dia = request.args.get('Apartado_agenda')
        # CLUB
        club = 'CIMERA'
        # DIAS TITULOS
        dia = dato_dia
        # LLAMADA HORARIOS CALENDARIO
        aforo_ = db.engine.execute(("SELECT * FROM clases where dia between '"+dato_dia+"' and '"+dato_dia+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
        aforo = [row for row in aforo_]
        return render_template('aforo/Cimera/aforo_dia.html', aforo=aforo, fecha_title=fecha_title, dia=dia, club=club)
    else:
        return redirect(url_for('aforo.aforo_club'))

@aforo.route("/aforo/inicio/cimera/informacion_sala", methods=['GET', 'POST'])
@login_required
def aforo_inicio_cimera_informacion_sala():
    # GET
    Ver_sala = request.form.get("ver_apartado")
    Dia_sala = request.form.get("dia_apartado")
    ID_sala = request.form.get("id_apartado")
    Nombre_sala = request.form.get("nombre_apartado")
    Horario_sala = request.form.get("horario_apartado")
    # ARG
    Dia_id_apartado = request.args.get("Dia_apartado")
    Act_id_apartado = request.args.get('Actividad_apartado')
    tipo_envio = request.args.get('envio_nuevo')
    if request.method == 'POST' and request.form.get("ver_apartado") == 'vista':
        # DATA SALA
        sala = request.form.get("sala_apartado")
        # ENVIO CITA
        url = day.url_api_app+'citas/obtenerUsuariosByClase'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'id': sala}
        r = requests.get(url, headers=headers, json=datos_envio)
        resp = r.json()
        return render_template('aforo/Cimera/aforo_informes.html', resp=resp, sala=sala, Dia_sala=Dia_sala, ID_sala=ID_sala, Nombre_sala=Nombre_sala, Horario_sala=Horario_sala)
    if request.args.get("envio_nuevo") == 'validacion':
        Dia_id_apartado = request.args.get("Dia_apartado")
        Dia_sala = Dia_id_apartado
        # DATA SALA
        sala = request.args.get('ID_Sala_apartado')
        Nombre_sala = request.args.get('Nombre_sala')
        Horario_sala = request.args.get('Horario_sala')
        # ENVIO CITA
        url = day.url_api_app+'citas/obtenerUsuariosByClase'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'id': sala}
        r = requests.get(url, headers=headers, json=datos_envio)
        resp = r.json()
        return render_template('aforo/Cimera/aforo_informes.html', resp=resp, sala=sala, Dia_sala=Dia_sala, ID_sala=ID_sala, Nombre_sala=Nombre_sala, Horario_sala=Horario_sala)
    if request.method == 'POST' and request.form.get("validacion") == 'validacion':
        # DATOS
        Horario_sala_can = request.form.get('horario_apartado')
        Nombre_sala_can = request.form.get('nombre_apartado')
        Dia_apartado = request.form.get('dia_apartado')
        Actividad_apartado = request.form.get('actividad')
        envio_nuevo = 'validacion'
        # DATOS
        ID_Cliente_apartado = request.form.get("id_cliente_apartado")
        ID_Sala_apartado = request.form.get("clase_apartado")
        Sala = request.form.get("clase_apartado")
        # ENVIO CITA
        url = day.url_api_app+'citas/confirmarAsistencia'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente_apartado, 'id': ID_Sala_apartado}
        r = requests.post(url, headers=headers, json=datos_envio)
        r.json()
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_cimera_informacion_sala', Dia_apartado=Dia_apartado, Actividad_apartado=Actividad_apartado, envio_nuevo=envio_nuevo,
                                    ID_Sala_apartado=ID_Sala_apartado, Nombre_sala=Nombre_sala_can, Horario_sala=Horario_sala_can, Sala=Sala))
    if request.method == 'POST' and request.form.get("validacion") == 'cancelar':
        # DATOS
        Horario_sala_can = request.form.get('horario_apartado')
        Nombre_sala_can = request.form.get('nombre_apartado')
        Dia_apartado = request.form.get('dia_apartado')
        Actividad_apartado = request.form.get('actividad')
        envio_nuevo = 'nuevo'
        # DATOS PARA CANCELAR 
        ID_Cliente_apartado = request.form.get("id_cliente_apartado")
        ID_Sala_apartado = request.form.get("clase_apartado")
        Sala = request.form.get("clase_apartado")
        # ENVIO CITA
        url = day.url_api_app+'citas/cancelarApartados'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente_apartado, 'id': ID_Sala_apartado}
        r = requests.post(url, headers=headers, json=datos_envio)
        r.json()
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_cimera_informacion_sala', Dia_apartado=Dia_apartado, Actividad_apartado=Actividad_apartado, envio_nuevo=envio_nuevo,
                                    ID_Sala_apartado=ID_Sala_apartado, Nombre_sala=Nombre_sala_can, Horario_sala=Horario_sala_can, Sala=Sala))
    if request.args.get("envio_nuevo") == 'nuevo':
        # DATA SALA
        sala_id = request.args.get("Sala")
        sala = request.args.get("Actividad_apartado")
        Nombre_sala = request.args.get("Nombre_sala")
        Horario_sala = request.args.get("Horario_sala")
        # ENVIO CITA
        url = day.url_api_app+'citas/obtenerUsuariosByClase'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'id': sala, 'dia': Dia_id_apartado}
        r = requests.get(url, headers=headers, json=datos_envio)
        resp = r.json()
        return render_template('aforo/Cimera/aforo_informes.html', resp=resp, sala=sala_id, Dia_sala=Dia_id_apartado, ID_sala=Act_id_apartado, Nombre_sala=Nombre_sala, 
                                Horario_sala=Horario_sala)
    if request.method == 'POST' and request.form.get("envio_sala_apartado") == 'apartado':
        # DATOS
        ID_Cliente = request.form.get('id')
        Dia_apartado = request.form.get('dia_apartado')
        Actividad_apartado = request.form.get('actividad')
        envio_nuevo = 'nuevo'
        Horario_sala_can = request.form.get('horario_apartado')
        Nombre_sala_can = request.form.get('nombre_apartado')
        Sala = request.form.get("clase_apartado")
        # ENVIO CITA
        url = day.url_api_app+'citas/crearApartados'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente, 'club': 'CIMERA', 'dia': Dia_apartado, 'id': Actividad_apartado}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_cimera_informacion_sala', Dia_apartado=Dia_apartado, Actividad_apartado=Actividad_apartado, envio_nuevo=envio_nuevo,
                                     Horario_sala=Horario_sala_can, Nombre_sala=Nombre_sala_can, Sala=Sala))
    else:
        return redirect(url_for('aforo.aforo_inicio_cimera'))

#=====================================================================================================================================================#

#===================================================================[SPORTS PLAZA]===================================================================#
@aforo.route("/aforo/inicio/sport_plaza", methods=['GET', 'POST'])
@login_required
def aforo_inicio_sport_plaza():
    from models.models import db
    form = ClienteForm()
    today = date.today() # DIA ACTUAL
    fecha_title = today.strftime("%d %B, %Y, %A")
    # SPORTS PLAZA
    dias_dash_ = db.engine.execute(("SELECT nombre,fecha FROM dias_semana"))
    dias_dash = [row for row in dias_dash_]
    lunes_dash = dias_dash[0]['fecha']
    martes_dash = dias_dash[1]['fecha']
    miercoles_dash = dias_dash[2]['fecha']
    jueves_dash = dias_dash[3]['fecha']
    viernes_dash = dias_dash[4]['fecha']
    sabado_dash = dias_dash[5]['fecha']
    domingo_dash = dias_dash[6]['fecha']
    # CLUB
    club = 'Sports Plaza'
    # DIAS TITULOS
    lunes = lunes_dash
    martes = martes_dash
    miercoles = miercoles_dash
    jueves = jueves_dash
    viernes = viernes_dash
    sabado = sabado_dash
    domingo = domingo_dash
    # LLAMADA HORARIOS CALENDARIO
    lun_ = db.engine.execute(("SELECT * FROM clases where dia between '"+lunes+"' and '"+lunes+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    lun = [row for row in lun_]
    mar_ = db.engine.execute(("SELECT * FROM clases where dia between '"+martes+"' and '"+martes+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    mar = [row for row in mar_]
    mie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+miercoles+"' and '"+miercoles+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    mie = [row for row in mie_]
    jue_ = db.engine.execute(("SELECT * FROM clases where dia between '"+jueves+"' and '"+jueves+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    jue = [row for row in jue_]
    vie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+viernes+"' and '"+viernes+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    vie = [row for row in vie_]
    sab_ = db.engine.execute(("SELECT * FROM clases where dia between '"+sabado+"' and '"+sabado+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    sab = [row for row in sab_]
    dom_ = db.engine.execute(("SELECT * FROM clases where dia between '"+domingo+"' and '"+domingo+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
    dom = [row for row in dom_]
    all_ = db.engine.execute(("SELECT distinct nombre, color, tipo_actividad, segmentacion FROM clases where dia between '"+lunes+"' and '"+domingo+"' and club='"+club+"' AND segmentacion = false AND disponible = true"))
    all = [row for row in all_]
    if request.method == 'POST' and request.form.get("tipo") == 'canchas':
        # LLAMADA HORARIOS CALENDARIO
        lun_ = db.engine.execute(("SELECT * FROM clases where dia between '"+lunes+"' and '"+lunes+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        lun = [row for row in lun_]
        mar_ = db.engine.execute(("SELECT * FROM clases where dia between '"+martes+"' and '"+martes+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        mar = [row for row in mar_]
        mie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+miercoles+"' and '"+miercoles+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        mie = [row for row in mie_]
        jue_ = db.engine.execute(("SELECT * FROM clases where dia between '"+jueves+"' and '"+jueves+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        jue = [row for row in jue_]
        vie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+viernes+"' and '"+viernes+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        vie = [row for row in vie_]
        sab_ = db.engine.execute(("SELECT * FROM clases where dia between '"+sabado+"' and '"+sabado+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        sab = [row for row in sab_]
        dom_ = db.engine.execute(("SELECT * FROM clases where dia between '"+domingo+"' and '"+domingo+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        dom = [row for row in dom_]
        all_ = db.engine.execute(("SELECT distinct nombre, color, tipo_actividad, segmentacion FROM clases where dia between '"+lunes+"' and '"+domingo+"' and club='"+club+"' AND segmentacion = true AND disponible = true"))
        all = [row for row in all_]
        return render_template('aforo/Sport_plaza/aforo_semana.html', lun=lun, mar=mar, mie=mie, jue=jue, vie=vie, sab=sab, dom=dom, fecha_title=fecha_title,
        lunes=lunes, martes=martes, miercoles=miercoles, jueves=jueves, viernes=viernes, sabado=sabado, domingo=domingo, all=all, club=club, form=form)
    if request.method == 'POST':
        # DATOS
        ID_Cliente = request.form.get('id')
        Apartado_agenda = request.form.get('dia_apartado')
        Apartado_act = request.form.get('actividad')
        # ENVIO CITA
        url = day.url_api_app+'citas/crearApartados'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente, 'club': 'Sports Plaza', 'dia': Apartado_agenda, 'id': Apartado_act}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_sport_plaza'))
    else:
        return render_template('aforo/Sport_plaza/aforo_semana.html', lun=lun, mar=mar, mie=mie, jue=jue, vie=vie, sab=sab, dom=dom, fecha_title=fecha_title,
        lunes=lunes, martes=martes, miercoles=miercoles, jueves=jueves, viernes=viernes, sabado=sabado, domingo=domingo, all=all, club=club, form=form)

@aforo.route("/aforo/inicio/sport_plaza/dia", methods=['GET', 'POST'])
@login_required
def aforo_inicio_sport_plaza_dia_sala():
    if request.method == 'POST' and request.form.get("dia_salas") == 'dia':
        from models.models import db
        today = date.today() # DIA ACTUAL
        fecha_title = today.strftime("%d %B, %Y, %A")
        # FECHA PARA EL DIA 
        dato_dia = request.form.get('Fecha_Inicio')
        # CLUB
        club = 'Sports Plaza'
        # DIAS TITULOS
        dia = dato_dia
        # LLAMADA HORARIOS CALENDARIO
        aforo_ = db.engine.execute(("SELECT * FROM clases where dia between '"+dato_dia+"' and '"+dato_dia+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
        aforo = [row for row in aforo_]
        return render_template('aforo/Sport_plaza/aforo_dia.html', aforo=aforo, fecha_title=fecha_title, dia=dia, club=club)
    if request.method == 'POST' and request.form.get("dia_salas") == 'dia_canchas':
        from models.models import db
        today = date.today() # DIA ACTUAL
        fecha_title = today.strftime("%d %B, %Y, %A")
        # FECHA PARA EL DIA 
        dato_dia = request.form.get('Fecha_Inicio')
        # CLUB
        club = 'Sports Plaza'
        # DIAS TITULOS
        dia = dato_dia
        # LLAMADA HORARIOS CALENDARIO
        aforo_ = db.engine.execute(("SELECT * FROM clases where dia between '"+dato_dia+"' and '"+dato_dia+"' and club='"+club+"' AND segmentacion = true AND disponible = true ORDER BY hora"))
        aforo = [row for row in aforo_]
        return render_template('aforo/Sport_plaza/aforo_dia.html', aforo=aforo, fecha_title=fecha_title, dia=dia, club=club)
    if request.method == 'POST' and request.form.get("apartado_dia") == 'dia_apartado':
        # REGRESO
        dias_salas_ret = 'dia'
        # DATOS
        ID_Cliente = request.form.get('id')
        Apartado_agenda = request.form.get('dia_apartado')
        Apartado_act = request.form.get('actividad')
        # ENVIO CITA
        url = day.url_api_app+'citas/crearApartados'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente, 'club': 'Sports Plaza', 'dia': Apartado_agenda, 'id': Apartado_act}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_sport_plaza_dia_sala', dias_salas_ret=dias_salas_ret, Apartado_agenda=Apartado_agenda))
    if request.args.get("dias_salas_ret") == 'dia':
        from models.models import db
        today = date.today() # DIA ACTUAL
        fecha_title = today.strftime("%d %B, %Y, %A")
        # FECHA PARA EL DIA 
        dato_dia = request.args.get('Apartado_agenda')
        # CLUB
        club = 'Sports Plaza'
        # DIAS TITULOS
        dia = dato_dia
        # LLAMADA HORARIOS CALENDARIO
        aforo_ = db.engine.execute(("SELECT * FROM clases where dia between '"+dato_dia+"' and '"+dato_dia+"' and club='"+club+"' AND segmentacion = false AND disponible = true ORDER BY hora"))
        aforo = [row for row in aforo_]
        return render_template('aforo/Sport_plaza/aforo_dia.html', aforo=aforo, fecha_title=fecha_title, dia=dia, club=club)
    else:
        return redirect(url_for('aforo.aforo_club'))

@aforo.route("/aforo/inicio/sport_plaza/informacion_sala", methods=['GET', 'POST'])
@login_required
def aforo_inicio_sport_plaza_informacion_sala():
    # GET
    Ver_sala = request.form.get("ver_apartado")
    Dia_sala = request.form.get("dia_apartado")
    ID_sala = request.form.get("id_apartado")
    Nombre_sala = request.form.get("nombre_apartado")
    Horario_sala = request.form.get("horario_apartado")
    # ARG
    Dia_id_apartado = request.args.get("Dia_apartado")
    Act_id_apartado = request.args.get('Actividad_apartado')
    tipo_envio = request.args.get('envio_nuevo')
    if request.method == 'POST' and request.form.get("ver_apartado") == 'vista':
        # DATA SALA
        sala = request.form.get("sala_apartado")
        # ENVIO CITA
        url = day.url_api_app+'citas/obtenerUsuariosByClase'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'id': sala}
        r = requests.get(url, headers=headers, json=datos_envio)
        resp = r.json()
        return render_template('aforo/Sport_plaza/aforo_informes.html', resp=resp, sala=sala, Dia_sala=Dia_sala, ID_sala=ID_sala, Nombre_sala=Nombre_sala, Horario_sala=Horario_sala)
    if request.args.get("envio_nuevo") == 'validacion':
        Dia_id_apartado = request.args.get("Dia_apartado")
        Dia_sala = Dia_id_apartado
        # DATA SALA
        sala = request.args.get('ID_Sala_apartado')
        Nombre_sala = request.args.get('Nombre_sala')
        Horario_sala = request.args.get('Horario_sala')
        # ENVIO CITA
        url = day.url_api_app+'citas/obtenerUsuariosByClase'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'id': sala}
        r = requests.get(url, headers=headers, json=datos_envio)
        resp = r.json()
        return render_template('aforo/Sport_plaza/aforo_informes.html', resp=resp, sala=sala, Dia_sala=Dia_sala, ID_sala=ID_sala, Nombre_sala=Nombre_sala, Horario_sala=Horario_sala)
    if request.method == 'POST' and request.form.get("validacion") == 'validacion':
        # DATOS
        Horario_sala_can = request.form.get('horario_apartado')
        Nombre_sala_can = request.form.get('nombre_apartado')
        Dia_apartado = request.form.get('dia_apartado')
        Actividad_apartado = request.form.get('actividad')
        envio_nuevo = 'validacion'
        # DATOS
        ID_Cliente_apartado = request.form.get("id_cliente_apartado")
        ID_Sala_apartado = request.form.get("clase_apartado")
        Sala = request.form.get("clase_apartado")
        # ENVIO CITA
        url = day.url_api_app+'citas/confirmarAsistencia'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente_apartado, 'id': ID_Sala_apartado}
        r = requests.post(url, headers=headers, json=datos_envio)
        r.json()
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_sport_plaza_informacion_sala', Dia_apartado=Dia_apartado, Actividad_apartado=Actividad_apartado, envio_nuevo=envio_nuevo,
                                    ID_Sala_apartado=ID_Sala_apartado, Nombre_sala=Nombre_sala_can, Horario_sala=Horario_sala_can, Sala=Sala))
    if request.method == 'POST' and request.form.get("validacion") == 'cancelar':
        # DATOS
        Horario_sala_can = request.form.get('horario_apartado')
        Nombre_sala_can = request.form.get('nombre_apartado')
        Dia_apartado = request.form.get('dia_apartado')
        Actividad_apartado = request.form.get('actividad')
        envio_nuevo = 'nuevo'
        # DATOS PARA CANCELAR 
        ID_Cliente_apartado = request.form.get("id_cliente_apartado")
        ID_Sala_apartado = request.form.get("clase_apartado")
        Sala = request.form.get("clase_apartado")
        # ENVIO CITA
        url = day.url_api_app+'citas/cancelarApartados'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente_apartado, 'id': ID_Sala_apartado}
        r = requests.post(url, headers=headers, json=datos_envio)
        r.json()
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_sport_plaza_informacion_sala', Dia_apartado=Dia_apartado, Actividad_apartado=Actividad_apartado, envio_nuevo=envio_nuevo,
                                    ID_Sala_apartado=ID_Sala_apartado, Nombre_sala=Nombre_sala_can, Horario_sala=Horario_sala_can, Sala=Sala))
    if request.args.get("envio_nuevo") == 'nuevo':
        # DATA SALA
        sala_id = request.args.get("Sala")
        sala = request.args.get("Actividad_apartado")
        Nombre_sala = request.args.get("Nombre_sala")
        Horario_sala = request.args.get("Horario_sala")
        # ENVIO CITA
        url = day.url_api_app+'citas/obtenerUsuariosByClase'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'id': sala, 'dia': Dia_id_apartado}
        r = requests.get(url, headers=headers, json=datos_envio)
        resp = r.json()
        return render_template('aforo/Sport_plaza/aforo_informes.html', resp=resp, sala=sala_id, Dia_sala=Dia_id_apartado, ID_sala=Act_id_apartado, Nombre_sala=Nombre_sala, 
                                Horario_sala=Horario_sala)
    if request.method == 'POST' and request.form.get("envio_sala_apartado") == 'apartado':
        # DATOS
        ID_Cliente = request.form.get('id')
        Dia_apartado = request.form.get('dia_apartado')
        Actividad_apartado = request.form.get('actividad')
        envio_nuevo = 'nuevo'
        Horario_sala_can = request.form.get('horario_apartado')
        Nombre_sala_can = request.form.get('nombre_apartado')
        Sala = request.form.get("clase_apartado")
        # ENVIO CITA
        url = day.url_api_app+'citas/crearApartados'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': ID_Cliente, 'club': 'Sports Plaza', 'dia': Dia_apartado, 'id': Actividad_apartado}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("ID_client")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['Respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('aforo.aforo_inicio_sport_plaza_informacion_sala', Dia_apartado=Dia_apartado, Actividad_apartado=Actividad_apartado, envio_nuevo=envio_nuevo,
                                     Horario_sala=Horario_sala_can, Nombre_sala=Nombre_sala_can, Sala=Sala))
    else:
        return redirect(url_for('aforo.aforo_inicio_sport_plaza'))

#=====================================================================================================================================================#

#===================================================================[ SEGMENTACION ]===================================================================#
@aforo.route("/aforo/inicio/segmentacion", methods=['GET', 'POST'])
@login_required
def aforo_inicio_club_alpha_2_segmentacion():
    from models.models import db
    # DATOS INPUT
    Club = str(request.form.get("club_segmento"))
    Segmento = str(request.form.get("segmento_dato"))
    Segmento_tipo = str(request.form.get("tipo_dato"))
    # TITULOS
    today = date.today() # DIA ACTUAL
    fecha_title = today.strftime("%d %B, %Y, %A")
    # SPORTS PLAZA
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
    lunes = lunes_dash
    martes = martes_dash
    miercoles = miercoles_dash
    jueves = jueves_dash
    viernes = viernes_dash
    sabado = sabado_dash
    domingo = domingo_dash
    # HORARIOS CALENDARIO
    lun_ = db.engine.execute(("SELECT * FROM clases where dia between '"+lunes+"' and '"+lunes+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    lun = [row for row in lun_]
    mar_ = db.engine.execute(("SELECT * FROM clases where dia between '"+martes+"' and '"+martes+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    mar = [row for row in mar_]
    mie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+miercoles+"' and '"+miercoles+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    mie = [row for row in mie_]
    jue_ = db.engine.execute(("SELECT * FROM clases where dia between '"+jueves+"' and '"+jueves+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    jue = [row for row in jue_]
    vie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+viernes+"' and '"+viernes+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    vie = [row for row in vie_]
    sab_ = db.engine.execute(("SELECT * FROM clases where dia between '"+sabado+"' and '"+sabado+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    sab = [row for row in sab_]
    dom_ = db.engine.execute(("SELECT * FROM clases where dia between '"+domingo+"' and '"+domingo+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    dom = [row for row in dom_]
    all_ = db.engine.execute(("SELECT distinct nombre, color, tipo_actividad, segmentacion FROM clases where dia between '"+lunes+"' and '"+domingo+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true"))
    all = [row for row in all_]
    return render_template('aforo/Segmento/a2_aforo.html', lunes=lunes, martes=martes, miercoles=miercoles, jueves=jueves, viernes=viernes, sabado=sabado, domingo=domingo,\
                        fecha_title=fecha_title, Segmento=Segmento, lun=lun, mar=mar, mie=mie, jue=jue, vie=vie, sab=sab, dom=dom, all=all, Club=Club)

@aforo.route("/aforo/inicio/segmentacion", methods=['GET', 'POST'])
@login_required
def aforo_inicio_club_alpha_3_segmentacion():
    from models.models import db
    # DATOS INPUT
    Club = str(request.form.get("club_segmento"))
    Segmento = str(request.form.get("segmento_dato"))
    Segmento_tipo = str(request.form.get("tipo_dato"))
    # TITULOS
    today = date.today() # DIA ACTUAL
    fecha_title = today.strftime("%d %B, %Y, %A")
    # SPORTS PLAZA
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
    lunes = lunes_dash
    martes = martes_dash
    miercoles = miercoles_dash
    jueves = jueves_dash
    viernes = viernes_dash
    sabado = sabado_dash
    domingo = domingo_dash
    # HORARIOS CALENDARIO
    lun_ = db.engine.execute(("SELECT * FROM clases where dia between '"+lunes+"' and '"+lunes+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    lun = [row for row in lun_]
    mar_ = db.engine.execute(("SELECT * FROM clases where dia between '"+martes+"' and '"+martes+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    mar = [row for row in mar_]
    mie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+miercoles+"' and '"+miercoles+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    mie = [row for row in mie_]
    jue_ = db.engine.execute(("SELECT * FROM clases where dia between '"+jueves+"' and '"+jueves+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    jue = [row for row in jue_]
    vie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+viernes+"' and '"+viernes+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    vie = [row for row in vie_]
    sab_ = db.engine.execute(("SELECT * FROM clases where dia between '"+sabado+"' and '"+sabado+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    sab = [row for row in sab_]
    dom_ = db.engine.execute(("SELECT * FROM clases where dia between '"+domingo+"' and '"+domingo+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    dom = [row for row in dom_]
    all_ = db.engine.execute(("SELECT distinct nombre, color, tipo_actividad, segmentacion FROM clases where dia between '"+lunes+"' and '"+domingo+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true"))
    all = [row for row in all_]
    return render_template('aforo/Segmento/a3_aforo.html', lunes=lunes, martes=martes, miercoles=miercoles, jueves=jueves, viernes=viernes, sabado=sabado, domingo=domingo,\
                        fecha_title=fecha_title, Segmento=Segmento, lun=lun, mar=mar, mie=mie, jue=jue, vie=vie, sab=sab, dom=dom, all=all, Club=Club)

@aforo.route("/aforo/inicio/segmentacion", methods=['GET', 'POST'])
@login_required
def aforo_inicio_cimera_segmentacion():
    from models.models import Clases, Dia_Apartados,db
    # DATOS INPUT
    Club = str(request.form.get("club_segmento"))
    Segmento = str(request.form.get("segmento_dato"))
    Segmento_tipo = str(request.form.get("tipo_dato"))
    # TITULOS
    today = date.today() # DIA ACTUAL
    fecha_title = today.strftime("%d %B, %Y, %A")
    # SPORTS PLAZA
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
    lunes = lunes_dash
    martes = martes_dash
    miercoles = miercoles_dash
    jueves = jueves_dash
    viernes = viernes_dash
    sabado = sabado_dash
    domingo = domingo_dash
    # HORARIOS CALENDARIO
    lun_ = db.engine.execute(("SELECT * FROM clases where dia between '"+lunes+"' and '"+lunes+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    lun = [row for row in lun_]
    mar_ = db.engine.execute(("SELECT * FROM clases where dia between '"+martes+"' and '"+martes+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    mar = [row for row in mar_]
    mie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+miercoles+"' and '"+miercoles+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    mie = [row for row in mie_]
    jue_ = db.engine.execute(("SELECT * FROM clases where dia between '"+jueves+"' and '"+jueves+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    jue = [row for row in jue_]
    vie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+viernes+"' and '"+viernes+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    vie = [row for row in vie_]
    sab_ = db.engine.execute(("SELECT * FROM clases where dia between '"+sabado+"' and '"+sabado+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    sab = [row for row in sab_]
    dom_ = db.engine.execute(("SELECT * FROM clases where dia between '"+domingo+"' and '"+domingo+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    dom = [row for row in dom_]
    all_ = db.engine.execute(("SELECT distinct nombre, color, tipo_actividad, segmentacion FROM clases where dia between '"+lunes+"' and '"+domingo+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true"))
    all = [row for row in all_]
    return render_template('aforo/Segmento/cim_aforo.html', lunes=lunes, martes=martes, miercoles=miercoles, jueves=jueves, viernes=viernes, sabado=sabado, domingo=domingo,\
                        fecha_title=fecha_title, Segmento=Segmento, lun=lun, mar=mar, mie=mie, jue=jue, vie=vie, sab=sab, dom=dom, all=all, Club=Club)

@aforo.route("/aforo/inicio/segmentacion", methods=['GET', 'POST'])
@login_required
def aforo_inicio_sport_plaza_segmentacion():
    from models.models import Clases, Dia_Apartados,db
    # DATOS INPUT
    Club = str(request.form.get("club_segmento"))
    Segmento = str(request.form.get("segmento_dato"))
    Segmento_tipo = str(request.form.get("tipo_dato"))
    # TITULOS
    today = date.today() # DIA ACTUAL
    fecha_title = today.strftime("%d %B, %Y, %A")
    # SPORTS PLAZA
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
    lunes = lunes_dash
    martes = martes_dash
    miercoles = miercoles_dash
    jueves = jueves_dash
    viernes = viernes_dash
    sabado = sabado_dash
    domingo = domingo_dash
    # HORARIOS CALENDARIO
    lun_ = db.engine.execute(("SELECT * FROM clases where dia between '"+lunes+"' and '"+lunes+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    lun = [row for row in lun_]
    mar_ = db.engine.execute(("SELECT * FROM clases where dia between '"+martes+"' and '"+martes+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    mar = [row for row in mar_]
    mie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+miercoles+"' and '"+miercoles+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    mie = [row for row in mie_]
    jue_ = db.engine.execute(("SELECT * FROM clases where dia between '"+jueves+"' and '"+jueves+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    jue = [row for row in jue_]
    vie_ = db.engine.execute(("SELECT * FROM clases where dia between '"+viernes+"' and '"+viernes+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    vie = [row for row in vie_]
    sab_ = db.engine.execute(("SELECT * FROM clases where dia between '"+sabado+"' and '"+sabado+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    sab = [row for row in sab_]
    dom_ = db.engine.execute(("SELECT * FROM clases where dia between '"+domingo+"' and '"+domingo+"' AND nombre='"+Segmento+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true ORDER BY hora"))
    dom = [row for row in dom_]
    all_ = db.engine.execute(("SELECT distinct nombre, color, tipo_actividad, segmentacion FROM clases where dia between '"+lunes+"' and '"+domingo+"' and club='"+Club+"' AND segmentacion = "+Segmento_tipo+" AND disponible = true"))
    all = [row for row in all_]
    return render_template('aforo/Segmento/sp_aforo.html', lunes=lunes, martes=martes, miercoles=miercoles, jueves=jueves, viernes=viernes, sabado=sabado, domingo=domingo,\
                        fecha_title=fecha_title, Segmento=Segmento, lun=lun, mar=mar, mie=mie, jue=jue, vie=vie, sab=sab, dom=dom, all=all, Club=Club)

#===================================================================[ RESERVAS X USUARIO ]===================================================================#
@aforo.route("/aforo/inicio/citas_por_usuario", methods=['GET', 'POST'])
@login_required
def aforo_inicio_citas_por_usuario():
    if request.method == 'POST':
        id_cliente = request.form.get("id")
        id_client = str(id_cliente)
        url = 'http://XXX'+id_client
        headers = {'Content-type': 'application/json','Accept': 'application/json'}
        datos_envio = {"Token":"XXX"}
        r = requests.get(url, headers=headers, json=datos_envio)
        dato = r.json()
        # REGISTRO DE AFOTOS
        url = day.url_api_app+'citas/obtenerApartadosUserSemana?usuario='+id_client
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r = requests.get(url, headers=headers)
        dato_api = r.json()
        return render_template('Citas_por_Usuario/citas_por_usuario.html', dato=dato, dato_api=dato_api)
