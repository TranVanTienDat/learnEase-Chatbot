
import os
from flask_restful import Resource, request
from models.states import State 
from langChain import write_query, execute_query, generate_answer
from langChain.langChain import LangChain
from filters.query_full import create_full_chain
from lib.convert_text_to_sql import extract_sql_code
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
            
            sql_prompt = """
            You are a SQL query generator. You will be given a question and you need to generate a SQL query to answer that question.
            Output only the SQL query, nothing else.
            When selecting from tables, only use the following columns:
                - classes: name, full_name
                - seasons: name, duration
                - subject: name
            and no limit on the number of rows.
            Wrap your SQL query inside triple backticks and specify 'sql' language like ```sql.
            Output only the SQL query wrapped inside the code block, nothing else.
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
            
            sql = extract_sql_code(query_text)
            query_state = State( query=sql)

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

