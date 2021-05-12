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
        <div style="background-color:black">
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

app.layout = html.Div([
    html.Div([
        html.H1("Konstellation for project:"),
        html.H2(f"{config.project_id}"),
        html.P("Hover over links to view linked item relationships:"),
        html.Span(id='cytoscape-mouseoverEdgeData-output'),
    ],
    style={
        "display": "inline-block",
        "fontFamily": "Arial",
        "width": "30%",
        "height": "300px",
        "verticalAlign": "top",
        "backgroundColor":" #D3D2D2"}
    ),
    html.Div([
        cyto.Cytoscape(
            id="linked_items_report",
            elements=nodes,
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
            style={"width": "800px", 
                "height": "800px",
                "backgroundColor": "#E9E8E8",
                "margin":"auto"},
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
    ],
    style={
    "display": "inline-block",
    }),   
])

@app.callback(Output('cytoscape-mouseoverEdgeData-output', 'children'),
                Input('linked_items_report', 'mouseoverEdgeData'))
def displayTapEdgeData(data):
    if data:
        return f"\"{data['target']}\" linked to \"{data['source']}\" by the \"{data['element']}\" element."

app.run_server(debug=True)