#from Seneca.Orchestrator import Orchestrator
import argparse
from fastapi import FastAPI
import Agent.registry
from Agent.registry.registry import AGENT_REGISTRY
from Seneca.Orchestrator import Orchestrator

app = FastAPI()

@app.get("/")
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_key", required=True, help="Api Key of OpenAI")  
    Orchestrator().talk()
    return 0 


if __name__ == "__main__":
    main()
