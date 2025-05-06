from typing_extensions import Annotated
from models.states import State
from typing import TypedDict
from langchain import hub
from langchain_community.utilities import SQLDatabase
from langChain.langChain import LangChain
query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

SIMPLE_PROMPT = """Given the following database schema and a question, generate a SQL query to answer the question.

Database Schema:
{table_info}

Question: {input}

Generate a SQL query that answers the question. Only return the SQL query, nothing else."""

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]


def write_query(state: State):
    """Generate SQL query to fetch information."""
    langChanin = LangChain('postgresql://postgres:aA%4012345@127.0.0.1:5432/learnEase')

    prompt = query_prompt_template.invoke(
        {
            "dialect": langChanin.db.dialect,
            "top_k": 6,
            "table_info": langChanin.db.get_table_info(["classes", "seasons", "subjects","seasons_class_links","classes_subjects_links","components_setting_schedules"]),
            "input": state["question"],
        }
    )

  
    structured_llm = langChanin.llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}