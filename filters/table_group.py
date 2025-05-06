from typing import List
from  filters.filter_table import Table
from filters.filter_table import create_table_chain
from langChain.langChain import LangChain
from langchain_core.runnables import RunnableLambda

def get_tables(categories: List[Table]) -> List[str]:
    tables = []
    for category in categories:
        if category.name == "classes" or category.name == "seasons" or category.name == "subjects" or category.name == "course":
            tables.extend(
                [
                    "seasons",
                    "subjects",
                    "seasons_class_links",
                    "classes_subjects_links",
                    "components_setting_schedules",
                    "classes",
                ]
            )
            if(category.name == "register student"):
                tables.extend(["student_registrations"])
    return tables

