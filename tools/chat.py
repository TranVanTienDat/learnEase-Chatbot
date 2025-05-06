import json
from langChain.langChain import LangChain
from langchain.chat_models import init_chat_model
from models.type_question import TypeQuestion
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

system = """
You are a smart assistant.
You will answer the usual questions
"""

@tool
def type_question(question):
    """Đây là tool dùng để trả lời câu hỏi tự nhiên và khi muốn đăng kí nhưng chưa có thông tin thì xin thêm thông tin"""
    llm =  init_chat_model("gemini-2.0-flash", model_provider="google_genai")
  
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{input}")])
    chain = prompt | llm

    # Invoke (gửi câu hỏi thật sự vào chuỗi)
    result = chain.invoke({"question": question})

    return result

