from groq import Groq
import os 
class baseAgent:
    def __init__(self):
        self.client =Groq(
            api_key=os.environ.get("GROQ_API_KEY")
        )
    def init_open_ai(self):
        pass
    
    def talk(self):
        self.msg = "User: "
        self.user_input = input(self.msg)
        print(self.user_input)
    
    def get_user_input(self):
        return self.user_input
    #def get_api_key(self):
    #    return self.__api_key
    
    
