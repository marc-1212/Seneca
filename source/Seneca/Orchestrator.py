from Agent.registry.registry import AGENT_REGISTRY
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path
from pydantic import BaseModel, Field
from States.GeneralStates import GeneralState
from langchain_groq import ChatGroq
from langgraph.types import Command
from typing import Literal

posible_routes = tuple([element['name'] for  element in AGENT_REGISTRY.values()]) # Convertir a enteros

class RouteSchema(BaseModel):
    """Selecciona el ID del orquestador de destino."""
    route: Literal[posible_routes] = Field(
        description="the agent selected",
        json_schema_extra={"String": posible_routes}
    )

def build_router_prompt(user_input: str):
        systemPrompt = "You are an router of orquestrators. Choose the best ID acording to the intention of the user.\n"
        systemPrompt+= "List of orquestrators:\n"
        for id, agent in AGENT_REGISTRY.items():
            systemPrompt += f"id: {id}, agent_name: {agent['name']}, agent_description: {agent['description']}\n"
        userPrompt = f"Task: having this prompt from the user: ' {user_input}' .Return response where contains the agent_name of the agent selected according to the intention of the User.\n"
        return ChatPromptTemplate.from_messages(
            [("system", systemPrompt),
            ("human", userPrompt)] 
        )
                
model = ChatGroq(model="llama-3.1-8b-instant",
                            temperature=0)
def Orchestrate(state: GeneralState) -> Command[Literal["Seneca", "Secretary"]]:
    prompt = build_router_prompt(state.GeneralMessages[-1].content)
    chain = prompt | model.with_structured_output(
            RouteSchema
        )
    response_dict = chain.invoke({"user_input": prompt})
    print(response_dict)
    next_node = AGENT_REGISTRY[response_dict.route]["name"]
    print("this is the next NODE:" +  next_node)
    return Command(goto=next_node)


def Seneca__(state: GeneralState):
    "This is an example"
    print("seneca")
    return

def Secretary__(state: GeneralState):
    print("secretaryt")
    "This is another example"
    return
