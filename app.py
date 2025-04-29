from learn_ease_app import LearEaseApp
from config.engine import test_connection
import extensions.ext_blueprints as ext_blueprints
from dotenv import load_dotenv
load_dotenv()

app = LearEaseApp(__name__)


ext_blueprints.init_app(app)

@app.route('/')
def check_db():
    is_connected = test_connection()
    if is_connected:
        return {"status": "success", "message": "Database connected successfully"}
    else:
        return {"status": "error", "message": "Database connection failed"}, 500
