
from typing import Annotated, List, Union, TypedDict
from pydantic import BaseModel, Field
from datetime import date
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage, AIMessage



class SenecaState(BaseModel):
   query_last_msg : AIMessage | None
   query_conversation : AIMessage | None
 

class SecretaryState(BaseModel):
    place_located_user: str
    time: str


class GeneralState(BaseModel):
    seneca: SenecaState | None
    secretary: SecretaryState | None
    messages: Annotated[List[BaseMessage], add_messages]
    lastNode: str

