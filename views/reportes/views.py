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
    # FORMULARIOS
from forms.forms import *
app = Flask(__name__)
app.config.from_object(api)
app.config.from_object(day)

reportes = Blueprint('reportes', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

#===================================================================[MENU]===================================================================#
@reportes.route("/reportes/club")
@login_required
def reportes_club():
    return render_template('reportes/Menu/club.html')

@reportes.route("/reportes/especiales/menu")
@login_required
def reportes_especiales_menu():
    return render_template('reportes_especiales/Menu/club.html')

#===================================================================[REPORTES GENERALES]===================================================================#
@reportes.route("/reportes/inicio/sport_plaza/asistencia", methods=['GET', 'POST'])
@login_required
def reportes_inicio_reportes():
    from models.models import db
    # CONFIGURACION
    today = date.today() # DIA ACTUAL
    fecha_title = today.strftime("%d %B, %Y, %A")
    # DATA RECIBO
    Inicio = request.form.get("fecha_inicio") #YY-MM-DD
    Fin = request.form.get("fecha_fin")
    # QUERY SALAS Y CANCHAS
    sala_ = db.engine.execute(text("SELECT nombre, SUM(cupo_actual) as Actual FROM clases WHERE dia BETWEEN '"+Inicio+"' AND '"+Fin+"' AND club='Sports Plaza'\
                                     AND segmentacion = false GROUP BY nombre"))
    sala = [row for row in sala_]
    cancha_ = db.engine.execute(text("SELECT nombre, SUM(cupo_actual) as Actual FROM clases WHERE dia BETWEEN '"+Inicio+"' AND '"+Fin+"' AND club='Sports Plaza'\
                                     AND segmentacion = true GROUP BY nombre"))
    cancha = [row for row in cancha_]
    # APARTADOS EN GYM 
    apartados_gym_ = db.engine.execute(text("SELECT count(id) FROM registro_gimnasio WHERE registro_acceso between '"+Inicio+"' and '"+Fin+"' and id_terminal in(1,2,5,6)"))
    apartados_gym = [row for row in apartados_gym_]
    # CITAS AGENDADAS
    cupo_actual_ = db.engine.execute(text("SELECT sum(cupo_actual) FROM clases WHERE dia BETWEEN '"+Inicio+"' AND '"+Fin+"' AND club='Sports Plaza'"))
    cupo_actual = [row for row in cupo_actual_]
    # MAS POPULAR
    usuarios_fitness_ = db.engine.execute(text("SELECT nombre  FROM clases WHERE dia BETWEEN '"+Inicio+"' AND '"+Fin+"' AND club='Sports Plaza' ORDER BY cupo_actual\
                                         DESC FETCH FIRST 1 ROW ONLY"))
    usuarios_fitness = [row for row in usuarios_fitness_]
    # USUARIOS NUEVOS
    usuarios_totales_ = db.engine.execute(text("SELECT count(idcliente) FROM cliente join tipocliente on tipocliente.idtipocliente=cliente.tipocliente WHERE inicioactividades\
                                         BETWEEN '"+Inicio+"' AND '"+Fin+"' AND idclub=4 and tipocliente.nombre='MIEMBRO SP'"))
    usuarios_totales = [row for row in usuarios_totales_]
    return render_template('reportes/Sport_plaza/dashboard.html', fecha_title=fecha_title, sala=sala, cancha=cancha, lunes=Inicio, domingo=Fin,\
                            apartados_gym=apartados_gym, usuarios_fitness=usuarios_fitness, usuarios_totales=usuarios_totales, cupo_actual=cupo_actual)

@reportes.route("/reportes/inicio/asistencia", methods=['GET', 'POST'])
@login_required
def reportes_inicio_reportes_asistencia():
    from models.models import db
    # CONFIGURACION
    today = date.today() # DIA ACTUAL
    fecha_title = today.strftime("%d %B, %Y, %A")
    # DATA RECIBO
    Inicio = request.form.get("fecha_inicio") #YY-MM-DD
    Fin = request.form.get("fecha_fin")
    Club = request.form.get("Club")
    # QUERY SALAS Y CANCHAS
    sala_ = db.engine.execute(text("SELECT nombre, SUM(cupo_actual) as Actual FROM clases WHERE dia BETWEEN '"+Inicio+"' AND '"+Fin+"' AND club='"+Club+"'\
                                     AND segmentacion = false GROUP BY nombre"))
    sala = [row for row in sala_]
    cancha_ = db.engine.execute(text("SELECT nombre, SUM(cupo_actual) as Actual FROM clases WHERE dia BETWEEN '"+Inicio+"' AND '"+Fin+"' AND club='"+Club+"'\
                                     AND segmentacion = true GROUP BY nombre"))
    cancha = [row for row in cancha_]
    # APARTADOS EN GYM 
    apartados_gym_ = db.engine.execute(text("SELECT sum(cupo_actual) FROM clases WHERE dia BETWEEN '"+Inicio+"' AND '"+Fin+"' AND club='"+Club+"' \
                                    AND (nombre LIKE 'GYM%' OR NOMBRE LIKE 'GIM%')"))
    apartados_gym = [row for row in apartados_gym_]
    # CITAS AGENDADAS
    cupo_actual_ = db.engine.execute(text("SELECT sum(cupo_actual) FROM clases WHERE dia BETWEEN '"+Inicio+"' AND '"+Fin+"' AND club='"+Club+"'"))
    cupo_actual = [row for row in cupo_actual_]
    # MAS POPULAR
    usuarios_fitness_ = db.engine.execute(text("SELECT nombre  FROM clases WHERE dia BETWEEN '"+Inicio+"' AND '"+Fin+"' AND club='"+Club+"' ORDER BY cupo_actual\
                                         DESC FETCH FIRST 1 ROW ONLY"))
    usuarios_fitness = [row for row in usuarios_fitness_]
    # USUARIOS NUEVOS
    usuarios_totales_ = db.engine.execute(text("SELECT SUM(CUPO_ACTUAL) FROM clases WHERE nombre IN ('INDOOR CYCLING','STRETCH','GAP','HI-LOW', 'EXTREME WORKOUT','PILATES',\
        'YOGA ALTERNATIVA','HIIT','AEREO','FITNESS ATTACK','BAILE FITNESS','YOGA FLOW', 'JUMPING','BAILE FITNESS','POLE FITNESS','POLE FITNESS','STRETCHING','YOGA','CLINICA DE YOGA',\
        'STEP','HIT', 'FITNESS PUMP','TOTAL BARRE','AQUA FITNESS','DANCE REVOLUTION','BAILE DE SALON','TRX','CARDIO BOX', 'BOOT CAMP','ACRO YOGA INDIVIDUAL') \
        and club='"+Club+"' AND DIA BETWEEN '"+Inicio+"' AND '"+Fin+"'"))
    usuarios_totales = [row for row in usuarios_totales_]
    print(usuarios_totales)
    return render_template('reportes/Asistencias/dashboard.html', fecha_title=fecha_title, sala=sala, cancha=cancha, lunes=Inicio, domingo=Fin,\
                            apartados_gym=apartados_gym, usuarios_fitness=usuarios_fitness, usuarios_totales=usuarios_totales, cupo_actual=cupo_actual)

#===================================================================[ESPECIALES]===================================================================#
@reportes.route("/reportes/especiales/menu/promociones")
@login_required
def reportes_especiales_menu_promociones():
    # ENVIO CITA
    url = day.url_api_app+'alpha/reportePromociones'
    headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
    datos_envio = {}
    r = requests.get(url, headers=headers, json=datos_envio)
    resp = r.json()
    return render_template('reportes_especiales/Promociones/resultado.html', resp=resp)

@reportes.route("/reportes/especiales/menu/usuarios_sp", methods=['GET', 'POST'])
@login_required
def reportes_especiales_menu_usuarios_sp():
    # DATA SALA
    fecha_inicio = request.form.get("Fecha_Inicio")
    fecha_fin = request.form.get("Fecha_Fin")
    # ENVIO CITA
    url = day.url_api_app+'alpha/reporte'
    headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
    datos_envio = {'idClub': 4, 'fechaInicio':fecha_inicio, 'fechaFin':fecha_fin}
    r = requests.post(url, headers=headers, json=datos_envio)
    resp = r.json()
    return render_template('reportes_especiales/Usuarios_SP/resultado.html', resp=resp)

@reportes.route("/reportes/especiales/menu/parking_sp", methods=['GET', 'POST'])
@login_required
def reportes_especiales_menu_parking_sp():
    from models.models import db
    # DATA SALA
    fecha_inicio = request.form.get("Fecha_Inicio")
    fecha_fin = request.form.get("Fecha_Fin")
    # DATOS
    accesos_tag_ = db.engine.execute(text("select hora_entrada as hora_evento, (select CASE  WHEN  sentido THEN 'ENTRADA' ELSE 'SALIDA' END AS SENTIDO from caseta_antena where\
    caseta_antena.antena_id=registro_parking.id_antena and caseta_antena.caseta_id=registro_parking.id_caseta ),registro_tag.id_chip,tipo_acceso.nombre,id_antena,id_caseta\
    from registro_parking \
    full outer join registro_tag on registro_parking.id_chip=registro_tag.id\
    full outer join parking_usuario on id_parking=id_venta_detalle\
    full outer join tipo_acceso on tipo_acceso.id=registro_parking.tipo_Acceso \
    join caseta on caseta.id=registro_parking.id_caseta join club on caseta.club_id=club.idclub\
    where hora_entrada between '"+fecha_inicio+" 00:00:00' and '"+fecha_fin+" 23:59:59' and club.nombre='Sports Plaza'  order by hora_evento"))
    resp = [row for row in accesos_tag_]
    return render_template('reportes_especiales/Parking_SP/resultado.html', resp=resp)

@reportes.route("/reportes/especiales/menu/historico_accesos", methods=['GET', 'POST'])
@login_required
def reportes_especiales_menu_historico_accesos():
    from models.models import db
    # DATA RECIBO
    fecha_inicio = request.form.get("Fecha_Inicio") #YY-MM-DD
    fecha_fin = request.form.get("Fecha_Fin")
    club = request.form.get("Club")
    # DATOS
    accesos_tag_ = db.engine.execute(text("select hora_entrada as hora_evento, (select CASE  WHEN  sentido THEN 'ENTRADA' ELSE 'SALIDA' END AS SENTIDO from caseta_antena where\
    caseta_antena.antena_id=registro_parking.id_antena and caseta_antena.caseta_id=registro_parking.id_caseta ),registro_tag.id_chip,tipo_acceso.nombre,id_antena,id_caseta\
    from registro_parking \
    full outer join registro_tag on registro_parking.id_chip=registro_tag.id\
    full outer join parking_usuario on id_parking=id_venta_detalle\
    full outer join tipo_acceso on tipo_acceso.id=registro_parking.tipo_Acceso \
    join caseta on caseta.id=registro_parking.id_caseta join club on caseta.club_id=club.idclub\
    where hora_entrada between '"+fecha_inicio+" 00:00:00' and '"+fecha_fin+" 23:59:59' and club.nombre='"+club+"'  order by hora_evento"))
    resp = [row for row in accesos_tag_]
    return render_template('reportes_especiales/Parking_Accesos/resultado.html', resp=resp, club=club)

@reportes.route("/reportes/especiales/menu/historico_accesos/qr", methods=['GET', 'POST'])
@login_required
def reportes_especiales_menu_historico_accesos_qr():
    from models.models import db
    # DATA RECIBO
    fecha_inicio = request.form.get("Fecha_Inicio") #YY-MM-DD
    fecha_fin = request.form.get("Fecha_Fin")
    club = request.form.get("Club")
    # DATOS
    accesos_qr_ = db.engine.execute(text("SELECT * FROM registro_qr_dia\
    WHERE hora_evento between '"+fecha_inicio+" 00:00:00' and '"+fecha_fin+"  23:59:59' AND club='"+club+"'\
    GROUP BY hora_evento,sentido,id_chip,id_caseta,nombre,id_antena,club ORDER BY hora_evento"))
    resp = [row for row in accesos_qr_]
    return render_template('reportes_especiales/Parking_Accesos/resultado.html', resp=resp, club=club)

@reportes.route("/reportes/especiales/menu/historico_accesos/qr/salidas", methods=['GET', 'POST'])
@login_required
def reportes_especiales_menu_historico_accesos_qr_salidas():
    from models.models import db
    # DATA RECIBO
    fecha_inicio = request.form.get("Fecha_Inicio") #YY-MM-DD
    fecha_fin = request.form.get("Fecha_Fin")
    club = request.form.get("Club")
    # DATOS 
    accesos_qr_ = db.engine.execute(text("SELECT * FROM REGISTRO_QR_DIA\
    WHERE HORA_EVENTO between '"+fecha_inicio+" 00:00:00' and '"+fecha_fin+"  23:59:59' AND club='"+club+"' AND SENTIDO='SALIDA'\
    GROUP BY hora_evento,sentido,id_chip,id_caseta,nombre,id_antena,club ORDER BY hora_evento"))
    resp = [row for row in accesos_qr_]
    return render_template('reportes_especiales/Parking_Accesos/resultado.html', resp=resp, club=club)

@reportes.route("/reportes/especiales/menu/historico_incidencias", methods=['GET', 'POST'])
@login_required
def reportes_especiales_menu_historico_incidencias():
    # DATA RECIBO
    fecha_inicio = request.form.get("Fecha_Inicio")
    fecha_fin = request.form.get("Fecha_Fin")
    club = request.form.get("Club")
    # ENVIO CITA
    url = day.url_api_app+'parking/amonestacionesPorTiempo'
    headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
    datos_envio = {'fechaInicio':fecha_inicio,'fechaFin':fecha_fin,'club':club}
    r = requests.post(url, headers=headers, json=datos_envio)
    resp = r.json()
    return render_template('reportes_especiales/Parking_Incidencias/resultado.html', resp=resp, club=club)
