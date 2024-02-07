from openai import OpenAI
from dotenv import load_dotenv
import time, json, re
import datetime


current_datetime = datetime.datetime.now()

load_dotenv()

client = OpenAI()

# https://platform.openai.com/docs/assistants/tools/knowledge-retrieval

#get list of assistants
def list_assistants(order="desc",limit=20):
    my_assistants = client.beta.assistants.list(order=order,limit=limit)
    # print([id.id for id in my_assistants.data])
    return [id.id for id in my_assistants.data]


def list_assistant_files(assistant_id):
    assistant_files = client.beta.assistants.files.list(
    assistant_id=assistant_id)
    # print(assistant_files.data)
    return assistant_files.data

def get_assistant_file_mapping():
    res = {assistant_id:list_assistant_files(assistant_id) for assistant_id in list_assistants()}
    print(res)  
    return res

class Retrieval_Assistant:
    def __init__(self, assistant_name="Soccer_BOT", \
       instructions="You are a elite workout assistant. You must use the document uploaded  \
       to create new training programs with definitions is json format. \
       You must include BOTH a 'definitions' key and object and 'training_program' key and object with each response. \
       Here is an example for you to follow: ",
        
              model="gpt-3.5-turbo-1106"):
       self.client = OpenAI()
       load_dotenv()       
       self.thread_id = None #updated with self.create_thread
       self.name = assistant_name
       self.instructions =   instructions
       self.model = model
       self.assistant = None
       self.file_ids = []
       self.json_file = "generic.json"
       self.json_response = "workout_example.json"
       self.file_paths = []
    
    def upload_file(self, file_path):
        
        if file_path not in self.file_paths:
            self.file_paths.append(file_path)
            file = client.files.create( file=open(file_path, "rb"),  purpose='assistants')
            if file.id not in self.file_ids:
                self.file_ids.append(file.id)    

        print('file uploaded')

    def create_assistant_on_init(self):

        if len(self.file_ids) < 1:
            print("Please supply a document that will be used for retrevial with this assistant. ")
            return 
    
        kwargs = {"name": self.name, "instructions": self.instructions, \
        "tools":[{"type": "retrieval"}], "file_ids":self.file_ids, "model": self.model}
        try:
            assistant = self.client.beta.assistants.create(**kwargs)
            self.assistant =  assistant           
            print("New assistant created " + self.assistant.id)
            return self.assistant

        except Exception as e:
            print(str(e))
            return str(e)

    def create_thread(self):
       try:           
           thread = self.client.beta.threads.create()
           self.thread_id = thread.id
           print("New thread created " + str(thread.id))
           return thread
       except Exception as e:
           print(str(e))

    def create_message_in_tread(self, user_message):
        format_message = f"{user_message}"
        message = client.beta.threads.messages.create( thread_id=self.thread_id, role="user",
        content=user_message)

        print("New message created " + message.id)
    
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
            clean_message =  messages.data[0].content[0].text.value 

            # return {"response": str(clean_message)}
            return clean_message
        except Exception as e:
            print(str(e))

    def load_json_file(self, file_path):
        try:
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                return data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {file_path}")
            return None

    def load_json_sample_response(self, file_path):
        try:
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                return data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {file_path}")
            return None

    
    def update_system_prompt(self):
        # schema = self.load_json_file(self.json_file) 
        val = f"{self.load_json_sample_response(self.json_response)}."
        self.instructions = val



        

#upload files 
#create assistant 
#create thread 
#create message 
#get response 

file_name_a = "Soccer.docx"


ra = Retrieval_Assistant()

ra.update_system_prompt()

ra.upload_file(file_name_a)
time.sleep(3)

ra.create_assistant_on_init()
ra.create_thread()
ra.create_message_in_tread(f"Make a new a workout plan based on Soccer. \
 The response should be in json and include both training_program and definitions keys for the response")
res = ra.run_errand_get_messages(ra.thread_id,ra.assistant.id,ra.instructions)
print(res)
# print(ra.assistant)

