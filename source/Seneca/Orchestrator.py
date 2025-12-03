from Agent.Agents.baseAgent import baseAgent
from Agent.registry.registry import AGENT_REGISTRY
import json
from pathlib import Path

schema_path = Path(__file__).parent.parent /"Schemas"/"orquestrator_schema.json"

with open(schema_path, 'r') as f:
    schema = json.load(f)

class Orchestrator(baseAgent):
    def __init__(self):
        super().__init__()
        
    def talk(self):
        while True:    
            super().talk()
            userInput =  super().get_user_input()


    def send_msg_to_GPT(self, userPrompt):
        print(userPrompt)
        prompt = self.build_router_prompt(userPrompt)
        schema = self.build_schema_prompt()    
        response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                max_completion_tokens=500,
                messages=[{"role": "user", "content": prompt}],
                functions=[schema],
                temperature=0,
                function_call='auto',
            )

        if response.choices[0].finish_reason != "function_call" :
            raise ValueError("Orchestrator not working properly:" + response.choices[0].finish_reason)
        arguments = response.choices[0].message.function_call.arguments
        route = json.loads(arguments)
        print(route)
        return int(route['route'])

    def build_schema_prompt(self):
        schema["parameters"]["properties"]["route"]["enum"] = list(AGENT_REGISTRY.keys())
        return schema
   
    def build_router_prompt(self, user_input: str):
        prompt = "You are an router of orquestrators. Choose the best ID acording to the intention of the user.\n"
        prompt += "List of orquestrators:\n"
        for id, agent in AGENT_REGISTRY.items():
            print(id, agent["name"])
            prompt += f"id: {id}, agent_name: {agent["name"]}, agent_description: {agent["description"]}\n"
        prompt += user_input + '\n'
        prompt += "Task: Return a JSON response where contains the ID of the agent selected according to the intention of the User.\n"
        prompt += "Example: {\"Route\": 1}"
        return prompt
        