import os
from dotenv import load_dotenv
from openai import OpenAI


class OpenAIAssistant:
    def __init__(self, api_key=None, name="MrRobot", instructions="give me the latest news in Artifical Intelligence \
         for developers", tools=None, model="gpt-3.5-turbo"):
        load_dotenv()
        # self.api_key = api_key
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.model = model
        self.assistant = self.create_assistant()

        # Initialize the OpenAI API client with the provided key and assistant parameters
    
    def check_if_thread_exists(self):
        pass
    
    def create_assistant(self):
        kwargs = {"name": self.name, "instructions": self.instructions, "tools": self.tools, "model": self.model}
        assistant = client.beta.assistants.create(**kwargs)
        return assistant

    def initiate_interaction(self, input_message):
        # Send the input message to the Assistant to initiate the interaction
        pass

    def trigger_assistant(self, input_message):
        # Process the input message to generate a relevant response
        pass

    def get_response_output(self):
        # Retrieve and display the response to the user's message
        pass