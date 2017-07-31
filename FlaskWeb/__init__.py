"""
The flask application package.
"""
set FLASK_DEBUG=1
from flask import Flask

app = Flask(__name__)

import FlaskWeb.views
