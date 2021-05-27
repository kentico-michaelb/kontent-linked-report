import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_cytoscape as cyto
from network_builder import create_network
import config

nodes = create_network()

app = dash.Dash(__name__)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Konstellation.</title>
        {%favicon%}
        {%css%}
    </head>
    <body style="background-color: #918F8F">
        <div style="background-color:black;">
        <img id="logo"
                alt="Kontent"
                src="static\\images\\02-kk-logo-col-blk.svg"
                height="148px" width="257px"
                "/>
        </div>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

styles = {
    "container": {
        "position": "fixed",
        "display": "flex",
        "flexDirection": "column",
        "flexWrap": "wrap",
        "alignContent": "flex-start",
        "height": "100%",
        "width": "100%"
    },
    "cy-container": {
        "position": "relative",
        "backgroundColor":"#E9E8E8",
        "width": "74%",
        "height": "100%",
        "margin": "auto"
    },
    "cytoscape": {
        "position": "absolute",
        "width": "100%",
        "height": "100%",
        "zIndex": 999
    },
    "info": {
        "width": "25%",
        "height": "40%",
        "position": "relative",
        "backgroundColor": "#D3D2D2",
        "padding": "10px"
    },
    "btn-reset": {
        "marginBottom":"20px"
    }
}

app.layout = html.Div(style=styles["container"], children=[
    html.Div(style=styles["info"], children=[
        html.H1("Konstellation for project:"),
        html.H2(id="project-id", children=config.project_id),
        dcc.Input(id="project-id-input",
            type="text",
            debounce=True),
        html.Button("Build Graph", id="btn-reset", style=styles["btn-reset"]),
        html.P("Hover over links to view linked item relationships:"),
        html.Div(id="cytoscape-mouseoverEdgeData-output"),
        html.Div(id="output")
    ]),
    html.Div(className="cy-container", style=styles["cy-container"], children=[
        cyto.Cytoscape(
            id="linked_items_report",
            elements=nodes,
            style=styles["cytoscape"],
            zoomingEnabled=True,
            zoom=2,
            layout={
                "name": "cose",
                "idealEdgeLength": 100,
                "nodeOverlap": 20,
                "refresh": 20,
                "padding": 40,
                "randomize": False,
                "fit": True,
                "componentSpacing": 125,
                "nodeRepulsion": 400000,
                "edgeElasticity": 100,
                "nestingFactor": 5
            },
            responsive=True,
            stylesheet=[
            {
                "selector": "node",
                "style": {
                    "label": "data(id)",
                    "font-weight": 700,
                    "background-color": "#F05A22"
                }
            },
            {
                "selector": "edge",
                "style": {
                    "curve-style": "bezier"
                }
            },
            {
                "selector": "source",
                "style": {
                    "source-arrow-color": "#B72929",
                    "source-arrow-shape": "triangle",
                    "line-color": "#B72929"
                }
            }
        ]
        ),
    ]),
])


@app.callback(Output("cytoscape-mouseoverEdgeData-output", "children"),
                Input("linked_items_report", "mouseoverEdgeData"))
def displayTapEdgeData(data):
    if data:
        return f"\"{data['target']}\" linked to \"{data['source']}\" by the \"{data['element']}\" element."


@app.callback(
    [Output("linked_items_report", "zoom"),
    Output("linked_items_report", "elements"),
    Output("project-id", "children")],
    [Input("btn-reset", "n_clicks")],
    state=[State('project-id-input', 'value')]
)
def reset_layout(n_clicks, value):
    if value:
        nodes = create_network(value)
        project_id = value
    else:
        project_id = config.project_id
        nodes = create_network()
    return [1, nodes, project_id]

app.run_server(debug=True)