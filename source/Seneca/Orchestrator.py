from Agent.registry.registry import AGENT_REGISTRY
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path
from pydantic import BaseModel, Field
from States.GeneralStates import GeneralState
from langchain_groq import ChatGroq
from langgraph.types import Command
from typing import Annotated, List, Union, TypedDict
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage


from typing import Literal

posible_routes = tuple([element['name'] for  element in AGENT_REGISTRY.values()])

class RouteSchema(BaseModel):
    """Selecciona el ID del orquestador de destino."""
    route: Literal[posible_routes] = Field(
        description="the agent selected",
        json_schema_extra={"String": posible_routes}
    )

def get_converstation(messages: List[BaseMessage]) ->str:
    if len(messages) == 1:
         return ""
    conversation = ""
    for  i in range(len(messages[:-1])):
        conversation = messages[i].type + " : " + messages[i].content + "\n"
    return conversation


def build_router_prompt(state : GeneralState):
        systemPrompt = "You are an router of orquestrators. Choose the best ID acording to the intention of the user.\n"
        systemPrompt+= "List of orquestrators:\n"
        for id, agent in AGENT_REGISTRY.items():
            systemPrompt += f"id: {id}, agent_name: {agent['name']}, agent_description: {agent['description']}\n"
        userPrompt = ""
        conversation = get_converstation(state.messages)
        if conversation != "":
            userPrompt +=  f"Having this conversation:"
            userPrompt += conversation
        userPrompt += f"Task: having this prompt from the user: ' {state.messages[-1].content}' .Return response where contains the agent_name of the agent selected according to the intention of the User.\n"
        return ChatPromptTemplate.from_messages(
            [("system", systemPrompt),
            ("human", userPrompt)] 
        )
                
model = ChatGroq(model="openai/gpt-oss-120b",
                            temperature=0)
def Orchestrate(state: GeneralState) -> Command[Literal["Seneca", "Secretary"]]:
    prompt = build_router_prompt(state)
    chain = prompt | model.with_structured_output(
            RouteSchema
        )
    response_dict = chain.invoke({"user_input": prompt})
    next_node = AGENT_REGISTRY[response_dict.route]["name"]
    print("this is the next NODE:" +  next_node)
    return Command(goto=next_node)
