from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField,\
    TextAreaField, SelectField, PasswordField, FloatField, TextField
from wtforms.fields.html5 import EmailField, DateTimeLocalField, DateField, DateTimeField,\
    SearchField
from flask_wtf.file import FileField
from wtforms.widgets import TextArea
from wtforms.validators import Required
from datetime import datetime

class FormCategoria(FlaskForm):
    nombre = StringField("Nombre:", validators=[Required("Tienes que introducir el dato")])
    submit = SubmitField('Enviar')

class LoginForm(FlaskForm):
    username = StringField('User', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Entrar')

class FormUsuario(FlaskForm):
    nombre = StringField('Nombre completo')
    email = StringField('Email')
    username = StringField('Login', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    admin =  SelectField("Admin", choices=[("false", "No"),("true", "Si")], default="No")
    user_fi =  SelectField("FI", choices=[("0", "No"),("1", "Si")], default="No")
    leader_fi =  SelectField("FI", choices=[("0", "No"),("1", "Si")], default="No")
    user_am =  SelectField("AM", choices=[("0", "No"),("1", "Si")], default="No")
    user_auditor =  SelectField("Auditor", choices=[("0", "No"),("1", "Si")], default="No")
    user_caseta =  SelectField("Caseta", choices=[("0", "No"),("1", "Si")], default="No")
    user_caseta_cim =  SelectField("Caseta Cimera", choices=[("0", "No"),("1", "Si")], default="No")
    user_deportes =  SelectField("Caseta", choices=[("0", "No"),("1", "Si")], default="No")
    user_gerente = SelectField("Gerente", choices=[("0", "No"),("1", "Si")], default="No")
    user_subgerente = SelectField("Subgerente", choices=[("0", "No"),("1", "Si")], default="No")
    user_rh =  SelectField("Rh", choices=[("0", "No"),("1", "Si")], default="No")
    user_rh_consulta =  SelectField("Rh", choices=[("0", "No"),("1", "Si")], default="No")
    user_aux =  SelectField("Rh", choices=[("0", "No"),("1", "Si")], default="No")
    user_pagos =  SelectField("Rh", choices=[("0", "No"),("1", "Si")], default="No")
    user_reportes =  SelectField("Rh", choices=[("0", "No"),("1", "Si")], default="No")
    user_parking =  SelectField("Rh", choices=[("0", "No"),("1", "Si")], default="No")
    user_apartados =  SelectField("Rh", choices=[("0", "No"),("1", "Si")], default="No")
    user_qr_pases =  SelectField("Rh", choices=[("0", "No"),("1", "Si")], default="No")
    user_registro =  SelectField("Registro", choices=[("0", "No"),("1", "Si")], default="No")
    user_logs =  SelectField("Registro", choices=[("0", "No"),("1", "Si")], default="No")
    user_configuracion =  SelectField("Registro", choices=[("0", "No"),("1", "Si")], default="No")
    user_facturas =  SelectField("Facturas", choices=[("0", "No"),("1", "Si")], default="No")
    user_rutinas =  SelectField("Registro", choices=[("0", "No"),("1", "Si")], default="No")
    user_domiciliacion =  SelectField("Domiciliacion", choices=[("0", "No"),("1", "Si")], default="No")
    alpha_2 =  SelectField("Alpha 2", choices=[("0", "No"),("1", "Si")], default="No")
    alpha_3 =  SelectField("Alpha 3", choices=[("0", "No"),("1", "Si")], default="No")
    alpha_4 =  SelectField("Alpha 4", choices=[("0", "No"),("1", "Si")], default="No")
    cimera =  SelectField("Cimera", choices=[("0", "No"),("1", "Si")], default="No")
    submit = SubmitField('Aceptar')

class FormChangePassword(FlaskForm):
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Aceptar')

class FormAcceso(FlaskForm):
    id = IntegerField('ID', validators=[Required()])
    submit = SubmitField('Consultar')

class AccesoForm(FlaskForm):
    id = IntegerField('ID', validators=[Required()])
    submit = SubmitField('Consultar')

class ClienteForm(FlaskForm):
    idcliente = SelectField('ID',default=0)
    nombre_completo = StringField("Nombre:", default=0)
    submit = SubmitField('Consultar')

#TEST

class FormCita(FlaskForm):
    id = IntegerField('ID', validators=[Required()])
    dia_apartado = SelectField(u'Dia')
    actividad = SelectField(u'Apartado')
    submit = SubmitField('Agendar Cita')

class FormCitaFuturo(FlaskForm):
    id = IntegerField('ID', validators=[Required()])
    dia_apartado_futuro = SelectField(u'Dia')
    actividad_futuro = SelectField(u'Apartado')
    submit = SubmitField('Agendar Cita Futura')

# TEST DIAS
class FormCita_lunes(FlaskForm):
    id = IntegerField('ID', validators=[Required()])
    dia_apartado = SelectField(u'Dia')
    actividad = SelectField(u'Apartado')
    submit = SubmitField('Agendar Cita')

class FormCita_martes(FlaskForm):
    id = IntegerField('ID', validators=[Required()])
    dia_apartado = SelectField(u'Dia')
    actividad = SelectField(u'Apartado')
    submit = SubmitField('Agendar Cita')

class FormCita_miercoles(FlaskForm):
    id = IntegerField('ID', validators=[Required()])
    dia_apartado = SelectField(u'Dia')
    actividad = SelectField(u'Apartado')
    submit = SubmitField('Agendar Cita')

class FormCita_jueves(FlaskForm):
    id = IntegerField('ID', validators=[Required()])
    dia_apartado = SelectField(u'Dia')
    actividad = SelectField(u'Apartado')
    submit = SubmitField('Agendar Cita')

class FormCita_viernes(FlaskForm):
    id = IntegerField('ID', validators=[Required()])
    dia_apartado = SelectField(u'Dia')
    actividad = SelectField(u'Apartado')
    submit = SubmitField('Agendar Cita')

class FormCita_sabado(FlaskForm):
    id = IntegerField('ID', validators=[Required()])
    dia_apartado = SelectField(u'Dia')
    actividad = SelectField(u'Apartado')
    submit = SubmitField('Agendar Cita')

class FormCita_domingo(FlaskForm):
    id = IntegerField('ID', validators=[Required()])
    dia_apartado = SelectField(u'Dia')
    actividad = SelectField(u'Apartado')
    submit = SubmitField('Agendar Cita')

class FormInfoSala(FlaskForm):
    dia_apartado = SelectField(u'Dia')
    sala_apartado = SelectField(u'Apartado')
    submit = SubmitField('Informe Sala')

class FormQRPases(FlaskForm):
    id_prodserv = SelectField(u'Producto')
    venta_detalle = SelectField(u'Venta Detalle')
    submit = SubmitField('Generar Pase')

class FormDiasOxxo(FlaskForm):
    dias_para_pago = SelectField("Oxxo", choices=[("1", "1 Día"),("2", "2 Días"),("3", "3 Días"),("4", "4 Días"),("5", "5 Días")], default="1")
