

AGENT_REGISTRY = {}
def agent(name :str, description: str):
    def decorator(agentClass):
        AGENT_REGISTRY[name] = {
            "id": len(AGENT_REGISTRY),
            "name" : name,
            "description" :description,
            "class" : agentClass
        }
        agentClass.description = description
        agentClass.name = name
        return agentClass
    return decorator