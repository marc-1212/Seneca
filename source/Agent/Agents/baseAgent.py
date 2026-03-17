


from States.GeneralStates import GeneralState
import os 
from langchain_core.prompts import ChatMessagePromptTemplate

class baseAgent:
    def __init__(self, llm):
        self.llm = llm
        self.state: GeneralState
        self.prompt: ChatMessagePromptTemplate
    
