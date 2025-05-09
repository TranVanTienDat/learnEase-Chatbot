from operator import itemgetter
from langchain.prompts import PromptTemplate

from langchain.chains import create_sql_query_chain
from filters.filter_table import create_table_chain
from filters.table_group import get_tables
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

system_select = """You are a {dialect} expert. Given an input question, create a syntactically correct {dialect} query to run.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per {dialect}. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use date('now') function to get the current date, if the question involves "today".

Only use the following tables:
{table_info}

Write an initial draft of the query. Then double check the {dialect} query for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins

Use format:

First draft: FIRST_DRAFT_QUERY
Final answer: FINAL_ANSWER_QUERY
"""


system_insert = """
You are an assistant that generates postgresql INSERT queries.

Given the student's details:
- Student name
- Parent name
- Phone number
- Class name

Generate an SQL INSERT statement to add a new student into the "student_registrations" table. 
Assume that the "student_registrations" table has the following columns:
- "id" (auto-increment, no need to insert)
- "full_name"
- "parent_name"
- "parent_phone"
- "class_name 

Respond only with the SQL needed.
not needed 
-{dialect} dialect.
- {table_info}
- {top_k} results.

Use format:
First draft: <SQLquery>
Final answer: <SQLquery>
"""



def parse_final_answer(output: str) -> str:
    print("Output: ", output)
    output = output.strip()
    if output.startswith("```sql"):
        return output
    return output.split("Final answer: ")[1]

def create_full_chain(llm, db, type_question: str):
    system = system_select if type_question == "query" else system_insert
    prompt = ChatPromptTemplate.from_messages(
    [("system", system), ("human", "{input}")]).partial(dialect=db.dialect)
   
    category_chain = create_table_chain()
    table_chain = category_chain | get_tables
    # Create the SQL query chain
    query_chain = create_sql_query_chain(llm, db, prompt=prompt) | parse_final_answer
    # Convert "question" key to "input" key
    table_chain = {"input": itemgetter("question")} | table_chain 
    # Compose the full chain
    return RunnablePassthrough.assign(table_names_to_use=table_chain) | query_chain