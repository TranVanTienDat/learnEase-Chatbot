from typing_extensions import Annotated
from models.states import State
from typing import TypedDict
from langchain import hub
from langchain_community.utilities import SQLDatabase
from langChain.langChain import LangChain
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool

query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]


def write_query(state: State,langChain :LangChain):
    """Generate SQL query to fetch information."""
    prompt = query_prompt_template.invoke(
            {
                "dialect": langChain.db.dialect,
                "top_k": 10,
                "table_info": langChain.db.get_table_info(),
                "input": state["question"],
            }
        )
    
    structured_llm = langChain.llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}


# example: execute_query({"query": "SELECT COUNT(EmployeeId) AS EmployeeCount FROM Employee;"})
def execute_query(state: State,db):
    """Execute SQL query."""
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}


def generate_answer(state: State,llm):
    """Answer question using retrieved information as context."""
    prompt = (
    "You are an assistant who helps answer user questions about the system. "
    "Do not provide SQL queries or mention SQL in your response.\n\n"
    "Given the following user question, corresponding SQL query, "
    "and SQL result, answer the user question naturally.\n\n"
    f'Question: {state["question"]}\n'
    f'SQL Query: {state["query"]}\n'
    f'SQL Result: {state["result"]}\n\n'
    "1. If the result only contains columns with the names 'id' or 'key', you may use them to answer the question.\n"
    "2. If the result contains columns other than 'id' and 'key', you should only use the data from those columns, ignoring any information from 'id' and 'key'.\n"
    "Please provide a clear and natural response in Vietnamese language.\n"
    "Based on the data above, answer the user's question clearly, concisely, and completely. \n"
    "Do not make assumptions, do not comment on the accuracy of the data, and do not offer advice.\n"
    "If an error occurs, say Sorry the system is faulty"
)
    response = llm.invoke(prompt)
    return {"content": response.content}