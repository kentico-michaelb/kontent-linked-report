import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_cytoscape as cyto
from network_builder import create_network

nodes = create_network()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Img(id="logo", 
                alt="Kontent", 
                src="static\\images\\01-kk-logo-main.svg",
                height="148px", width="257px"
        ),
        html.H1("Linked Items Network Graph"),
        html.P("Hover over edges to view relationships:"),
        html.Span(id='cytoscape-mouseoverEdgeData-output'),
    ],
    style={
        "display": "inline-block",
        "fontFamily": "Arial",
        "width": "500px",
        "verticalAlign": "top",
        "backgroundColor":" #FFFFFF"}
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
            style={"width": "1000px", 
                "height": "1000px",
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