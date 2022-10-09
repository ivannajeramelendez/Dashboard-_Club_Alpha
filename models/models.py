from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float, Sequence
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func 
from sqlalchemy.orm import relationship, backref
from app.app import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class Categorias(db.Model):
    """Categorías de las Publicaciones"""
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    #articulos = relationship("Articulos", cascade="all, delete-orphan", backref="Categorias", lazy='dynamic')

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Clases(db.Model):
    __tablename__ = 'clases'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100))
    tecnico = Column(String(100))
    tipo_actividad = Column(String(100))
    color = Column(String(100))
    lugar = Column(String(100))
    duracion = Column(Integer)
    nivel = Column(String(100))
    hora = Column(String(100))
    cupo_actual = Column(Integer)
    cupo_maximo = Column(Integer)
    rango = Column(String(100))
    disponible = Column(Boolean)
    dia = Column(String(100))
    club = Column(String(100))
    id_apartados = Column(String(100))
    paga = Column(Integer)
    segmentacion = Column(Boolean)
    
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Registro_Gimnasio(db.Model):
    __tablename__ = 'registro_gimnasio'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_cliente = Column(Integer)
    id_terminal = Column(Integer)
    registro_acceso = Column(String(100))
    id_apartados = Column(UUID(as_uuid=True), default=uuid.uuid4)
    
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Pase_Consumido(db.Model):
    __tablename__ = 'pase_consumido'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha_redencion = Column(String(100))
    apartado_usuario = Column(Integer)
    pase_usuario = Column(String(100))
    terminal_redencion_id = Column(Integer)
    activo = Column(Boolean)
    created_by = Column(String(100))
    created = Column(String(100))
    updated = Column(String(100))
    updated_by = Column(String(100))
    
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Clientes_Actuales(db.Model):
    __tablename__ = 'cliente'
    idcliente = Column(Integer, primary_key=True)
    nomembresia = Column(String(100))
    nombre = Column(String(100))
    apellidopaterno = Column(String(100))
    apellidomaterno = Column(String(100))
    nombrecompleto = Column(String(100))
    servicio = Column(String(100))
    estatusacceso = Column(String(100))
    tipoacceso = Column(Boolean)
    domiciliopago = Column(Boolean)
    inicioactividades = Column(String(100))
    sexo = Column(String(100))
    fechanacimiento = Column(String(100))
    mensualidadpagada = Column(Boolean)
    email = Column(String(100))
    fechafinacceso = Column(String(100))
    idsexo = Column(Integer)
    nacionalidad = Column(String(100))
    telefono = Column(String(100))
    idclientegrupo = Column(Integer)
    idclientesector = Column(Integer)
    idcaptura = Column(Integer)
    idcapturafecha = Column(Integer)
    activo = Column(Boolean)
    fechacreacion = Column(String(100))
    fechamodificacion = Column(String(100))
    idclub = Column(Integer)
    tipocliente = Column(Integer)
    categoria = Column(Integer)
    estatuscliente = Column(Integer)
    estatusmembresia = Column(Integer)
    estatuscobranza = Column(Integer)
    tieneacceso = Column(Boolean)
    tipomembresia = Column(Integer)
    id_foto = Column(Integer)
    
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Dia_Apartados(db.Model):
    __tablename__ = 'ca_apartados'
    id_apartados = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dia = Column(String(100))
    
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Qr_Pases(db.Model):
    __tablename__ = 'pase_usuario'
    id_venta_detalle = Column(Integer, primary_key=True)
    activo = Column(Boolean(100))
    cantidad = Column(Integer)
    created = Column(String(100))
    created_by = Column(String(100))
    disponibles = Column(Integer)
    f_compra = Column(String(100))
    id_prod = Column(Integer)
    updated = Column(String(100))
    updated_by = Column(String(100))
    idcliente = Column(Integer)
    concepto = Column(String(100))
    consumido = Column(Integer)
    
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Usuarios(db.Model):
    """Usuarios"""
    __tablename__ = 'usuarios_pagina'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password_hash = Column(String(128), nullable=False)
    nombre = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    admin = Column(Integer)
    user_fi = Column(Integer)
    leader_fi = Column(Integer)
    user_am = Column(Integer)
    user_auditor = Column(Integer)
    user_caseta = Column(Integer)
    user_caseta_cim = Column(Integer)
    user_gerente = Column(Integer)
    user_subgerente = Column(Integer)
    user_deportes = Column(Integer)
    user_rh = Column(Integer)
    user_rh_consulta = Column(Integer)
    user_aux = Column(Integer)
    user_pagos = Column(Integer)
    user_reportes = Column(Integer)
    user_parking = Column(Integer)
    user_apartados = Column(Integer)
    user_qr_pases = Column(Integer)
    user_registro = Column(Integer)
    user_logs = Column(Integer)
    user_configuracion = Column(Integer)
    user_rutinas = Column(Integer)
    user_facturas = Column(Integer)
    user_domiciliacion = Column(Integer)
    alpha_2 = Column(Integer)
    alpha_3 = Column(Integer)
    alpha_4 = Column(Integer)
    cimera = Column(Integer)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Flask-Login integracion
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def is_admin(self):
        return self.admin

    def is_user_auditor(self):
        return self.user_auditor

    def is_user_rh(self):
        return self.user_rh

    def is_user_rh_consulta(self):
        return self.user_rh_consulta

    def is_user_aux(self):
        return self.user_aux

    def is_user_pagos(self):
        return self.user_pagos

    def is_user_reportes(self):
        return self.user_reportes

    def is_user_registro(self):
        return self.user_registro

    def is_user_gerente(self):
        return self.user_gerente

    def is_user_subgerente(self):
        return self.user_subgerente

    def is_user_caseta(self):
        return self.user_caseta

    def is_user_caseta_cim(self):
        return self.user_caseta_cim

    def is_user_apartados(self):
        return self.user_apartados

    def is_user_qr_pases(self):
        return self.user_qr_pases

    def is_user_parking(self):
        return self.user_parking

    def is_user_deportes(self):
        return self.user_deportes

    def is_user_logs(self):
        return self.user_logs

    def is_user_configuracion(self):
        return self.user_configuracion
    
    def is_user_rutinas(self):
        return self.user_rutinas
    
    def is_user_facturas(self):
        return self.user_facturas
    
    def is_user_domiciliacion(self):
        return self.user_domiciliacion

    def is_user_fi(self):
        return self.user_fi

    def is_leader_fi(self):
        return self.leader_fi
    
    def is_user_am(self):
        return self.user_am
    
    def is_alpha_2(self):
        return self.alpha_2

    def is_alpha_3(self):
        return self.alpha_3

    def is_alpha_4(self):
        return self.alpha_4

    def is_cimera(self):
        return self.cimera

class Clientes_Club(db.Model):
    __tablename__ = 'clientes_club'
    idcliente = Column(Integer, primary_key=True)
    nombre_completo = Column(String(100), nullable=False)
    club = Column(Integer)
    activo = Column(String(100))
    
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Ejercicios_Rutinas(db.Model):
    __tablename__ = 'ejercicio'
    id = Column(Integer, primary_key=True)
    activo = Column(String(100))
    created = Column(String(100))
    grupo_muscular = Column(String(100))
    maquina = Column(String(100))
    nombre = Column(String(100))
    ruta = Column(String(100))
    ruta_video = Column(String(100))
    segmento = Column(String(100))
    updated = Column(String(100))
    
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class SCRUM_kanban(db.Model):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True)
    title = Column(db.String(100), unique=True, nullable=False, primary_key=True)
    status = Column(db.String(100), nullable=False)
    user_id = Column(db.Integer, db.ForeignKey('usuarios_pagina.id'))
    
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class User(db.Model):
    __tablename__ = 'user_jwt'
    id = Column(Integer, primary_key = True)
    public_id = Column(String(50), unique = True)
    name = Column(String(100))
    email = Column(String(70), unique = True)
    password = Column(String(80))

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))
## ======================================================================================= ##