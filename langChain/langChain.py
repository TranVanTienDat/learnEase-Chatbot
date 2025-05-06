import os
from flask_restful import Resource
from langchain_community.utilities import SQLDatabase
from langchain.chat_models import init_chat_model
from config.engine import get_db_credentials
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from urllib.parse import quote_plus
from dotenv import load_dotenv
load_dotenv()

os.environ.get("TOGETHER_API_KEY")
os.environ.get("GOOGLE_API_KEY")
class LangChain:
    _instance = None
    
    def __new__(cls, db_url: str = None):
        if cls._instance is None:
            cls._instance = super(LangChain, cls).__new__(cls)
            configDB = get_db_credentials()
            encoded_password = quote_plus(configDB['password'])
            db_url = f"postgresql://{configDB['user']}:{encoded_password}@{configDB['host']}:{configDB['port']}/{configDB['db']}"
            
            cls._instance.db = SQLDatabase.from_uri(db_url)
            cls._instance.llm = init_chat_model("meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", model_provider="together")
            cls._instance.execute_query_tool = QuerySQLDatabaseTool(db=cls._instance.db)
        return cls._instance