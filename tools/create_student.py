from langchain_core.tools import tool
from langChain.langChain import LangChain
from filters.query_full import create_full_chain
from models.states import State 
from langChain import  execute_query, generate_answer
from lib.convert_text_to_sql import extract_sql_code

@tool
def create_student(question:str):
    """Đây là tool dùng để thêm học sinh vào bảng registions_student"""
    langChain = LangChain()
    chain = create_full_chain(langChain.llm, langChain.db, "register_student")
    query_text =  chain.invoke({
                    "question": question
                })

    sql = extract_sql_code(query_text)
    query_state = State( query=sql)

    
    query_ex_state = execute_query(query_state,langChain.db)
    new_state = State(question=question, query=query_state["query"], result=query_ex_state["result"], )

    response = generate_answer(new_state,langChain.llm)
    return response