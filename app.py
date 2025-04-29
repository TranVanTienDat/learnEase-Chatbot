import os
from learn_ease_app import LearEaseApp
from config.engine import test_connection
import extensions.ext_blueprints as ext_blueprints
from dotenv import load_dotenv
load_dotenv()
os.getenv("LANGSMITH_API_KEY")

app = LearEaseApp(__name__)


ext_blueprints.init_app(app)

@app.route('/')
def home():
        return {"status": "success", "message": "Hi, Welcome chatbot-BE"}, 200
