from flask import Flask, render_template, redirect, url_for, request, abort, flash,\
    session, Response, Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required,\
    current_user
from psycopg2 import OperationalError
from sqlalchemy.sql.expression import asc
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, desc
from sqlalchemy.sql.functions import concat
from sqlalchemy import DateTime, select, distinct, tuple_, text
from app import api, day
from datetime import date, datetime, timedelta
import requests
import json
    # FORMULARIOS
from forms.forms import *
app = Flask(__name__)
app.config.from_object(api)

rutinas = Blueprint('rutinas', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

# =================================================================================== [EJERCICIOS] ======================================================================= #
@rutinas.route("/rutinas/ejercicios", methods=['GET', 'POST'])
@rutinas.route("/rutinas/ejercicios/<int:page>", methods=['GET', 'POST'])
@login_required
def rutinas_ejercicios(page=1):
    from models.models import Ejercicios_Rutinas,db
    # PAGINACION TOTAL
    per_page = 20 
    ejercicios = Ejercicios_Rutinas.query.filter(Ejercicios_Rutinas.activo == 'true').order_by(Ejercicios_Rutinas.created.desc()).paginate(page,per_page,error_out=False)
    # AGREGAR
    if request.method == 'POST' and request.form.get("metodo") == 'nuevo':
        # DATOS
        Url = request.form.get('url')
        Url_video = request.form.get('url_video')
        Nombre = request.form.get('nombre')
        Grupo = request.form.get('grupo')
        Maquina = request.form.get('maquina')
        Segmento = request.form.get('segmento')
        # ENVIO DATOS
        url = day.url_api_app+'rutina/crearEjercicio'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'ruta': Url, "nombre": Nombre, "grupoMuscular":Grupo, 'maquina':Maquina, 'rutaVideo':Url_video, 'segmento':Segmento}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("Nombre")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rutinas.rutinas_ejercicios'))
    if request.method == 'POST' and request.form.get("metodo") == 'editar':
        # DATOS
        Url = request.form.get('url')
        Url_video = request.form.get('url_video')
        Nombre = request.form.get('nombre')
        Grupo = request.form.get('grupo')
        Maquina = request.form.get('maquina')
        ID = request.form.get('id')
        Segmento = request.form.get('segmento')
        # ENVIO DATOS
        url = day.url_api_app+'rutina/actualizarEjercicio'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'id':ID,'ruta': Url, "nombre": Nombre, "grupoMuscular":Grupo, 'maquina':Maquina, 'rutaVideo':Url_video, 'segmento':Segmento}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("Nombre")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rutinas.rutinas_ejercicios'))
    if request.method == 'POST' and request.form.get("metodo") == 'eliminar':
        # DATOS
        ID = request.form.get('id')
        # ENVIO DATOS
        url = day.url_api_app+'rutina/deleteEjercicio/'+ID
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r = requests.get(url, headers=headers)
        text = request.form.get("id")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rutinas.rutinas_ejercicios'))
    return render_template('rutinas/Ejercicios/consulta.html', ejercicios=ejercicios)

# =================================================================================== [CREAR RUTINA] ======================================================================= #
@rutinas.route("/rutinas/creacion/cliente/nueva", methods=['GET', 'POST'])
@login_required
def rutinas_creacion_rutinas():
    from models.models import db
    ID_Cliente = request.form.get("ID_Cliente")
    if request.method == 'POST' and request.form.get("crear_rutina") == 'crear_rutina':
        # EJERCICIOS
        ejercicios_ = db.engine.execute(("SELECT * FROM ejercicio WHERE activo = 'true'"))
        ejercicios = [row for row in ejercicios_]
        # ID
        id_cliente = ID_Cliente
        # DATOS 
        url = day.url_api_app+'alpha/clienteRutina/'+id_cliente
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r = requests.get(url, headers=headers)
        cliente = r.json()
        return render_template('rutinas/Rutinas/consulta.html', ejercicios=ejercicios, cliente=cliente)
    if request.method == 'POST' and request.form.get("enviar_rutina") == 'enviar_rutina':
        # DATOS
        Nombre_Rutina = request.form.get('nombre_rutina')
        Objetivo_Rutina = request.form.get('objetivo_rutina')
        Dia_Inicio = request.form.get('dia_inicio')
        ID_Cliente = request.form.get('ID_Cliente')
        id = str(ID_Cliente)
        # LISTAS
        Ejecicio = request.form.getlist('ejercicio')
        Repeticiones = request.form.getlist('repeticiones')
        Series = request.form.getlist('series')
        Orden = request.form.getlist('orden')
        # ENVIO DATOS
        url = day.url_api_app+'rutina/agregarRutinaCliente'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {"body":[{'idCliente': ID_Cliente,'nombreRutina': Nombre_Rutina,'nombreObjetivo': Objetivo_Rutina,'semanas': Dia_Inicio,\
                        'rutina': [{'id_ejercicio': a, 'repeticiones': r,'series': s,'orden': o} for a,r,s,o in zip(Ejecicio,Repeticiones,Series,Orden)] }] }
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("test")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            return redirect(url_for('rutinas.rutinas_creacion_rutinas', ID_Cliente=id,tipo='datos'))
    if request.args.get("tipo") == 'datos':
        # DATOS
        IDCliente = request.args.get('ID_Cliente')
        # DATOS 
        url_foto = day.url_api_app+'alpha/clienteRutina/'+IDCliente
        headers_foto = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r_foto = requests.get(url_foto, headers=headers_foto)
        cliente_foto = r_foto.json()
        # ENVIO DATOS
        url = day.url_api_app+'rutina/obtenerRutina/'+IDCliente
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r = requests.get(url, headers=headers)
        datos = r.json()
        return render_template('rutinas/Consulta/consulta_rutinas.html', datos=datos,cliente_foto=cliente_foto)
    if request.form.get("enviar_rutina") == 'final_rutina':
        # DATOS
        ID_Cliente = request.form.get('ID_Cliente')
        Nombre_Rutina = request.form.get('nombre_rutina')
        Objetivo_Rutina = request.form.get('objetivo_rutina')
        Dia_Inicio = request.form.get('dia_inicio')
        # LISTAS
        Ejecicio = request.form.getlist('ejercicio')
        Repeticiones = request.form.getlist('repeticiones')
        Series = request.form.getlist('series')
        Orden = request.form.getlist('orden')
        # ENVIO DATOS
        url = day.url_api_app+'rutina/asignarRutina'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {"body":[{'idCliente': ID_Cliente,'nombreRutina': Nombre_Rutina,'nombreObjetivo': Objetivo_Rutina,'semanas': Dia_Inicio,\
                        'rutina': [{'id_ejercicio': a, 'repeticiones': r,'series': s,'orden': o} for a,r,s,o in zip(Ejecicio,Repeticiones,Series,Orden)] }] }
        r = requests.post(url, headers=headers, json=datos_envio)
        if r == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rutinas.rutinas_agenda'))
    else:
        return redirect(url_for('rutinas.rutinas_agenda'))

# ================================================================================= [CONSULTA RUTINA] ======================================================================= #
@rutinas.route("/rutinas/consulta/rutina", methods=['GET', 'POST'])
@login_required
def rutinas_consulta_rutina():
    if request.method == 'POST' and request.form.get("consultar") == 'consultar':
        from models.models import db
        IDCliente = request.form.get("ID_Cliente")
        # DATOS 
        url = day.url_api_app+'alpha/clienteRutina/'+IDCliente
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r = requests.get(url, headers=headers)
        cliente = r.json()
        # DATOS RUTINA
        url_ejercicios = day.url_api_app+'rutina/obtenerRutina/'+IDCliente
        headers_ejercicios = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r_ejercicios = requests.get(url_ejercicios, headers=headers_ejercicios)
        if r_ejercicios.status_code == 200:
            ejercicios = r_ejercicios.json()
            return render_template('rutinas/Usuario/consulta_rutinas.html', cliente=cliente, ejercicios=ejercicios)
        else:
            resp_api = 'El usuario no tiene una rutina asignada'
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rutinas.rutinas_agenda'))
    if request.method == 'POST' and request.form.get("eliminar") == 'eliminar':
        # DATOS
        ID = request.form.get('ID_Cliente')
        # ENVIO DATOS
        url = day.url_api_app+'rutina/deleteRutina/'+ID
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r = requests.get(url, headers=headers)
        text = request.form.get("id")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rutinas.rutinas_agenda'))
    else:
        return redirect(url_for('rutinas.rutinas_agenda'))

# ================================================================================= [AGENDA ASESORES] ======================================================================= #
@rutinas.route("/rutinas/agenda", methods=['GET', 'POST'])
@login_required
def rutinas_agenda():
    from models.models import db
    # INICIO
    today = date.today() # DIA ACTUAL
    fecha_title = today.strftime("%d de %B del %Y")
    # FECHA
    dias_dash_ = db.engine.execute(("SELECT nombre,fecha FROM dias_semana"))
    dias_dash = [row for row in dias_dash_]
    lunes = dias_dash[0]['fecha']
    martes = dias_dash[1]['fecha']
    miercoles = dias_dash[2]['fecha']
    jueves = dias_dash[3]['fecha']
    viernes = dias_dash[4]['fecha']
    sabado = dias_dash[5]['fecha']
    domingo = dias_dash[6]['fecha']
    # SEGMENTACION DEL ACCESOR
    if current_user.alpha_2 == 1 and current_user.user_rutinas == 1:
        # VIEWS
        lun_dash_ = db.engine.execute(("select * from agenda where club='Club Alpha 2' and dia='"+lunes+"' order by hora"))
        lun_dash = [row for row in lun_dash_]
        mar_dash_ = db.engine.execute(("select * from agenda where club='Club Alpha 2' and dia='"+martes+"' order by hora"))
        mar_dash = [row for row in mar_dash_]
        mie_dash_ = db.engine.execute(("select * from agenda where club='Club Alpha 2' and dia='"+miercoles+"' order by hora"))
        mie_dash = [row for row in mie_dash_]
        jue_dash_ = db.engine.execute(("select * from agenda where club='Club Alpha 2' and dia='"+jueves+"' order by hora"))
        jue_dash = [row for row in jue_dash_]
        vie_dash_ = db.engine.execute(("select * from agenda where club='Club Alpha 2' and dia='"+viernes+"' order by hora"))
        vie_dash = [row for row in vie_dash_]
        sab_dash_ = db.engine.execute(("select * from agenda where club='Club Alpha 2' and dia='"+sabado+"' order by hora"))
        sab_dash = [row for row in sab_dash_]
        dom_dash_ = db.engine.execute(("select * from agenda where club='Club Alpha 2' and dia='"+domingo+"' order by hora"))
        dom_dash = [row for row in dom_dash_]
    elif current_user.alpha_3 == 1 and current_user.user_rutinas == 1:
        lun_dash_ = db.engine.execute(("select * from agenda where club='Club Alpha 3' and dia='"+lunes+"' order by hora"))
        lun_dash = [row for row in lun_dash_]
        mar_dash_ = db.engine.execute(("select * from agenda where club='Club Alpha 3' and dia='"+martes+"' order by hora"))
        mar_dash = [row for row in mar_dash_]
        mie_dash_ = db.engine.execute(("select * from agenda where club='Club Alpha 3' and dia='"+miercoles+"' order by hora"))
        mie_dash = [row for row in mie_dash_]
        jue_dash_ = db.engine.execute(("select * from agenda where club='Club Alpha 3' and dia='"+jueves+"' order by hora"))
        jue_dash = [row for row in jue_dash_]
        vie_dash_ = db.engine.execute(("select * from agenda where club='Club Alpha 3' and dia='"+viernes+"' order by hora"))
        vie_dash = [row for row in vie_dash_]
        sab_dash_ = db.engine.execute(("select * from agenda where club='Club Alpha 3' and dia='"+sabado+"' order by hora"))
        sab_dash = [row for row in sab_dash_]
        dom_dash_ = db.engine.execute(("select * from agenda where club='Club Alpha 3' and dia='"+domingo+"' order by hora"))
        dom_dash = [row for row in dom_dash_]
    elif current_user.cimera == 1 and current_user.user_rutinas == 1:
        lun_dash_ = db.engine.execute(("select * from agenda where club='CIMERA' and dia='"+lunes+"' order by hora"))
        lun_dash = [row for row in lun_dash_]
        mar_dash_ = db.engine.execute(("select * from agenda where club='CIMERA' and dia='"+martes+"' order by hora"))
        mar_dash = [row for row in mar_dash_]
        mie_dash_ = db.engine.execute(("select * from agenda where club='CIMERA' and dia='"+miercoles+"' order by hora"))
        mie_dash = [row for row in mie_dash_]
        jue_dash_ = db.engine.execute(("select * from agenda where club='CIMERA' and dia='"+jueves+"' order by hora"))
        jue_dash = [row for row in jue_dash_]
        vie_dash_ = db.engine.execute(("select * from agenda where club='CIMERA' and dia='"+viernes+"' order by hora"))
        vie_dash = [row for row in vie_dash_]
        sab_dash_ = db.engine.execute(("select * from agenda where club='CIMERA' and dia='"+sabado+"' order by hora"))
        sab_dash = [row for row in sab_dash_]
        dom_dash_ = db.engine.execute(("select * from agenda where club='CIMERA' and dia='"+domingo+"' order by hora"))
        dom_dash = [row for row in dom_dash_]
    # AGENDAR
    if request.method == 'POST' and request.form.get("tipo") == 'agendar':
        # DATOS
        IDCliente = request.form.get('id')
        Sala = request.form.get('sala')
        Asesor = request.form.get('asesor')
        # ENVIO DATOS
        url = day.url_api_app+'rutina/crearReserva'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': IDCliente, "id": Sala, "asesor":Asesor}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("Nombre")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rutinas.rutinas_agenda'))
    # CANCELAR
    if request.method == 'POST' and request.form.get("tipo") == 'cancelar':
        # DATOS
        IDCliente = request.form.get('id')
        Sala = request.form.get('sala')
        # ENVIO DATOS
        url = day.url_api_app+'rutina/cancelarReserva'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'usuario': IDCliente, "id": Sala}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("Nombre")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rutinas.rutinas_agenda'))
    # FOOTER
    return render_template('rutinas/Agenda/agenda.html', fecha_title=fecha_title, 
                            lun_dash=lun_dash,mar_dash=mar_dash,mie_dash=mie_dash,jue_dash=jue_dash,vie_dash=vie_dash,sab_dash=sab_dash,dom_dash=dom_dash,
                            lunes=lunes, martes=martes, miercoles=miercoles, jueves=jueves, viernes=viernes, sabado=sabado, domingo=domingo)

# ================================================================================= [AGENDA ASESORES] ======================================================================= #
@rutinas.route("/rutinas/bascula", methods=['GET', 'POST'])
@login_required
def rutinas_pesaje():
    from models.models import db
    # INICIO
    today = date.today() # DIA ACTUAL
    fecha_title = today.strftime("%d de %B del %Y")
    # BASCULA
    if request.method == 'POST' and request.form.get("tipo") == 'envio_cliente':
        # DATOS
        IDCliente = request.form.get('ID_Cliente')
        tipo = "primero"
        # ENVIO DATOS
        url = day.url_api_app+'rutina/ultimoPesajeGeneral/'+IDCliente
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r = requests.get(url, headers=headers)
        dato = r.json()
        return render_template('rutinas/Pesaje/pesaje.html', fecha_title=fecha_title, dato=dato, tipo=tipo,IDCliente=IDCliente)
    if request.method == 'POST' and request.form.get("tipo") == 'envio_bascula':
        # DATOS
        IDCliente = request.form.get('IDCliente')
        Edad = request.form.get('Edad')
        Sexo = request.form.get('Sexo')
        Altura = request.form.get('Altura')
        Atleta = request.form.get('Atleta')
        Nivel_Actividad = request.form.get('Actividad')
        tipo = "segundo"
        # ENVIO DE DATOS A BASCULA
        if current_user.username == 'asesor.alpha_2':
            url = 'http://XXX'
        elif current_user.username == 'asesor.alpha_3':
            url = 'http://XXX'
        elif current_user.username == 'asesor.cimera':
            url = 'http://XXX'
        datos_envio = {"sexo": Sexo, 'edad': Edad, "altura":Altura, "atleta":Atleta, "nivelActividad":Nivel_Actividad}
        r = requests.post(url, json=datos_envio)
        dato = r.json()
        resp_api = dato
        return render_template('rutinas/Pesaje/pesaje.html', fecha_title=fecha_title, Edad=Edad,Sexo=Sexo,Altura=Altura,Nivel_Actividad=Nivel_Actividad, resp_api=resp_api,tipo=tipo,IDCliente=IDCliente)
    if request.method == 'POST' and request.form.get("tipo") == 'envio_fin':
        # DATOS
        Edad = request.form.get('Edad') # NO INCLUIRLA
        Sexo = request.form.get('Sexo')
        Altura = request.form.get('Altura')
        Atleta = request.form.get('Atleta')
        Nivel_Actividad = request.form.get('Actividad')
        Peso = request.form.get('Peso')
        Mas_Osea = request.form.get('MasaOsea')
        IMC = request.form.get('IMC')
        Edad_Metabolica = request.form.get('EdadMetabolica')
        Masa_Grasa = request.form.get('MasaGrasa')
        Agua = request.form.get('Agua')
        Calorias_Diarias = request.form.get('CaloriasDiarias')
        Masa_Magra = request.form.get('MasaMagra')
        Adiposidad = request.form.get('Adiposidad')
        Valoracion_Fisica = request.form.get('ValoracionFisica')
        TMB = request.form.get('TMB')
        IDUsuario = request.form.get('IDUsuario')
        IDTerminal = request.form.get('IDTerminal')
        # ENVIO DATOS
        url = day.url_api_app+'rutina/datosBascula'
        headers = {'Content-type': api.api_content}
        datos_envio = {'Sexo':Sexo,'Altura':Altura,'Atleta':Atleta,'NivelActividad':Nivel_Actividad, 'Peso':Peso, 'MasaOsea':Mas_Osea, 'IMC':IMC, 'EdadMetabolica':Edad_Metabolica, \
            'MasaGrasa':Masa_Grasa, 'Agua':Agua, 'CaloriasDiarias':Calorias_Diarias, 'MasaMagra':Masa_Magra, 'Adiposidad':Adiposidad, 'ValoracionFisica':Valoracion_Fisica, 'TMB':TMB, \
            'IDUsuario':IDUsuario, 'IDTerminal': IDTerminal}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("Edad")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rutinas.rutinas_agenda'))
    return render_template('rutinas/Pesaje/pesaje.html', fecha_title=fecha_title)

# ================================================================================= [ASIGNAR RUTINA] ======================================================================= #
@rutinas.route("/rutinas/asignar/rutina", methods=['GET', 'POST'])
@login_required
def rutinas_asignar_rutina():
    from models.models import db
    # INICIO
    today = date.today() # DIA ACTUAL
    fecha_title = today.strftime("%d de %B del %Y")
    # QUERY VIEW
    plantillas_ = db.engine.execute(("SELECT id,activo,nombre_objetivo,nombre_rutina,tipo_plantilla,semanas FROM rutina WHERE plantilla IS true"))
    plantillas = [row for row in plantillas_]
    plantilla_2_ = db.engine.execute(("select rutina.id ,rutina.activo,nombre_objetivo,nombre_rutina,tipo_plantilla,semanas,\
                dia,orden,repeticiones,series, ejercicio_id,grupo_muscular,maquina,ejercicio.nombre, ruta,ruta_video,segmento\
                from rutina join rutina_ejercicio on rutina_id=rutina.id join ejercicio on  ejercicio_id=ejercicio.id where plantilla is true"))
    plantilla_2 = [row for row in plantilla_2_]
    # NUEVA PLANTILLA
    if request.method == 'POST' and request.form.get("tipo") == 'nuevo':
        # DATOS
        Nombre = request.form.get('nombre')
        Objetivo = request.form.get('Objetivo')
        Semanas = request.form.get('semanas')
        Segmento = request.form.get('segmento')
        # LISTAS
        Ejecicio = request.form.getlist('ejercicio')
        Repeticiones = request.form.getlist('repeticiones')
        Series = request.form.getlist('series')
        Orden = request.form.getlist('orden')
        # ENVIO DATOS
        url = day.url_api_app+'rutina/crearPlantillaRutina'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {"body":[{'nombreRutina': Nombre,'nombreObjetivo': Objetivo,'semanas': Semanas,'tipoPlantilla': Segmento,\
                        'rutina': [{'id_ejercicio': a, 'repeticiones': r,'series': s,'orden': o} for a,r,s,o in zip(Ejecicio,Repeticiones,Series,Orden)] }] }
        print(datos_envio)
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("test")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rutinas.rutinas_asignar_rutina'))
    # EDITAR PLANTILLA
    if request.method == 'POST' and request.form.get("tipo") == 'editar':
        # DATOS
        Sala = request.form.get('id')
        # ENVIO DATOS
        url = day.url_api_app+'rutina/obtenerPlantilla/'+Sala
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r = requests.get(url, headers=headers)
        datos = r.json()
        return render_template('rutinas/Asignar/consulta_editar.html', datos=datos)
    if request.method == 'POST' and request.form.get("tipo") == 'editar_envio':
        # DATOS
        ID = request.form.get('id_rutina')
        Nombre = request.form.get('nombre_rutina')
        Objetivo = request.form.get('objetivo_rutina')
        Semanas = request.form.get('semanas')
        Segmento = request.form.get('segmento')
        Comentarios = request.form.get('comentarios')
        # LISTAS
        Ejecicio = request.form.getlist('ejercicio')
        Repeticiones = request.form.getlist('repeticiones')
        Series = request.form.getlist('series')
        Orden = request.form.getlist('orden')
        # ENVIO DATOS
        url = day.url_api_app+'rutina/actualizarPlantilla'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {'idPlantilla': ID,'nombreRutina': Nombre,'nombreObjetivo': Objetivo,'tipoPlantilla': Segmento,'comentarios': Comentarios,'semanas': Semanas,\
                        'ejercicios': [{'id_ejercicio': a, 'repeticiones': r,'series': s,'orden': o} for a,r,s,o in zip(Ejecicio,Repeticiones,Series,Orden)] }
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("test")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            print(dato)
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rutinas.rutinas_asignar_rutina'))
    # ELIMINAR PLANTILLA
    if request.method == 'POST' and request.form.get("tipo") == 'eliminar':
        # DATOS
        ID = request.form.get('id')
        # DATOS 
        url = day.url_api_app+'rutina/deletePlantilla/'+ID
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        r = requests.get(url, headers=headers)
        text = request.form.get("test")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rutinas.rutinas_asignar_rutina'))
    # ASIGNAR RUTINA
    if request.method == 'POST' and request.form.get("tipo") == 'asignar':
        # DATOS
        IDCliente = request.form.get('id_cliente')
        IDRutina = request.form.get('id_rutina')
        # ENVIO DATOS
        url = day.url_api_app+'rutina/asignarRutinaPlantilla'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {"usuario":IDCliente, "idRutina":IDRutina}
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("test")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rutinas.rutinas_asignar_rutina'))
    return render_template('rutinas/Asignar/consulta.html', fecha_title=fecha_title,plantillas=plantillas, plantilla_2=plantilla_2)
    
@rutinas.route("/rutinas/asignar/rutina/nuevo", methods=['GET', 'POST'])
@login_required
def rutinas_asignar_rutina_nuevo():
    from models.models import db
    # INICIO
    today = date.today() # DIA ACTUAL
    fecha_title = today.strftime("%d de %B del %Y")
    # EJERCIOS PARA PLANTILLA
    ejercicios_ = db.engine.execute(("SELECT * FROM ejercicio WHERE activo = 'true'"))
    ejercicios = [row for row in ejercicios_]
    if request.method == 'POST' and request.form.get("tipo") == 'nuevo':
        # DATOS
        Nombre = request.form.get('nombre')
        Objetivo = request.form.get('Objetivo')
        Semanas = request.form.get('semanas')
        Segmento = request.form.get('segmento')
        # LISTAS
        Ejecicio = request.form.getlist('ejercicio')
        Repeticiones = request.form.getlist('repeticiones')
        Series = request.form.getlist('series')
        Orden = request.form.getlist('orden')
        # ENVIO DATOS
        url = day.url_api_app+'rutina/crearPlantillaRutina'
        headers = {'Content-type': api.api_content, 'Authorization':'Bearer '+ day.resp_api_token}
        datos_envio = {"body":[{'nombreRutina': Nombre,'nombreObjetivo': Objetivo,'semanas': Semanas,'tipoPlantilla': Segmento,\
                        'rutina': [{'id_ejercicio': a, 'repeticiones': r,'series': s,'orden': o} for a,r,s,o in zip(Ejecicio,Repeticiones,Series,Orden)] }] }
        print(datos_envio)
        r = requests.post(url, headers=headers, json=datos_envio)
        text = request.form.get("test")
        if text == "":
            flash("El campo texto es obligatorio(*)", category='alert alert-danger')
        else:
            dato = r.json()
            resp_api = dato['respuesta']
            flash(resp_api, category='alert alert-success')
            return redirect(url_for('rutinas.rutinas_asignar_rutina'))
    return render_template('rutinas/Nuevo/consulta.html', fecha_title=fecha_title,ejercicios=ejercicios)