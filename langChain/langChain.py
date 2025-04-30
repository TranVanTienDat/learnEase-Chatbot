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
# class LangChain:
#     def __init__(self, db_url: str):
#         self.db = SQLDatabase.from_uri("postgresql://postgres:aA%4012345@127.0.0.1:5432/learnEase")
#         self.llm = init_chat_model("mistralai/Mixtral-8x7B-Instruct-v0.1", model_provider="together")
#         self.execute_query_tool = QuerySQLDatabaseTool(db=self.db)

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