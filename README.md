# Kontent Konstellations

This is a sample app that uses the [Kentico Kontent Python SDK](#https://github.com/kentico-michaelb/kontent-delivery-python-sdk) to retrieve content from Kentico Kontent.  Plotly and [Dash](https://plotly.com/python/network-graphs/#network-graphs-in-dash) are used to generate a network graph of linked items in a Kontent project.

>Note: Konstellations uses [Kentico Kontent's "items" endpoint](https://docs.kontent.ai/reference/delivery-api#operation/list-content-items), meaning it is limited to a 2000 item response. To change what items are returned, please see the [Filtering](#filtering) section of this README.

If you find a bug in the sample or have a feature request, please submit a GitHub issue.

## Table of Contents
- [Getting started](#Getting-started)
  - [Connecting to your Sample Project](#Connecting-to-your-Sample-Project)
- [Features](#Features)
- [Filtering](#Filtering)

## Getting started
We recommend running this sample application using virtual environment tooling such as [virtualenv](https://virtualenv.pypa.io/en/latest/).

To run the application:

1. Clone the app repository with your favorite GIT client
2. Add your Kontent Project ID key to config.py in the project root - detailed instructions available below
3. Install the project dependencies: pip install -r requirements.txt
4. Run the application: ```report.py```


### Connecting to your Sample Project
If you already have a [Kentico Kontent account](https://app.kontent.ai), you can connect this application to your version of the Sample project.

1. In Kentico Kontent, choose Project settings from the app menu
1. Under Development, choose API keys and copy the Project ID
1. Open the `config.py` file
1. Use the values from your Kentico Kontent project as the `project_id` value
1. Save the changes

## Features
* Nodes can be moved by clicking and dragging.
* Hovering over an arrow (edge) between two nodes shows how they are related in the left-hand margin.
* Zooming in/out can be done with your mousewheel when your cursor is positioned over the graph.
* Clicking the "Reset" button will reset the zoom.

## Filtering
To leverage the [Kontent Python SDK's Filtering](https://github.com/kentico-michaelb/kontent-delivery-python-sdk#Filtering-content):
1. Open `network_builder.py`
2. Import the Kontent SDK's Filter 
3. Replace ```response = client.get_content_items()``` with your filtered query.

Example: 
```python
from kontent_delivery.builders.filter_builder import Filter

# returns all items of the "article" content type
response = client.get_content_items(
    Filter("system.type", "[eq]", "article")
)
```
4. Run the application with: ```report.py```