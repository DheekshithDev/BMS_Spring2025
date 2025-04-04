# IMPORTS
import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html, Input, Output, Dash, no_update
import dash_daq as daq
import plotly.express as px
import pandas as pd
import numpy as np


mol1_df = pd.read_csv("assets/simulation_results_M1.csv")
mol2_df = pd.read_csv("assets/simulation_results_M2.csv")
mol3_df = pd.read_csv("assets/simulation_results_M3.csv")
mol4_df = pd.read_csv("assets/simulation_results_M4.csv")


def plotter(df, **kwargs):
    if kwargs['corr'] is None:  # K1, K2, topX, simul
        df_subset = df[
            (df["k1"] == kwargs['k1']) &
            (df["k2"] == kwargs['k2']) &
            (df["top_X_percent"] == kwargs['topX'])
            # & (df["simulations"] == kwargs['simul'])  ## Not yet ready
            ]
        fig = px.line(df_subset, x='correlation', y='probability', markers=True, color_discrete_sequence=['magenta'], height=800)
        fig.update_yaxes(tickformat=".4f")
        fig.update_traces(cliponaxis=False)
        return fig
    elif kwargs['k1'] is None:  # Corr, K2, topX, simul
        df_subset = df[
            (df["correlation"] == kwargs['corr']) &
            (df["k2"] == kwargs['k2']) &
            (df["top_X_percent"] == kwargs['topX'])
            # & (df["simulations"] == kwargs['simul'])  ## Not yet ready
            ]
        fig = px.line(df_subset, x='k1', y='probability', markers=True, color_discrete_sequence=['magenta'], height=800)
        fig.update_yaxes(tickformat=".4f")
        fig.update_traces(cliponaxis=False)
        return fig
    elif kwargs['k2'] is None:  # Corr, K1, topX, simul
        df_subset = df[
            (df["correlation"] == kwargs['corr']) &
            (df["k1"] == kwargs['k1']) &
            (df["top_X_percent"] == kwargs['topX'])
            # & (df["simulations"] == kwargs['simul'])  ## Not yet ready
            ]
        fig = px.line(df_subset, x='k2', y='probability', markers=True, color_discrete_sequence=['magenta'], height=800)
        fig.update_yaxes(tickformat=".4f")
        fig.update_traces(cliponaxis=False)
        return fig
    elif kwargs['topX'] is None:  # Corr, K1, K2, simul
        df_subset = df[
            (df["correlation"] == kwargs['corr']) &
            (df["k1"] == kwargs['k1']) &
            (df["k2"] == kwargs['k2'])
            # & (df["simulations"] == kwargs['simul'])  ## Not yet ready
            ]
        fig = px.line(df_subset, x='top_X_percent', y='probability', markers=True, color_discrete_sequence=['magenta'], height=800)
        fig.update_yaxes(tickformat=".4f")
        fig.update_traces(cliponaxis=False)
        return fig
    elif kwargs['simul'] is None:  # Corr, K1, K2, topX
        pass
    else:
        print("Something went wrong in plotter function!")
        return None


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

SIDEBAR = html.Div([
    # html.H2("Sidebar", className="display-4"),
    # html.Hr(),
    dbc.Card([
        dbc.CardHeader([
            dbc.Tabs(id="molecule-tabs", active_tab='tab-molecule-1',
                     children=[dbc.Tab(id='mol1', label='Molecule 1', tab_id='tab-molecule-1'),
                               dbc.Tab(id='mol2', label='Molecule 2', tab_id='tab-molecule-2'),
                               dbc.Tab(id='mol3', label='Molecule 3', tab_id='tab-molecule-3'),
                               dbc.Tab(id='mol4', label='Molecule 4', tab_id='tab-molecule-4'),], class_name="molecule-tabs"),
            dbc.Tooltip("Molecule 1", target='mol1', placement='bottom'),
            dbc.Tooltip("Molecule 2", target='mol2', placement='bottom'),
            dbc.Tooltip("Molecule 3", target='mol3', placement='bottom'),
            dbc.Tooltip("Molecule 4", target='mol4', placement='bottom'),
        ], className="sidebar-card-header"),
        dbc.CardBody([
            html.Div([
                dbc.Label("Correlation", html_for='correlation-slider',
                          style={'margin-left': '1rem', 'width': '100%', 'textAlign': 'left', 'fontWeight': 'bold'}),
                # daq.NumericInput(id='correlation-input', value=0, min=-1, max=1, style={'margin-bottom': '1rem'}),
                # dbc.FormText("Enter specific value for correlation: ", color="secondary"),
                dbc.Input(type="number", id="correlation-input", min=-1, max=1, step=0.1, placeholder="Enter correlation value",
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
            ], id="corr-div", className="sidebar-div"),
            html.Div([
                dbc.Label("K1", html_for='k1-slider',
                          style={'margin-left': '1rem', 'width': '100%', 'textAlign': 'left', 'fontWeight': 'bold'}),
                dbc.Input(type="number", id="k1-input", min=50, max=1750, step=50, placeholder="Enter K1 samples",
                          style={'margin-left': '1rem', 'margin-bottom': '1rem', 'width': '10rem'}),
                dcc.Slider(
                    id='k1-slider',
                    min=50,
                    max=1750,
                    step=50,
                    value=100,
                    tooltip={"placement": "bottom", "always_visible": False},
                    marks={(r := round(1750*x)): str(r) for x in np.arange(0, 1.25, 0.25)},
                    className="slider-style"
                ),
                dbc.Tooltip(
                    "Adjust the K1 slider",
                    target="k1-slider",
                    placement="bottom"
                )
            ], id="k1-div", className="sidebar-div"),
            html.Div([
                dbc.Label("K2", html_for='k2-slider',
                          style={'margin-left': '1rem', 'width': '100%', 'textAlign': 'left', 'fontWeight': 'bold'}),
                dbc.Input(type="number", id="k2-input", min=1, max=20, step=1, placeholder="Enter K2 samples",
                          style={'margin-left': '1rem', 'margin-bottom': '1rem', 'width': '10rem'}),
                dcc.Slider(
                    id='k2-slider',
                    min=1,
                    max=20,
                    step=1,
                    value=1,
                    tooltip={"placement": "bottom", "always_visible": False},
                    marks={(r := round(20*x)): str(r) for x in np.arange(0, 1.25, 0.25)},
                    className="slider-style"
                ),
                dbc.Tooltip(
                    "Adjust the K2 slider",
                    target="k2-slider",
                    placement="bottom"
                )
            ], id="k2-div", className="sidebar-div"),
            html.Div([
                dbc.Label("Top X%", html_for='topX-slider',
                          style={'margin-left': '1rem', 'width': '100%', 'textAlign': 'left', 'fontWeight': 'bold'}),
                dbc.Input(type="number", id="topX-input", min=1, max=20, step=1, placeholder="Enter Top X% ",
                          style={'margin-left': '1rem', 'margin-bottom': '1rem', 'width': '10rem'}),
                dcc.Slider(
                    id='topX-slider',
                    min=1,
                    max=20,
                    step=1,
                    value=1,
                    tooltip={"placement": "bottom", "always_visible": False},
                    marks={x: str(x) for x in range(0, 21, 1)},
                    className="slider-style"
                ),
                dbc.Tooltip(
                    "Adjust the Top X% slider",
                    target="topX-slider",
                    placement="bottom"
                )
            ], id="topX-div", className="sidebar-div"),
            html.Div([
                dbc.Label("Simulations", html_for='simul-slider',
                          style={'margin-left': '1rem', 'width': '100%', 'textAlign': 'left', 'fontWeight': 'bold'}),
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
            ], id="simul-div", className="sidebar-div"),
        ])
    ], className="sidebar-card"),
], className="sidebar-style")

MAIN_CONTENT = html.Div([
    # html.H4("Main Content", className="display-4"),
    dbc.Tabs(id="graphs-tabs", active_tab="tab-graph-1",
             children=[dbc.Tab(label='Correlation', id='corr-tab', tab_id='tab-graph-1', children=[dcc.Graph(id='graph-1')], class_name="", tab_class_name="nav nav-pills"),
                       dbc.Tab(label='K1', id='k1-tab', tab_id='tab-graph-2', children=[dcc.Graph(id='graph-2')], class_name="", tab_class_name="nav nav-pills"),
                       dbc.Tab(label='K2', id='k2-tab', tab_id='tab-graph-3', children=[dcc.Graph(id='graph-3')], class_name="", tab_class_name="nav nav-pills"),
                       dbc.Tab(label='Top X%', id='topX-tab', tab_id='tab-graph-4', children=[dcc.Graph(id='graph-4')], class_name="", tab_class_name="nav nav-pills"),
                       dbc.Tab(label='Simulations', id='simul-tab', tab_id='tab-graph-5', children=[dcc.Graph(id='graph-5')], class_name="", tab_class_name="nav nav-pills")],
             className="graph-tabs-container"),
    dbc.Button([html.Img(src="/assets/copilot-icon.svg", style={"height": "10px", "marginRight": "4px"}), "Copilot"], color="primary", style={"margin-top": "2px", "width": "20%"})
], className="content-style")


app.layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(SIDEBAR, width=5, style={"height": "100vh",  "overflowY": "auto"}, className="hide-scrollbar"),
            dbc.Col(MAIN_CONTENT, width=7, style={"height": "100vh"}),
        ],
        style={"height": "100vh"}
    ),
    fluid=True,
    style={"height": "100vh"}
)

#### CALLBACKS-START ####

# Callback for main content graph tab rendering
@app.callback(
    [Output("corr-div", "className"),
     Output("k1-div", "className"),
     Output("k2-div", "className"),
     Output("topX-div", "className"),
     Output("simul-div", "className")],
    Input("graphs-tabs", "active_tab")
)
def graphs_tabs_render(active_tab):
    if active_tab == 'tab-graph-1':  # Correlation
        update_1 = "sidebar-div-disabled"  # Greyout
        update_2 = "sidebar-div"  # Color back
        return [update_1, update_2, update_2, update_2, update_2]
    elif active_tab == 'tab-graph-2':
        update_1 = "sidebar-div-disabled"  # Greyout
        update_2 = "sidebar-div"  # Color back
        return [update_2, update_1, update_2, update_2, update_2]
    elif active_tab == 'tab-graph-3':
        update_1 = "sidebar-div-disabled"  # Greyout
        update_2 = "sidebar-div"  # Color back
        return [update_2, update_2, update_1, update_2, update_2]
    elif active_tab == 'tab-graph-4':
        update_1 = "sidebar-div-disabled"  # Greyout
        update_2 = "sidebar-div"  # Color back
        return [update_2, update_2, update_2, update_1, update_2]
    elif active_tab == 'tab-graph-5':
        update_1 = "sidebar-div-disabled"  # Greyout
        update_2 = "sidebar-div"  # Color back
        return [update_2, update_2, update_2, update_2, update_1]
    return [html.Div("No content available.")]


# Callback for sidebar adjustments for graphs
@app.callback(
    [
     Output("graph-1", "figure"),
     Output("graph-2", "figure"),
     Output("graph-3", "figure"),
     Output("graph-4", "figure"),
     Output("graph-5", "figure"),

     # Output("correlation-input", "value"),
     # Output("k1-input", "value"),
     # Output("k2-input", "value"),
     # Output("topX-input", "value"),
     # Output("simul-input", "value"),
     #
     # Output("correlation-slider", "value"),
     # Output("k1-slider", "value"),
     # Output("k2-slider", "value"),
     # Output("topX-slider", "value"),
     # Output("simul-slider", "value")
     ],

    [
     Input("molecule-tabs", "active_tab"),
     Input("graphs-tabs", "active_tab"),

     Input("correlation-slider", "value"),
     Input("k1-slider", "value"),
     Input("k2-slider", "value"),
     Input("topX-slider", "value"),
     Input("simul-slider", "value"),

     # Input("correlation-input", "value"),
     # Input("k1-input", "value"),
     # Input("k2-input", "value"),
     # Input("topX-input", "value"),
     # Input("simul-input", "value"),
    ],
)
def correlation_slider_graph_render(mol_active_tab, grph_active_tab, corr_slr_val, k1_slr_val, k2_slr_val, topX_slr_val, simul_slr_val):
    df = {
        "tab-molecule-1": mol1_df,
        "tab-molecule-2": mol2_df,
        "tab-molecule-3": mol3_df,
        "tab-molecule-4": mol4_df,
    }.get(mol_active_tab)

    topX_slr_val = (topX_slr_val / 100)

    # Temporary Adjustment
    corr_slr_val = max(min(corr_slr_val, df['correlation'].max()), df['correlation'].min())
    k1_slr_val = max(min(k1_slr_val, df['k1'].max()), df['k1'].min())
    k2_slr_val = max(min(k2_slr_val, df['k2'].max()), df['k2'].min())
    topX_slr_val = max(min(topX_slr_val, df['top_X_percent'].max()), df['top_X_percent'].min())

    if grph_active_tab == 'tab-graph-1':  # Correlation Tab
        fig_update = plotter(df, corr=None, k1=k1_slr_val, k2=k2_slr_val, topX=topX_slr_val, simul=simul_slr_val)
        return [fig_update, no_update, no_update, no_update, no_update]

    elif grph_active_tab == 'tab-graph-2':  # K1 Tab
        fig_update = plotter(df, corr=corr_slr_val, k1=None, k2=k2_slr_val, topX=topX_slr_val, simul=simul_slr_val)
        return [no_update, fig_update, no_update, no_update, no_update]

    elif grph_active_tab == 'tab-graph-3':  # K2 Tab
        fig_update = plotter(df, corr=corr_slr_val, k1=k1_slr_val, k2=None, topX=topX_slr_val, simul=simul_slr_val)
        return [no_update, no_update, fig_update, no_update, no_update]

    elif grph_active_tab == 'tab-graph-4':  # topX Tab
        fig_update = plotter(df, corr=corr_slr_val, k1=k1_slr_val, k2=k2_slr_val, topX=None, simul=simul_slr_val)
        return [no_update, no_update, no_update, fig_update, no_update]

    elif grph_active_tab == 'tab-graph-5':  # Simulations Tab
        fig_update = plotter(df, corr=corr_slr_val, k1=k1_slr_val, k2=k2_slr_val, topX=topX_slr_val, simul=None)
        return [no_update, no_update, no_update, no_update, fig_update]

#### CALLBACKS-END ####


if __name__ == '__main__':
    app.run(debug=True)
