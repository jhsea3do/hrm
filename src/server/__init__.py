from flask import Flask
from .ctrls import public, main, js
from .api import api

app = Flask(__name__, static_url_path='')
app.register_blueprint(main, url_prefix='/')
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(public, url_prefix='/')
app.register_blueprint(js, url_prefix='/')
