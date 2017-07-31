"""
The flask application package.
"""
export FLASK_DEBUG=1
from flask import Flask

app = Flask(__name__)

import FlaskWeb.views
