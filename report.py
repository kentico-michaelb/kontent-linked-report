import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_cytoscape as cyto
from dash_html_components.H1 import H1
import config
from kontent_delivery.client import DeliveryClient

client = DeliveryClient(config.project_id, options=config.delivery_options)

# get items
response = client.get_content_items()
items = response.items

# get used content types
response = client.get_content_types()

content_types = {}

for content_type in response.types:
    linked_elements = []
    for element, value in vars(content_type.elements).items():
        # find linked elements on content type for iteration
        if value.type == "modular_content":
            linked_elements.append(element)

    content_types[content_type.codename] = linked_elements

# create nodes
nodes = []

for item in items:
    node = {"data":{"id": item.codename, "label": item.name }}
    nodes.append(node)

    # loop thru linked elements in content type
    if item.content_type in content_types:
        for linked_element in content_types[item.content_type]:
            related = item.get_linked_items(linked_element)
            if related != None:
                for linked_item in related:
                    related_node = {"data":{"id": linked_item.codename, "label": linked_item.name }}
                    nodes.append(related_node)
                    link = {"data": {"source": item.codename, "target": linked_item.codename, "element": linked_element}}
                    nodes.append(link)


app = dash.Dash(__name__)

app.layout = html.Div([
    html.Img(id="logo", 
             alt="Kontent", 
             src="static\\images\\01-kk-logo-main.svg",
             height="148px", width="257px"
    ),
    html.H1("Linked Items Network Graph"),
    html.P("Hover over edges to view relationships:"),
    html.Span(id='cytoscape-mouseoverEdgeData-output'),
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
               "background-color": "#E9E8E8",
               "font-face":"Arial"},
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
                # The default curve style does not work with certain arrows
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

])

@app.callback(Output('cytoscape-mouseoverEdgeData-output', 'children'),
                Input('linked_items_report', 'mouseoverEdgeData'))
def displayTapEdgeData(data):
    if data:
        return f"The \"{data['element']}\" element links \"{data['source']}\" to \"{data['target']}\""

app.run_server(debug=True)