
from typing import Annotated, List, Union, TypedDict
from pydantic import BaseModel, Field
from datetime import date
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

class SenecaState(BaseModel):
    topic: str
    notableReflexions: Annotated[List[str], add_messages]


class SecretaryState(BaseModel):
    EventName: str
    place: str
    dates: date


class GeneralState(BaseModel):
    GeneralMessages: Annotated[List[BaseMessage], add_messages]
    seneca: SenecaState | None
    secretary: SecretaryState | None
    lastNode: str
