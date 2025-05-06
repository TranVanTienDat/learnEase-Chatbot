from lib.external_api import ExternalApi
from flask import Blueprint
from controllers.chat.chat import Chat

bp = Blueprint("chat", __name__, url_prefix="/api")
api = ExternalApi(bp)

api.add_resource(Chat, "/v1/chat")






