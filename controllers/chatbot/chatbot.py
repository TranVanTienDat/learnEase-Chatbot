
import os
from flask_restful import Resource, request
from models.states import State 
from langChain import write_query, execute_query, generate_answer
from langChain.langChain import LangChain
from filters.query_full import create_full_chain
from lib.convert_text_to_sql import extract_sql_code
from langChain.handle_input import ask_llama
class Chatbot(Resource):
    def get(self):
        return {
            "message": "Chatbot API is running!"
        }, 200

    def post(self):
        try:
            # Lấy dữ liệu từ request
            data = request.get_json()
            # Kiểm tra xem có question trong data không
            if "question" not in data:
                return {"error": "Missing question in request"}, 400
            
            type_answer = ask_llama(data["question"])
            if type_answer["action"] == "chat":
                return {
                    "status": "success",
                    "data": {
                        "content": type_answer["answer"]
                    }
                }, 201
            
            state = State(question=data["question"])
            langChain = LangChain()

            # create query
            chain = create_full_chain(langChain.llm, langChain.db)
            query_text = chain.invoke({
                        "question": state["question"]
                                })
            
            sql = extract_sql_code(query_text)

            print("SQL Query: ", sql)

            query_state = State( query=sql)

            query_ex_state = execute_query(query_state,langChain.db)
            if query_ex_state is None:
                return {"error": "Failed to execute query"}, 500
            
            print("Query Result: ", query_ex_state["result"])
            
            new_state = State(question=data["question"], query=query_state["query"], result=query_ex_state["result"], )

            response = generate_answer(new_state,langChain.llm)

        
            

            return {
                "status": "success",
                "data": response
            }, 201
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }, 500

