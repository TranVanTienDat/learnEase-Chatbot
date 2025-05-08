
from flask_restful import Resource, request
from agent.create_agent import new_agent
from langchain_core.messages import HumanMessage
from agent.extract_messages import extract_content_from_chunk
class Chat(Resource):
    def get(self):
        return {
            "message": "chat ready!"
        }, 200
    
    def post(self):
        try:
            # Lấy dữ liệu từ request
            data = request.get_json()
            # Kiểm tra xem có question trong data không
            if "question" not in data:
                return {"error": "Missing question in request"}, 400

            thread_id = data["id"]
            config = {"configurable": {"thread_id": thread_id}}
            agent_executor=new_agent(thread_id)
            full_content=""
            for chunk in agent_executor.stream({"input": data["question"]} ):
                full_content+=extract_content_from_chunk(chunk)
                
            print("full_content",full_content)
            return {
                "status": "success",
                "data":{
                    "content": full_content
                }
            }, 201
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }, 500

