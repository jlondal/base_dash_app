import base64
import datetime
import io

import dash
from flask import session
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objs as go
import dash_table_experiments as dt
from textwrap import dedent

from . import components as drc
from . import data_management as ddm
from . import control_pannel as cp
from . import graphs as grp
from . import utils as utls

import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

class dash_app:

    app = None
    DATASTORE_PATH = ''

    #build our app
    def __init__(self,flask_app,title,template=None,DATASTORE_PATH=''):

        self.DATASTORE_PATH = DATASTORE_PATH
        self.app = dash.Dash(__name__,server=flask_app)

        self.app.title = title

        if template is not None:
            self.app.index_string = template

        def body_layout():
            return html.Div(className='row', children=[
                    html.Div(className='col-md-3',id='control-panel', children=cp.Control_Pannel()),
                    html.Div(className='col-md-9',id='graphs',style={'height': 'calc(100vh - 160px)'}, children=[]),
                    html.Div(className='col-md-3',id='test-stuff',children=[html.Div([
                        html.P('More stuff ....')
                    ])])
                ])

        def get_layout():
            return html.Div([
                    drc.Upload_Box(),
                    body_layout()
            ])

        """
        layout should be as a function so when page referesh a new layout is generated
        otherwise dash app will pull from a in memory cache.
        """
        self.app.layout = get_layout



        """
        Wrapper functions for our call backs. We wrape the functions to try separate out the code
        to help for editing when we have a team working on it.
        """


        #generates our main control pannel after file is uploaded
        @self.app.callback(Output('control-panel', 'children'),
                      [Input('upload', 'contents')])
        def upload_dataset(contents):

            if contents is not None:
                content_type, content_string = contents.split(',')

                #uploads data frame and saves into session storage
                if 'spreadsheet' in content_type:
                    session_id = session['ss_id']
                    #saves data to store
                    df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)))
                    ddm.save_df(session_id,df,'data_explorer',self.DATASTORE_PATH)
                    #reloads data from store to check its correct
                    (df, features, dte_filter) = ddm.get_dataframe(session_id,'data_explorer',self.DATASTORE_PATH)

                return cp.Control_Pannel(df, features, dte_filter)



        @self.app.callback(Output('graphs', 'children'),
                      [Input('dropdown-y', 'value'),
                       Input('dropdown-x', 'value'),
                       Input('x-range-slider', 'value'),
                       Input('y-range-slider', 'value'),
                       Input('dropdown-date', 'value')
                      ])
        def update_graph(y_feature,x_feature,x_range,y_range,dte_year):
            return grp.Regression_Chart('graph-regression-display',
                                        x_feature,
                                        y_feature,
                                        x_range,
                                        y_range,
                                        dte_year,
                                        self.DATASTORE_PATH)

        #######################
        ### X FILTER
        ######################
        @self.app.callback(Output('x-range-slider', 'min'),
                      [Input('dropdown-x', 'value'),
                      Input('dropdown-date', 'value')
                      ])
        def update_x_range_min(feature,dte_year):
            return cp.Update_Range(feature,dte_year,low=True,DATASTORE_PATH=self.DATASTORE_PATH)


        @self.app.callback(Output('x-range-slider', 'max'),
                      [Input('dropdown-x', 'value'),
                      Input('dropdown-date', 'value')])
        def update_x_range_max(feature,dte_year):
            return cp.Update_Range(feature,dte_year,low=False,DATASTORE_PATH=self.DATASTORE_PATH)


        @self.app.callback(Output('x-range-slider', 'marks'),
                      [Input('dropdown-x', 'value'),
                      Input('dropdown-date', 'value')])
        def update_x_range_markers(feature,dte_year):
            return  cp.Get_Markers(feature,dte_year,self.DATASTORE_PATH)


        @self.app.callback(Output('x-range-slider', 'value'),
                      [Input('dropdown-x', 'value'),
                      Input('dropdown-date', 'value')])
        def update_x_range_value(feature,dte_year):
            return cp.Get_Min_Max(feature,dte_year,self.DATASTORE_PATH)


        #######################
        ### Y FILTER
        ######################
        @self.app.callback(Output('y-range-slider', 'min'),
                      [Input('dropdown-y', 'value'),
                      Input('dropdown-date', 'value')])
        def update_y_range_min(feature,dte_year):
            return cp.Update_Range(feature,dte_year,low=True,DATASTORE_PATH=self.DATASTORE_PATH)


        @self.app.callback(Output('y-range-slider', 'max'),
                      [Input('dropdown-y', 'value'),
                      Input('dropdown-date', 'value')])
        def update_y_range_max(feature,dte_year):
            return cp.Update_Range(feature,dte_year,low=False,DATASTORE_PATH=self.DATASTORE_PATH)


        @self.app.callback(Output('y-range-slider', 'marks'),
                      [Input('dropdown-y', 'value'),
                      Input('dropdown-date', 'value')])
        def update_y_range_markers(feature,dte_year):
            return  cp.Get_Markers(feature,dte_year,self.DATASTORE_PATH)



        @self.app.callback(Output('y-range-slider', 'value'),
                      [Input('dropdown-y', 'value'),
                      Input('dropdown-date', 'value')])
        def update_y_range_value(feature,dte_year):
            return cp.Get_Min_Max(feature,dte_year,self.DATASTORE_PATH)


    def getApp(self):
        return self.app
