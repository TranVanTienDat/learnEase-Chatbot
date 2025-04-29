
import os
from flask_restful import Resource, request
from models.states import State 
from langChain import write_query, execute_query, generate_answer
from langChain.langChain import LangChain
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
            
            # Tạo state object
            state = State(question=data["question"])
            # Tạo câu truy vấn và thực thi
            langChain = LangChain()
            query_result_state = write_query(state,langChain)
            if query_result_state is None:
                return {"error": "Failed to generate query"}, 500
            
            query_ex_state = execute_query(query_result_state,langChain.db)
            if query_ex_state is None:
                return {"error": "Failed to execute query"}, 500
            
            new_state = State(question=data["question"], query=query_result_state["query"], result=query_ex_state["result"], )

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

