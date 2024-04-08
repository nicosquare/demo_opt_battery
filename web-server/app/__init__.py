from flask import Flask

app = Flask(__name__, static_folder='../app/build', static_url_path='/')

app.config.from_object("config.DevelopmentConfig")

from app import main
from app import settings

