

AGENT_REGISTRY = {}
def agent(name :str, description: str):
    def decorator(agentClass):
        AGENT_REGISTRY[len(AGENT_REGISTRY) + 1] = {
            "name" : name,
            "description" :description,
            "class" : agentClass
        }
        return agentClass
    return decorator