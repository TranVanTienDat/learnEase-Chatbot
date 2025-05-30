from learn_ease_app import LearEaseApp


def init_app(app: LearEaseApp):
    # register blueprint routers

    from flask_cors import CORS 

    from controllers.chatbot import bp as chatbot_bp
    from controllers.chat import bp as chat_bp


    CORS(
        chatbot_bp,
        allow_headers=["Content-Type", "X-App-Code"],
        methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    )
    CORS(chat_bp, allow_headers=["Content-Type", "X-App-Code"], methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"])
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(chat_bp)

