from Agent.Agents.baseAgent import baseAgent
from Agent.registry.registry import agent
from States.GeneralStates import GeneralState
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from typing import Annotated
from langgraph.types import Command
import requests
import json
from langchain.agents import create_agent
import os
class secretaryMessage(BaseMessage):
    type : str = "Secretary"
    content :  str

@agent(name="Secretary", 
description = "You are a smart personal secretary assistant. Your job is to help him stay organized, remember meetings, manage his schedule, and find useful information online such as places to eat, work, or relax. You should be professional, polite, and efficient, with an organized and proactive personality. Your goal is to make Marc’s day easier and more productive. Main responsibilities: (1) Reminders & Scheduling: remember meetings, appointments, and tasks; organize daily or weekly schedules; send reminders before important events; prevent overlapping meetings. (2) Web Research: search for restaurants, cafés, gyms, coworking spaces, or local events; provide up-to-date and location-based results with details such as name, type, address, reviews, and links. (3) Logistical Support: answer practical questions about locations, opening hours, or travel times; plan transportation; maintain to-do lists. (4) Time Management: suggest ideal times for meetings, rest, or exercise; reorganize plans when something changes; identify free slots in Marc’s day. Operational guidelines: always confirm the time, date, and location when adding events; use web search when Marc asks for real-world or current information; include name, type, address, rating, and link when showing search results. Communication style: natural, professional, and warm; brief but complete; ask clarifying questions if something is unclear. Example interactions: Marc: 'Add a meeting with the AI team on Thursday at 10:00.' Assistant: 'Got it. I’ve scheduled your meeting with the AI team for Thursday at 10:00. Would you like me to remind you 15 minutes before?' Marc: 'Find me a place to eat sushi near my office.' Assistant: 'I found three sushi restaurants near your office: 1. Kibō Sushi – 4.7 stars, 112 Mallorca Street; 2. SushiYa BCN – 4.5 stars, 45 Casanova Street; 3. Sato i Tanaka – 4.8 stars, 120 Bruc Street. Would you like me to book a table at one of them?'"
)
class secretaryAgent(baseAgent):
    def __init__(self, llm):
        super().__init__(llm)   
        self.agent = create_agent(self.llm, [search_places, get_place_details_batch]).with_config({"recursion_limit":5})
    def __call__(self, state: GeneralState):
        try:
            last_query = state.messages[-1].content
            ai_msg = self.agent.invoke({"messages": HumanMessage(content=last_query)})
        except Exception as e :
            if  "GRAPH_RECURSION_LIMIT" in str(e):
                print("No encuentro informacion disponible")
                return Command(
                update={"messages": [secretaryMessage(content="No se ha encontrado informacion disponible", name="Secretary")] },
                goto="UserInput"
            )
            return Command(
                update={"messages": [secretaryMessage(content=ai_msg["messages"][-1].content, name="Secretary")] },
                goto="UserInput"
            )        



def search_places(dict_args: dict):
    """
    Busca lugares usando Google Maps Places API.
    dict_args : dict argumento que se tien e que pasar
    dict_args puede tener:
        - place: str sitio donde buscaras
        - radius: int (metros, opcional)
        - type: str (restaurant, cafe, etc.)
    Devuelve:
        - lista de lugares con name, place_id, rating, location
    """


    API_KEY = os.environ('GOOGLE_MAPS_API_KEY')
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "key": API_KEY,
        "type": dict_args.get("type", "restaurant"),
        "radius": dict_args.get("radius", 2000),
    }
    if "city" in dict_args:
        endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params["query"] = f"{dict_args.get('type', 'restaurant')} in {dict_args['city']}"

    response = requests.get(endpoint, params=params).json()
    results = []

    for r in response.get("results", []):
        results.append({
            "name": r.get("name"),
            "place_id": r.get("place_id"),
            "rating": r.get("rating"),
            "location": r.get("geometry", {}).get("location")
        })

    return results

def get_place_details_batch(place_ids: list):
    """
    Obtiene detalles de varios lugares de Google Maps usando Place Details API.
    Devuelve un diccionario {place_id: {...datos...}}
    """

    API_KEY = os.environ('GOOGLE_MAPS_API_KEY')
    endpoint = "https://maps.googleapis.com/maps/api/place/details/json"

    details = {}

    for pid in place_ids:
        params = {
            "place_id": pid,
            "key": API_KEY,
            "fields": "name,rating,formatted_phone_number,opening_hours,website"
        }
        response = requests.get(endpoint, params=params).json()
        result = response.get("result", {})

        details[pid] = {
            "name": result.get("name"),
            "rating": result.get("rating"),
            "phone": result.get("formatted_phone_number"),
            "website": result.get("website"),
            "opening_hours": result.get("opening_hours")
        }

    return details