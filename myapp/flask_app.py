import logging
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from myapp import app_config
import appengine_config

app = Flask(__name__)
app.config.from_object(__name__)

if appengine_config.GAE_DEV:
    logging.info('Using a dummy secret key.')
    app.secret_key = 'my-secure-key'
    app.debug = True
else:
    app.secret_key = app_config.app_secure_key

DEBUG = True
csrf = CSRFProtect(app)
