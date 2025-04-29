
from lib.external_api import ExternalApi
from flask import Blueprint
from controllers.chatbot.chatbot import Chatbot

bp = Blueprint("chatbot", __name__, url_prefix="/api")
api = ExternalApi(bp)

api.add_resource(Chatbot, "/v1/chatbot")






