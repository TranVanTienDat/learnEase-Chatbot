
import os
from flask_restful import Resource, request
from models.states import State 
from langChain import write_query, execute_query, generate_answer
from langChain.langChain import LangChain
from filters.query_full import create_full_chain
from lib.convert_text_to_sql import extract_sql_code
from langChain.handle_input import type_question
from langchain.chains import create_sql_query_chain
# prompt = """\n\nOnly return to the standard SQL command and do not provide any more information\n         
# Rules:
# - Only select allowed columns:
#   - classes: name, full_name
#   - seasons: name, duration
#   - subjects: name
# - Do NOT select any columns like id, *_id, key, *_key."""
class Chatbot(Resource):
    def get(self):
        return {
            "message": "Chatbot API is running!"
        }, 200

    # def post(self):
    #     try:
    #         # Lấy dữ liệu từ request
    #         data = request.get_json()
    #         # Kiểm tra xem có question trong data không
    #         if "question" not in data:
    #             return {"error": "Missing question in request"}, 400
            
    #         type_action = type_question(data["question"])
    #         print("Type Answer: ", type_action)
    #         if type_action["action"] == "chat":
    #             return {
    #                 "status": "success",
    #                 "data": {
    #                     "content": type_action["answer"]
    #                 }
    #             }, 201
            
          
            
    #         state = State(question=data["question"])
    #         langChain = LangChain()

    #         chain = create_full_chain(langChain.llm, langChain.db, type_action["action"])

    #         if type_action["action"] == "register_student":
    #             query_text = chain.invoke({
    #                 "question": state["question"] + type_action["answer"]
    #             })
    #         else:
    #             query_text = chain.invoke({
    #                 "question": state["question"]
    #             })
            

    #         print("Query Text: ", query_text)

    #         sql = extract_sql_code(query_text)
    #         query_state = State( query=sql)

    
    #         query_ex_state = execute_query(query_state,langChain.db)
    #         new_state = State(question=data["question"], query=query_state["query"], result=query_ex_state["result"], )

    #         response = generate_answer(new_state,langChain.llm)

        
            

    #         return {
    #             "status": "success",
    #             "data": response
    #         }, 201
            
    #     except Exception as e:
    #         return {
    #             "status": "error",
    #             "message": str(e)
    #         }, 500

