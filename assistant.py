import os, shelve
from dotenv import load_dotenv
from openai import OpenAI


class OpenAIAssistant:
    def __init__(self, api_key=None, name="MrRobot", \
        instructions="give me the latest news in Artifical Intelligence \
        for developers", tools=None, model="gpt-3.5-turbo"):
        load_dotenv()
        self.client = OpenAI()
        self.thread_id = None #updated with self.create_thread
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.model = model
        self.assistant = None #updated with self.create(assistant)
        self.active_messages = []

    def create_message(self, message="When is Christmas in America?"):
        id = self.get_thread_id()
        if not id:
            self.create_thread()
        else:
            id =  self.get_thread_id()

        data = {"thread_id": id, "role": "user", "content": message}

        message = self.client.beta.threads.messages.create(**data)
        print(message)
        

    def get_thread_id(self):
        with shelve.open('db') as db:
             # Retrieve the value associated with the key
            value = db[self.name]
            # Do something with the value
            print(value)
            return value

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
            self.thread_id = thread.id
            print('new thread saved to db')
            return thread.id 

   
            
            
        

roboto = OpenAIAssistant()
roboto.create_thread()
roboto.create_message()