import requests
from app import api, day

# MES VIGENTE
mes_inicio = '2022-10-01'
mes_fin = '2022-10-31'

# ENDPOINT PARA CAMBIAR DE PRODUCTIVO
ip_sql_sesion = 'XXX' # PRODUCTIVO
url_api_app = 'http://XXX/' # PRODUCTIVO
user_api_app = 'XXX' # PRODUCTIVO
passwd_api_app = 'XXX' # PRODUCTIVO

# TOKEN
url_token = day.url_api_app+'auth/login'
datos_token = {"nombreUsuario": "XXX", "password": "XXX"}
r_token = requests.post(url_token, json=datos_token)
resp_token = r_token.json()
resp_api_token = resp_token['token']