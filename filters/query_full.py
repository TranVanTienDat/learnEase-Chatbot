from operator import itemgetter

from langchain.chains import create_sql_query_chain
from filters.filter_table import create_table_chain
from filters.table_group import get_tables
from langchain_core.runnables import RunnablePassthrough

def create_full_chain(llm, db):

    category_chain = create_table_chain()
    table_chain = category_chain | get_tables
    # Create the SQL query chain
    query_chain = create_sql_query_chain(llm, db)
    # Convert "question" key to "input" key
    table_chain = {"input": itemgetter("question")} | table_chain 
    
    # Compose the full chain
    return RunnablePassthrough.assign(table_names_to_use=table_chain) | query_chain