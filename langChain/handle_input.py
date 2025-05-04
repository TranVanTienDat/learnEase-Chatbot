import json
from langChain.langChain import LangChain

def ask_llama(user_message):
    langchain = LangChain()
    prompt = f"""
You are a smart assistant.

Based on the user's question: "{user_message}"

- If a database query is needed, respond ONLY with a JSON object like:
{{"action": "query", "sql": "<SQL_QUERY>"}}

- If a normal answer is enough, respond ONLY with a JSON object like:
{{"action": "chat", "answer": "<your reply>"}}

Important rules:
- Only output a raw JSON object.
- Do not include any explanations, markdown, code block markers, or extra text.
- Ensure the JSON is 100% valid.
"""
    response = langchain.llm.invoke(prompt)
    
    try:
        return json.loads(response.content)  
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON returned from LLM: {response.content}")
