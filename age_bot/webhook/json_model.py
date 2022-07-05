# built-in
# 3rd party
from json_model import fields
from json_model import libs
# local

class WebhookLogger(libs.JsonModel):
    """
    This class is a json model
    """
    content = fields.String(required=False)
    embeds = fields.List(required=False)
    username = fields.String(required=True)
    avatar_url = fields.String(required=True)
    components = fields.List(required=False)
