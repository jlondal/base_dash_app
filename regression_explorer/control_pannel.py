"""
Generates the control pannel
and functiosn used by callbacks to control pannel
"""
import dash_core_components as dcc
import dash_html_components as html

from . import components as drc
from . import utils as utls
from . import data_management as ddm

import numpy as np

from flask import session


#############
# Layouts
############

def Control_Pannel(df=None,features=None,dte_filter=None):
    #if no data is provide an empty control pannel is returned
    if df is None:
        return _cp_wth_no_data()
    return _cp_wth_data(df,features,dte_filter)


def _cp_wth_no_data():
    return [drc.NamedDropdown(
                name='Y',
                id='dropdown-y',
                options=[],
                clearable=False,
                searchable=True
        ),
        dcc.RangeSlider(
            id='y-range-slider',
            min=0,
            max=0,
            step=1,
            value=[0, 0]
            ,allowCross=False
            #,vertical=True
        ),
        html.Br(),
        drc.NamedDropdown(
                name='X',
                id='dropdown-x',
                options=[],
                clearable=False,
                searchable=True
            ),
        dcc.RangeSlider(
            id='x-range-slider',
            min=0,
            max=0,
            step=1,
            value=[0, 0]
            ,allowCross=False
            #,vertical=True
        ),
        html.Br(),
        drc.NamedDropdown(
                name='Date Filter',
                id='dropdown-date',
                options=[],
                clearable=False,
                searchable=True
            )
        ]

def _cp_wth_data(df,features,dte_filter):



    y_series = df[features[0]]
    x_series = df[features[1]]
    (min_y,max_y,ymarkers) = utls._range_cal(y_series)
    (min_x,max_x,xmarkers) = utls._range_cal(x_series)


    return [drc.NamedDropdown(
                name='Select Y',
                id='dropdown-y',
                options=[{'label': i, 'value': i} for i in features],
                value=features[0],
                clearable=False,
                searchable=True
            ),
            html.Br(),
            dcc.RangeSlider(
                id='y-range-slider',
                min=min_y,
                max=max_y,
                step=1,
                value=[min_y, max_y]
                ,allowCross=False
                ,marks=ymarkers
                #,vertical=True
            ),
            html.Br(),html.Br(),
            drc.NamedDropdown(
                    name='Select X',
                    id='dropdown-x',
                    options=[{'label': i, 'value': i} for i in features],
                    value=features[1],
                    clearable=False,
                    searchable=True
                ),
            html.Br(),
            dcc.RangeSlider(
                id='x-range-slider',
                min=min_x,
                max=max_y,
                step=1,
                value=[min_x, max_x]
                ,allowCross=False
                ,marks=xmarkers
                #,vertical=True
            ),
            html.Br(),html.Br(),
            drc.NamedDropdown(
                    name='Select Year',
                    id='dropdown-date',
                    options=[{'label': i, 'value': i} for i in ['All'] + list(np.unique(df[dte_filter].dt.year))],
                    value='All',
                    clearable=False,
                    searchable=True,
                    multi=True
                )
        ]


#############
# Callbacks
############

def Update_Range(feature,dte_year,low=True,DATASTORE_PATH=''):
    #prevents an empty data selection
    if feature is None:
        return []

    if dte_year is None:
        dte_year = ['All']

    #gets data for active session
    session_id = session['ss_id']
    df = _get_df(session_id,dte_year,DATASTORE_PATH)

    if low == True:
        mn = min(df[feature])
    else:
        mn = max(df[feature])

    return  mn


#filters df by date
def _get_df(session_id,dte_year,DATASTORE_PATH):
    (df, features, dte_filter) = ddm.get_dataframe(session_id,'data_explorer',DATASTORE_PATH)

    if 'All' not in dte_year:
        df = df[df[dte_filter].dt.year.isin(dte_year) ]

    return df


def Get_Markers(feature,dte_year,DATASTORE_PATH):
    ranges = Get_Min_Max(feature,dte_year,DATASTORE_PATH)
    mn = ranges[0]
    mx = ranges[1]

    range_step = (mx- mn)//4

    markers = {
        mn: mn,
        mn+range_step: mn+range_step,
        mn+(range_step*2): mn+(range_step*2),
        mn+(range_step*3): mn+(range_step*3),
        mx: mx
    }

    return  markers

def Get_Min_Max(feature,dte_year,DATASTORE_PATH):
    #prevents an empty data selection
    if feature is None:
        return []

    if dte_year is None:
        dte_year = ['All']

    #gets data for active session
    session_id = session['ss_id']
    df = _get_df(session_id,dte_year,DATASTORE_PATH)

    mn = min(df[feature])
    mx = max(df[feature])

    return [mn, mx]
