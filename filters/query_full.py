from operator import itemgetter
from langchain.prompts import PromptTemplate

from langchain.chains import create_sql_query_chain
from filters.filter_table import create_table_chain
from filters.table_group import get_tables
from langchain_core.runnables import RunnablePassthrough

sql_prompt = sql_prompt = """
You are a professional SQL query generator.
Your task: Based on a given natural language question, generate the corresponding SQL query.

Important Rules:
- Only use the following tables:
{table_info}

- Use at most {top_k} tables to generate the query.
- Do not apply any row limitation (e.g., do not use LIMIT).
- Make sure the SQL query is syntactically correct.

Output Requirements:
- Output only the SQL query.
- Wrap the SQL query inside triple backticks and specify the 'sql' language.
- No explanations, comments, or text outside the code block.

Question: {input}
"""


# Tạo PromptTemplate đúng
prompt = PromptTemplate.from_template(sql_prompt)


def create_full_chain(llm, db):

    category_chain = create_table_chain()
    table_chain = category_chain | get_tables
    
    # Create the SQL query chain
    query_chain = create_sql_query_chain(llm, db, prompt=prompt)
    # Convert "question" key to "input" key
    table_chain = {"input": itemgetter("question")} | table_chain 
    # Compose the full chain
    return RunnablePassthrough.assign(table_names_to_use=table_chain) | query_chain