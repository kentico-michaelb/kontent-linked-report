import dash
from dash.dependencies import Input, Output
import dash_html_components as html
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
        html.H2(f"{config.project_id}"),
        html.P("Hover over links to view linked item relationships:"),
        html.Button("Reset Zoom", id="btn-reset", style=styles["btn-reset"]),
        html.Div(id="cytoscape-mouseoverEdgeData-output"),
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
     Output("linked_items_report", "elements")],
    [Input("btn-reset", "n_clicks")]
)
def reset_layout(n_clicks):
    return [1, nodes]

if __name__ == '__main__':
    app.run_server(debug=True)