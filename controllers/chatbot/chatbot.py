
import os
from flask_restful import Resource, request
from models.states import State 
from langChain import write_query, execute_query, generate_answer
from langChain.langChain import LangChain
from filters.query_full import create_full_chain
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
            
            sql_prompt = """Given a natural language question, generate ONLY the SQL query needed to answer it. 
                Do not add any explanation, preamble, or extra text. Return only raw SQL.
                When selecting from tables, only use the following columns:
                - classes: name, full_name
                - seasons: name, duration
                - subject: name
                Question: """ + data["question"]
            data["question"] = sql_prompt
            
            # Tạo state object
            state = State(question=data["question"])
            # Tạo câu truy vấn và thực thi
            langChain = LangChain()

            # create query
            chain = create_full_chain(langChain.llm, langChain.db)
            query_text = chain.invoke({
                        "question": state["question"]
                                })
            query_state = State( query=query_text)

            # query_result_state = write_query(state,langChain)
            # if query_result_state is None:
            #     return {"error": "Failed to generate query"}, 500
            
            query_ex_state = execute_query(query_state,langChain.db)
            if query_ex_state is None:
                return {"error": "Failed to execute query"}, 500
            
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

