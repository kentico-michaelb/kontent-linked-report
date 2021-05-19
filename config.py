import os

project_id = os.environ.get('KONTENT_API_KEY', None)
delivery_options = {   
    "preview": False,
    "preview_api_key": "enter_key_here",
    "secured": False,
    "secured_api_key": "enter_key_here",
    "timeout": (4,7)
    }