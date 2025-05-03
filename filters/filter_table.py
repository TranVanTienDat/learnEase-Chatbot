from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langChain.langChain import LangChain


class Table(BaseModel):
    """Table in SQL database."""
    
    name: str = Field(description="Name of table in SQL database.")

def create_table_chain():
    langChain = LangChain()

    system  = """Return the names of any SQL tables that are relevant to the user question.
    The tables are:
    
    classes
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{input}"),
        ]
)
    llm_with_tools = langChain.llm.bind_tools([Table])
    output_parser = PydanticToolsParser(tools=[Table])
    category_chain = prompt | llm_with_tools | output_parser

    return category_chain
