#from Seneca.Orchestrator import Orchestrator
import argparse
from fastapi import FastAPI
import Agent.registry
from Agent.registry.registry import AGENT_REGISTRY
from Seneca.Orchestrator import Orchestrate, Secretary__, Seneca__
from States.GeneralStates import  GeneralState
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from time import sleep

def recive_message_from_user(state: GeneralState)-> GeneralState:
    user_input = input("User:" )
    state.messages.append(HumanMessage(user_input))
    return state
def main():
    #return
    model = ChatGroq(model="openai/gpt-oss-120b",  
                            temperature=0,  verbose=True)
    graph = StateGraph(GeneralState)
    graph.add_node("UserInput", recive_message_from_user)
    graph.add_node("Orchestrator", Orchestrate)
    graph.add_node("Secretary", AGENT_REGISTRY["Secretary"]["class"](model))
    graph.add_node("Seneca", AGENT_REGISTRY["Seneca"]["class"](model))
    graph.set_entry_point("UserInput")
    graph.add_edge("UserInput", "Orchestrator")
    graph.add_edge("Seneca", "UserInput")
    graph.add_edge("Secretary", "UserInput")
    app = graph.compile()
    final_state= app.invoke(
            {
                "messages": [],
                "seneca": {
                     "query_last_msg": None,
                     "query_conversation"  : None    
                },
                "secretary": None,
                "lastNode": ""
            })
    print(final_state)
    return final_state["lastNode"]


if __name__ == "__main__":
    main()
