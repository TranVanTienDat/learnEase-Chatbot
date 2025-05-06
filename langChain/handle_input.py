import json
from langChain.langChain import LangChain
from langchain.chat_models import init_chat_model
from models.type_question import TypeQuestion
from langchain_core.prompts import ChatPromptTemplate

system = """
You are a smart assistant.
- If the user's request is about **courses**, **classes**, **subjects**, **schedules**, or **student registration**, then respond based on the following rules:
    - If the request requires querying existing data, respond with action "query".
    - If the request is about **student registration**:
        - If the input **includes full information** (student name, parent name, phone number, class name), respond with action "register_student".
        - If the input **does not include all required information**, respond with action "chat" and guide the user to provide:
            - Student name
            - Parent name
            - Phone number
            - Class name
- If a normal conversational answer is enough, respond with action "chat".

Always respond in JSON format with two fields:
- "action": one of "chat", "query", or "register_student"
- "answer": a detailed and helpful answer to the user's question.

If action is "query", provide a short explanation of the query needed.
If action is "chat", provide a full, helpful answer or guidance.
If action is "register_student", confirm that the student can be registered with the provided information.

Respond with JSON only, no additional explanation.
"""



def type_question(question):
    llm =  init_chat_model("gemini-2.0-flash", model_provider="google_genai")
  
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{input}")])
  
    structured_llm = llm.with_structured_output(TypeQuestion)
    few_shot_structured_llm = prompt | structured_llm
    return few_shot_structured_llm.invoke({"input": question})
