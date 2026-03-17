from Agent.Agents.baseAgent import baseAgent
from Agent.registry.registry import agent
from langchain.tools import tool
from States.GeneralStates import GeneralState, SenecaState
from langchain_core.messages import SystemMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from itertools import zip_longest
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
import requests 

class stoicMessage(BaseMessage):
    type : str = "Stoic"


@agent(name= "Seneca", 
       description = "You are an AI philosopher modeled after Seneca. You speak with calm wisdom, clarity, and reason. Your purpose is to help the user live with virtue, discipline, and tranquility through stoic philosophy. You are not afraid to tell uncomfortable truths if they serve the user's growth. You guide the user to focus on what is within their control, to accept what cannot be changed, and to act with integrity and reason. Your tone is serene, thoughtful, and direct — never harsh, but never flattering. You use examples, metaphors, and reflections drawn from Stoic thought. When the user feels lost, angry, or confused, help them return to reason and self-mastery. Encourage the user to seek peace through acceptance, simplicity, and awareness of mortality. Speak like a mentor and a friend who values truth over comfort. If the user asks for advice, respond as Seneca would: grounded in Stoicism, disciplined, and sincere."
       )
class StoicAgent(baseAgent):
    def __init__(self, llm):
        super().__init__(llm)
        self.embedding_model = OllamaEmbeddings(model="nomic-embed-text")
        self.db = Chroma(persist_directory="../../Estoicism_vector_db", embedding_function=self.embedding_model)
        self.seneca :SenecaState
        self.promptTemplate : ChatPromptTemplate = ChatPromptTemplate.from_template("""
        You are Seneca, the Stoic philosopher. Try to emulate as we are speaking in a talk, be natural, don't overextend explanations if it is not necessary and be pro active asking the user how can you help him.
        It is not necessary to  take into account all the context from the stoic writings.
        Be effective, and answer in the language the user question is talking.

        Context from Stoic writings:
        {context}

        Conversation history:
        {conversation}

        User question:
        {question}

        Respond with calm stoic wisdom.
        """)
    def search_wisdom(self, query:str):
        """Retrieve information to help answer a query. Use it for each new response you give for a new question or topic. And adapt use the information retrieved to generate the response"""
        print(self.db._collection.count())
        retrieved_docs = self.db.similarity_search(query, k=5)
        docs = [doc.page_content  for doc in retrieved_docs]

        return docs

    def recover_conversation(self): 
        self.conversation = ""
        for i in range(len(self.state.messages)):
            if self.state.messages[i].type == "Stoic" and i != 0:
                self.conversation += self.state.messages[i -1].content
                self.conversation += self.state.messages[i].content

    def rewrite_query(self, text: str):
            prompt = f"""
            Rewrite this sentence to search for Stoic texts for a RAG.
            Return only one sentence.

            Text:
            {text}
        """
            return self.llm.invoke(prompt)
    
    def __call__(self, state: GeneralState):
        self.state = state
        self.seneca = state.seneca
        self.seneca.query_last_msg = self.rewrite_query(self.state.messages[-1].content)
        docs = self.search_wisdom(self.seneca.query_last_msg.content)
        self.recover_conversation()
        if self.conversation:
            self.state.seneca.query_conversation = self.rewrite_query(self.conversation)
            docs += self.search_wisdom(self.state.seneca.query_conversation.content) 
        prompt = self.promptTemplate.invoke({
            "context": docs,
            "conversation": self.conversation,
            "question": self.state.messages[-1]
        })
        response = self.llm.invoke(prompt)
        print(response.content)
        state.messages.append(stoicMessage(response.content))
        state.seneca = self.seneca
        return state


