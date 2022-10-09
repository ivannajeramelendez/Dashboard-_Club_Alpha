from app import api, day
import os
import sshtunnel

SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
DEBUG = True

tunnel = sshtunnel.SSHTunnelForwarder((day.ip_sql_sesion), ssh_username=day.user_api_app, ssh_password=day.passwd_api_app, remote_bind_address=('localhost', 5432))
tunnel.start()

# POSTGREST
#SQLALCHEMY_DATABASE_URI = "postgresql://postgres:XXX@XXX:5432/XXX" ##CONEXION NORMAL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:XXX@XXX:{}/XXX'.format(tunnel.local_bind_port)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_SIZE = 30
SQLALCHEMY_MAX_OVERFLOW = -1 #CONEXIONES SIMULTANEAS -1

