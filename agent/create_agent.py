from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from tools.chat import type_question
from tools.query import query_tool
from tools.create_student import create_student
def  new_agent():
    memory = MemorySaver()
    model =  init_chat_model("gemini-2.0-flash", model_provider="google_genai")
    tools = [type_question,create_student,query_tool]
    agent_executor = create_react_agent(model, tools, checkpointer=memory)
    return agent_executor