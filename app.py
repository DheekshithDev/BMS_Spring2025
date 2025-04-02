# IMPORTS
import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html, Input, Output, Dash, no_update
import dash_daq as daq
import plotly.express as px
import pandas as pd
import numpy as np


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

SIDEBAR = html.Div([
    # html.H2("Sidebar", className="display-4"),
    # html.Hr(),
    dbc.Card([
        dbc.CardHeader([
            dcc.Tabs(id="molecule-tabs", value='tab-molecule-1',
                     children=[dcc.Tab(id='mol1', label='Mol1', value='tab-molecule-1'),
                               dcc.Tab(id='mol2', label='Mol2', value='tab-molecule-2'),
                               dcc.Tab(id='mol3', label='Mol3', value='tab-molecule-3'),
                               dcc.Tab(id='mol4', label='Mol4', value='tab-molecule-4'),]),
            dbc.Tooltip("Molecule 1", target='mol1', placement='bottom'),
            dbc.Tooltip("Molecule 2", target='mol2', placement='bottom'),
            dbc.Tooltip("Molecule 3", target='mol3', placement='bottom'),
            dbc.Tooltip("Molecule 4", target='mol4', placement='bottom'),
        ]),
        dbc.CardBody([
            html.Div([
                dbc.Label("Correlation", html_for='correlation-slider',
                          style={'margin-left': '1rem', 'width': '100%', 'textAlign': 'center'}),
                # daq.NumericInput(id='correlation-input', value=0, min=-1, max=1, style={'margin-bottom': '1rem'}),
                # dbc.FormText("Enter specific value for correlation: ", color="secondary"),
                dbc.Input(type="number", id="correlation-input", min=-1, max=1, step=0.01, placeholder="Enter correlation value",
                          style={'margin-left': '1rem', 'margin-bottom': '1rem', 'width': '10rem'}),
                dcc.Slider(
                    id='correlation-slider',
                    min=-1,
                    max=1,
                    step=0.1,
                    value=0,
                    tooltip={"placement": "bottom", "always_visible": False},
                    marks={-1:'-1', -0.5:'-0.5', 0:'0', 0.5:'0.5', 1:'1'},
                    className="slider-style"
                ),
                dbc.Tooltip(
                    "Adjust the correlation slider",
                    target="correlation-slider",
                    placement="bottom"
                )
            ], className="sidebar-div"),
            html.Div([
                dbc.Label("K1", html_for='k1-slider',
                          style={'margin-left': '1rem', 'width': '100%', 'textAlign': 'center'}),
                dbc.Input(type="number", id="k1-input", min=0, max=1758, step=50, placeholder="Enter K1 samples",
                          style={'margin-left': '1rem', 'margin-bottom': '1rem', 'width': '10rem'}),
                dcc.Slider(
                    id='k1-slider',
                    min=0,
                    max=1758,
                    step=50,
                    value=100,
                    tooltip={"placement": "bottom", "always_visible": False},
                    marks={(r := round(1758*x)): str(r) for x in np.arange(0, 1.25, 0.25)},
                    className="slider-style"
                ),
                dbc.Tooltip(
                    "Adjust the K1 slider",
                    target="k1-slider",
                    placement="bottom"
                )
            ], className="sidebar-div"),
            html.Div([
                dbc.Label("K2", html_for='k2-slider',
                          style={'margin-left': '1rem', 'width': '100%', 'textAlign': 'center'}),
                dbc.Input(type="number", id="k2-input", min=0, max=1758, step=50, placeholder="Enter K2 samples",
                          style={'margin-left': '1rem', 'margin-bottom': '1rem', 'width': '10rem'}),
                dcc.Slider(
                    id='k2-slider',
                    min=0,
                    max=1758,
                    step=50,
                    value=100,
                    tooltip={"placement": "bottom", "always_visible": False},
                    marks={(r := round(1758*x)): str(r) for x in np.arange(0, 1.25, 0.25)},
                    className="slider-style"
                ),
                dbc.Tooltip(
                    "Adjust the K2 slider",
                    target="k2-slider",
                    placement="bottom"
                )
            ], className="sidebar-div"),
            html.Div([
                dbc.Label("Top X%", html_for='topX-slider',
                          style={'margin-left': '1rem', 'width': '100%', 'textAlign': 'center'}),
                dbc.Input(type="number", id="topX-input", min=0, max=1758, step=50, placeholder="Enter Top X% ",
                          style={'margin-left': '1rem', 'margin-bottom': '1rem', 'width': '10rem'}),
                dcc.Slider(
                    id='topX-slider',
                    min=0,
                    max=100,
                    step=5,
                    value=10,
                    tooltip={"placement": "bottom", "always_visible": False},
                    marks={x: str(x) for x in range(0, 101, 25)},
                    className="slider-style"
                ),
                dbc.Tooltip(
                    "Adjust the Top X% slider",
                    target="topX-slider",
                    placement="bottom"
                )
            ], className="sidebar-div"),
            html.Div([
                dbc.Label("Simulations", html_for='simul-slider',
                          style={'margin-left': '1rem', 'width': '100%', 'textAlign': 'center'}),
                dbc.Input(type="number", id="simul-input", min=1, max=1000, step=100, placeholder="Enter Simulations ",
                          style={'margin-left': '1rem', 'margin-bottom': '1rem', 'width': '10rem'}),
                dcc.Slider(
                    id='simul-slider',
                    min=1,
                    max=1000,
                    step=100,
                    value=100,
                    tooltip={"placement": "bottom", "always_visible": False},
                    marks={(r := int(x)): str(r) for x in np.linspace(1, 1000, 5)},
                    className="slider-style"
                ),
                dbc.Tooltip(
                    "Adjust the simulations slider",
                    target="simul-slider",
                    placement="bottom"
                )
            ], className="sidebar-div"),
        ])
    ], className=""),
], className="sidebar-style")

MAIN_CONTENT = html.Div([
    # html.H4("Main Content", className="display-4"),
    dcc.Tabs(id="graphs-tabs", value="tab-graph-1",
             children=[dcc.Tab(label='Correlation', value='tab-graph-1', children=[dcc.Graph(id='graph-1')], className="graph-tabs"),
                       dcc.Tab(label='K1', value='tab-graph-2', children=[dcc.Graph(id='graph-2')], className="graph-tabs"),
                       dcc.Tab(label='K2', value='tab-graph-3', children=[dcc.Graph(id='graph-3')], className="graph-tabs"),
                       dcc.Tab(label='Top X%', value='tab-graph-4', children=[dcc.Graph(id='graph-4')], className="graph-tabs"),
                       dcc.Tab(label='Simulations', value='tab-graph-5', children=[dcc.Graph(id='graph-5')], className="graph-tabs")],
             className="graph-tabs-container")
], className="content-style")


app.layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(SIDEBAR, width=4, style={"height": "100vh",  "overflowY": "auto"}, className="hide-scrollbar"),
            dbc.Col(MAIN_CONTENT, width=8, style={"height": "100vh"}),
        ],
        style={"height": "100vh"}
    ),
    fluid=True,
    style={"height": "100vh"}
)

#### CALLBACKS-START ####

# Callback for main content graph tab rendering
@app.callback(
    Output("graph-1", "figure"),
    Input("graphs-tabs", "value")
)
def graphs_tabs_render(value):
    if value == 'tab-graph-1':
        return None
    elif value == 'tab-graph-2':
        return None
    elif value == 'tab-graph-3':
        return None
    elif value == 'tab-graph-4':
        return None
    elif value == 'tab-graph-5':
        return None
    return html.Div("No content available.")

# Callback for sidebar adjustments for graphs
@app.callback(
    [Output("graph-1", "figure"),
     Output("graph-2", "figure"),
     Output("graph-3", "figure"),
     Output("graph-4", "figure"),
     Output("graph-5", "figure")],

    [Input("graphs-tabs", "value"),
     Input("correlation-slider", "value")],
)
def correlation_slider_graph_render(graph_tabs, corr_slider):
    if graph_tabs == 'tab-graph-1':
        # Render something with correlation slider value
        return None, no_update, no_update, no_update, no_update
    elif graph_tabs == 'tab-graph-2':
        return no_update, None, no_update, no_update, no_update
    elif graph_tabs == 'tab-graph-3':
        return no_update, no_update, None, no_update, no_update
    elif graph_tabs == 'tab-graph-4':
        return no_update, no_update, no_update, None, no_update
    elif graph_tabs == 'tab-graph-5':
        return no_update, no_update, no_update, no_update, None

#### CALLBACKS-END ####


if __name__ == '__main__':
    app.run(debug=True)
