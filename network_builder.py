import config
from kontent_delivery.client import DeliveryClient

def create_network(api_key = config.project_id):
    # KONTENT PYTHON SDK
    # initialize Kontent delivery client
    client = DeliveryClient(api_key, options=config.delivery_options)

    response = client.get_content_items()
    items = response.items

    response = client.get_content_types()

    # content types with linked items
    content_types = {}

    # find linked elements on content type
    for content_type in response.types:
        linked_elements = []
        for element, value in vars(content_type.elements).items():
            if value.type == "modular_content":
                linked_elements.append(element)

        content_types[content_type.codename] = linked_elements

    # create nodes from Kontent items
    nodes = []

    for item in items:
        # create node
        node = {"data":{"id": item.codename, "label": item.name }}
        nodes.append(node)

        # set relationships from node's linked items elements
        if item.content_type in content_types:
            for linked_element in content_types[item.content_type]:
                related = item.get_linked_items(linked_element)
                if related != None:
                    for linked_item in related:
                        related_node = {"data":{"id": linked_item.codename, "label": linked_item.name }}
                        nodes.append(related_node)
                        link = {"data": {"source": item.codename, "target": linked_item.codename, "element": linked_element}}
                        nodes.append(link)
    
    return nodes


