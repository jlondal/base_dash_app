"""
A collection of functions to extended core components that can be reused
across apps.


Adding the follow new components

* Extended core Silder to include a label
* Extended core Dropdown to include a label
* A formated Upload box
"""

import dash_core_components as dcc
import dash_html_components as html


def _merge(a, b):
    return dict(a, **b)


def _omit(omitted_keys, d):
    return {k: v for k, v in d.items() if k not in omitted_keys}


def NamedSlider(name='', **kwargs):
    return html.Div(
        style={'padding': '10px 10px 15px 4px'},
        children=[
            html.P(f'{name}:'),
            html.Div(dcc.Slider(**kwargs), style={'margin-left': '6px'})
        ]
    )


def NamedDropdown(name='', **kwargs):
    return html.Div([
        html.P(f'{name}:', style={'margin-left': '3px'}),
        dcc.Dropdown(**kwargs)
    ])


"""
Requires Bootstrap for styling
"""
def Upload_Box(id='upload',
               style={
    'width': '100%',
    'height': '60px',
    'lineHeight': '60px',
    'borderWidth': '1px',
    'borderStyle': 'dashed',
    'borderRadius': '5px',
    'textAlign': 'center',
    'margin': '10px'
}):
    return html.Div(className='row', children=[
        html.Div(className='col-md-12', children=[
                dcc.Upload(
                    id='upload',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select a File'),
                        ' to change data'
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    }
                )
        ])
    ])
