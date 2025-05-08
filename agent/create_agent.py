from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from tools.chat import type_question
from tools.query import query_tool
from tools.create_student import create_student
from langchain.memory import ConversationBufferMemory
from langchain.agents import create_structured_chat_agent
from langchain.agents import AgentExecutor,create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agents = {}
memories = {}


def  new_agent(id:str):

    model =  init_chat_model("gemini-2.0-flash", model_provider="google_genai")
    tools = [type_question,create_student,query_tool]

  
    memory = get_or_create_memory(id, memories)
   
    if id in agents:
        return agents[id]
    else:
        agent = create_tool_calling_agent(model, tools, prompt)
        agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
    )
        agents[id]=agent_executor
        return agent_executor
    

def get_or_create_memory(id: str, memories: dict):
    """
    Lấy bộ nhớ của người dùng từ dictionary memories. Nếu không có, tạo bộ nhớ mới và lưu vào memories.
    
    Parameters:
    - id (str): ID của người dùng
    - memories (dict): Dictionary lưu trữ bộ nhớ của người dùng

    Returns:
    - memory: Bộ nhớ của người dùng
    """
    if id in memories:
        return memories[id]
    else:
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        memories[id] = memory  # Lưu bộ nhớ vào memories
        return memory