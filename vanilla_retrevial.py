from openai import OpenAI
from dotenv import load_dotenv
import time, json

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
    def __init__(self, assistant_name="Retreval Assistant", \
       instructions="You are an assistant that provides a json formatted answers to all queries. All responses must be in json format ",
       model="gpt-3.5-turbo-1106"):
       self.client = OpenAI()
       load_dotenv()       
       self.thread_id = None #updated with self.create_thread
       self.name = assistant_name
       self.instructions =   instructions
       self.model = model
       self.assistant = None
       self.file_ids = []
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
            print("Please supply a document that will be used for retrevial with this assistant")
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
        format_message = f"Provide a response to this message {user_message} as a json object that has a single key 'response' with the answer"
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
            # json.load(clean_message)

            return {"response": str(clean_message)}
        except Exception as e:
            print(str(e))
    
    def update_system_prompt(self):
        schema = {
            "{response": "OPEN AI ASSISTANT TEXT RESPONSE}"
        }

        val = f"{self.instructions} by formatting the response in the following schema {json.dumps(schema)}."
        self.instructions = val



        

#upload files 
#create assistant 
#create thread 
#create message 
#get response 

file_name_a = "Defender.pdf"
file_name_b = "Goalkeeper.pdf"
file_name_c = "Midfielder.pdf"
file_name_d = "Striker.pdf"
file_name_e = "Winger.pdf"



ra = Retrieval_Assistant()

ra.update_system_prompt()

ra.upload_file(file_name_a)
time.sleep(3)
ra.upload_file(file_name_b)
time.sleep(3)
ra.upload_file(file_name_c)
time.sleep(3)
ra.upload_file(file_name_d)
time.sleep(3)
ra.upload_file(file_name_e)
time.sleep(3)



ra.create_assistant_on_init()
ra.create_thread()
ra.create_message_in_tread("Give 10 facts about the position")
res = ra.run_errand_get_messages(ra.thread_id,ra.assistant.id,ra.instructions)
print(res)
# print(ra.assistant)

