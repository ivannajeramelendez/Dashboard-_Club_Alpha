from app.app import app
from models.models import *
from getpass import getpass

app.config['DEBUG'] = True  # debugger.

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)