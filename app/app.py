from flask import Flask
from cachetools import cached

@cached({})
def create_app():
    app = Flask(__name__)

    return app
