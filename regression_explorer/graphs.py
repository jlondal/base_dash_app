"""
Generates a scatter plot wiht a best fit line
"""

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from . import utils as utls
from . import data_management as ddm

from flask import session

import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression


def Regression_Chart(id, x_feature, y_feature,x_range,y_range, dte_year,DATASTORE_PATH):
            #prevents an empty data selection
            if dte_year is None:
                dte_year = ['All']

            #gets data for active session
            session_id = session['ss_id']
            (df, features, dte_filter) = ddm.get_dataframe(session_id,'data_explorer',DATASTORE_PATH)

            #filter data
            if 'All' not in dte_year:
                df = df[df[dte_filter].dt.year.isin(dte_year) ]

            df = df[df[x_feature] >= x_range[0]]
            df = df[df[x_feature] <= x_range[1]]

            df = df[df[y_feature] >= y_range[0]]
            df = df[df[y_feature] <= y_range[1]]

            #fits model, with trend lines
            X = df[x_feature].values.reshape(-1, 1)
            y = df[y_feature].values

            model = LinearRegression(normalize=True)
            model.fit(X,y)
            y_pred = model.predict(X)

            model_score = round(r2_score(y,y_pred),2)

            X_range_line = np.linspace(X.min() - 0.5, X.max() + 0.5, 300).reshape(-1, 1)
            y_range_line = model.predict(X_range_line)

            return _scatter_chart(id,
                                  df,
                                  (x_feature,y_feature,dte_filter),
                                  X_range_line.squeeze(),
                                  y_range_line,
                                  model_score,
                                  model)


def _scatter_chart(id,df, selectors ,X_trend,y_trend,model_score,model):

    (x_feature, y_feature, dte_filter) = selectors

    trace0 = go.Scatter(
                    x=df[x_feature],
                    y=df[y_feature],
                    text=df[dte_filter],
                    name='Actual',
                    mode='markers',
                    marker=dict(
                        size=12,
                        color = df[dte_filter].dt.year,
                        colorscale='Viridis',
                        showscale=True,
                        colorbar = {
                                'tick0': 0,
                                'dtick': 1
                      }
                    ),
                    opacity=0.7
                )

    trace1 = go.Scatter(
                    x=X_trend,
                    y=y_trend ,
                    name='Trend',
                    mode='lines',
                    hovertext=utls._format_coefs(model,x_feature,y_feature)
                )

    df_chart = [trace0,trace1]

    layout = go.Layout(
        title="""%s vs. %s \n
        R^2 = %s
        """ % (y_feature,x_feature,model_score),

        hovermode='closest',
        showlegend=False,
        xaxis=dict(
            title=x_feature,
            titlefont=dict(
                family='Gotham Book, monospace',
                size=14,
                color='black'
            )
        ),
        yaxis=dict(
            title=y_feature,
            titlefont=dict(
                family='Gotham Book, monospace',
                size=14,
                color='black'
            )
        )
    )

    chart =  dcc.Graph(
                        id = id ,
                        figure=go.Figure(data=df_chart, layout=layout),
                        style={'margin-left': '20px', 'height': 'calc(100vh - 160px)'},
                        config={'modeBarButtonsToRemove': [
                            'pan2d',
                            'select2d',
                            'autoScale2d',
                            'hoverClosestCartesian',
                            'hoverCompareCartesian',
                            'toggleSpikelines'
                        ]}
                    )

    return [ chart ]
