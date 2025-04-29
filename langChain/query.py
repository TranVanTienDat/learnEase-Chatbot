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
                "table_info": langChain.db.get_table_info(["classes"]),
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
    print(f"execute_query_tool: {execute_query_tool}")
    return {"result": execute_query_tool.invoke(state["query"])}


def generate_answer(state: State,llm):
    """Answer question using retrieved information as context."""
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}\n\n'
        "Please provide a clear and natural response in Vietnamese language."
    )
    response = llm.invoke(prompt)
    return {"content": response.content}