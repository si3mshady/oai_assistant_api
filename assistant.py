import os, shelve
from dotenv import load_dotenv
from openai import OpenAI


class OpenAIAssistant:
    def __init__(self, api_key=None, name="MrRobot", instructions="give me the latest news in Artifical Intelligence \
         for developers", tools=[None], model="gpt-3.5-turbo"):
        load_dotenv()
        self.client = OpenAI()

        self.name = name
        self.instructions = instructions
        # self.tools = tools
        self.model = model
        self.assistant = None

    def save_to_db(self, key, value):
        with shelve.open('db') as db:
            db[key] = value

    def check_thread_exists(self,key):
        with shelve.open('db') as db:
            if key in db:
                return True
            pass
    
    def create_assistant(self):
    
        kwargs = {"name": self.name, "instructions": self.instructions, "model": self.model}
        try:
            assistant = self.client.beta.assistants.create(**kwargs)
            print(assistant)
            self.assistant =  assistant
            

        except Exception as e:
            print(str(e))

    def create_thread(self):
        result = self.check_thread_exists(self.name)
        if not result: 
            thread = self.client.beta.threads.create()
            self.save_to_db(self.name, thread.id)
            print('new thread saved to db')
            
            
        

    def initiate_interaction(self, input_message):
        # Send the input message to the Assistant to initiate the interaction
        pass

    def trigger_assistant(self, input_message):
        # Process the input message to generate a relevant response
        pass

    def get_response_output(self):
        # Retrieve and display the response to the user's message
        pass

roboto = OpenAIAssistant()
roboto.create_thread()
