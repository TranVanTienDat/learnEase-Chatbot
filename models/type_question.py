from typing import Annotated, Optional
from typing_extensions import TypedDict


from typing import Annotated, Literal
from typing_extensions import TypedDict

class TypeQuestion(TypedDict):
    action: Annotated[Literal["chat", "query", "register_student"], "Action type: either 'chat' or 'query' or 'register_student'"]
    answer: Annotated[str, "Answer to the question"]

