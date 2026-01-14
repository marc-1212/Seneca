from Agent.Agents.baseAgent import baseAgent
from Agent.registry.registry import agent
from langchain.tools import tool
from States.GeneralStates import GeneralState
from langchain_core.messages import SystemMessage
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

@agent(name= "Seneca", 
       description = "You are an AI philosopher modeled after Seneca. You speak with calm wisdom, clarity, and reason. Your purpose is to help the user live with virtue, discipline, and tranquility through stoic philosophy. You are not afraid to tell uncomfortable truths if they serve the user's growth. You guide the user to focus on what is within their control, to accept what cannot be changed, and to act with integrity and reason. Your tone is serene, thoughtful, and direct — never harsh, but never flattering. You use examples, metaphors, and reflections drawn from Stoic thought. When the user feels lost, angry, or confused, help them return to reason and self-mastery. Encourage the user to seek peace through acceptance, simplicity, and awareness of mortality. Speak like a mentor and a friend who values truth over comfort. If the user asks for advice, respond as Seneca would: grounded in Stoicism, disciplined, and sincere."
       )
class StoicAgent(baseAgent):
    def __init__(self, llm):
        super().__init__(llm)


    def talk(self):
        def __talk(state :GeneralState):
            print("Seneca")
            return
            mytools = [conclusion, search_wisdom]
            llm_with_tools = self.llm.bind_tools(mytools)
            System  =     [
            SystemMessage(content=self.description)
        ]
            response = llm_with_tools.invoke(System + state.GeneralMessages)
            print(response)
            state.GeneralMessages.append(response)
            
            state.lastNode = "Seneca"
            return state
        return __talk

@tool(response_format="content_and_artifact")
def search_wisdom(query: str) ->str:
    """Retrieve information to help answer a query. Use it anytime you want to give the user a response"""
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory='../../chroma_db', embedding_function=embedding_model)
    retrieved_docs = db.similarity_search(query, k=3)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    print("hola" + serialized, retrieved_docs)
    return serialized, retrieved_docs


@tool
def conclusion(meditation: str) -> float:
    """Use any time the user has finnished a reflexion, or says I want to save this meditation"""
    print("meditation")
    return 0