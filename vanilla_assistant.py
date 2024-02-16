# import os
from dotenv import load_dotenv
from openai import OpenAI
import time, json



class OpenAIAssistant:
    def __init__(self, assistant_name="MrRobot", \
        instructions="Provide an answer for all questions",  model="gpt-3.5-turbo"):
        #uses a .env file with OPENAI_API_KEY variable 
        load_dotenv()
        self.client = OpenAI()
        self.thread_id = None #updated with self.create_thread
        self.name = assistant_name
        self.instructions =   instructions
        self.model = model
        self.file_paths = []
        self.assistant = self.create_assistant_on_init()

    def upload_file(self, file_path):
        
        if file_path not in self.file_paths:
            self.file_paths.append(file_path)
            file = self.client.files.create( file=open(file_path, "rb"),  purpose='assistants')
            # if file.id not in self.file_ids:
                # self.file_ids.append(file.id)    
        print('file uploaded')


    
    def update_system_prompt(self, prompt):
       
        val = prompt

        self.instructions = val

        return val


    
    def run_errand_get_messages(self, thread_id, assistant_id ,instructions):
        try: 
            kwargs = {
                "thread_id": thread_id,
                "assistant_id": assistant_id,
                "instructions": instructions
            }
            run = self.client.beta.threads.runs.create(**kwargs)

            while run.status != 'completed':
                time.sleep(5)
                run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
                )

            messages = self.client.beta.threads.messages.list( thread_id=thread_id )
            print("\n\n" + messages.data[0].content[0].text.value + "\n\n")
            return messages
        except Exception as e:
            print(str(e))
        
      

    def create_message(self,thread_id, message):        
        try: 
            data = {"thread_id": thread_id, "role": "user", "content": message}
            message = self.client.beta.threads.messages.create(**data)

        except Exception as e:
            print(str(e))

        
        

    def create_assistant_on_init(self):
    
        kwargs = {"name": self.name, "instructions": self.instructions, "model": self.model}
        try:
            assistant = self.client.beta.assistants.create(**kwargs)
            self.assistant =  assistant           
            return self.assistant

        except Exception as e:
            print(str(e))
            return str(e)

    def create_thread(self):
        try:           
            thread = self.client.beta.threads.create()
            self.thread_id = thread.id
            return thread
        except Exception as e:
            print(str(e))


agent = OpenAIAssistant(assistant_name="SecureBot")

agent.update_system_prompt("You are a AI security expert, answer all questions based on information in your knowledge base")

agent.upload_file("owasp_testing.pdf")


agent.create_thread()

agent.create_message(agent.thread_id,"What is OWASP?")
res = agent.run_errand_get_messages(agent.thread_id,agent.assistant.id,agent.instructions)
print(res)

       
        