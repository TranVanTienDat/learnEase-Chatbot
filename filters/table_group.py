from typing import List
from  filters.filter_table import Table
from filters.filter_table import create_table_chain
from langChain.langChain import LangChain
from langchain_core.runnables import RunnableLambda

def get_tables(categories: List[Table]) -> List[str]:
    tables = []
    for category in categories:
        if category.name == "classes":
            tables.extend(
                [
                    "seasons",
                    "seasons_class_links",
                    "subjects",
                    "classes_subjects_links",
                    "components_setting_schedules"
                ]
            )
    return tables

