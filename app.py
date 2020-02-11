import os
import json
from textwrap import dedent

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go
import numpy as np
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from dash.dependencies import Input, Output, State

import base64
import json
import pandas as pd
import plotly
import io

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from jose import jwt
from six.moves.urllib.parse import urlencode
from six.moves.urllib.request import urlopen
import uuid

#Sets global vars
from globals import *

#We begin by creating a base Flask server
flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
flask_app.debug = False


@flask_app.route('/')
def index_page():
    return "Hello, world"

#We add Dash app to our Flask server
from regression_explorer import dash_app
dash_template = open(TEMPLATE_PATH + "/dash_base.html",'r').read()
app_dash= dash_app(flask_app,"Data Explorer",template=dash_template,DATASTORE_PATH=DATASTORE_PATH).getApp()

# Rout to App
@flask_app.route('/dashboard')
def render_dashboard():
    try:
        ss_id = session['ss_id']
    except:
        ss_id = str(uuid.uuid4())
        session['ss_id'] = ss_id

    print("Current Session : %s " % (ss_id))

    return app_dash.index()

#server = app_dash.server
server = flask_app

if __name__ == '__main__':
    server.run(host='0.0.0.0',port=8000)
