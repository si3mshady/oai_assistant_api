from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()


#make agent 
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

class Retreval_Assistant:
    def __init__(self, assistant_name="Retreval Assistant", \
       instructions="You are a customer support chatbot. Use your knowledge base to best respond to customer queries.",\
       model="gpt-3.5-turbo"):
       load_dotenv()
       self.client = OpenAI()
       self.thread_id = None #updated with self.create_thread
       self.name = assistant_name
       self.instructions =   instructions
       self.model = model
       self.assistant = self.create_assistant_on_init()
    
    def upload_file(self, file_path):
        file = client.files.create( file=open(file_path, "rb"),  purpose='assistants')
        print('file uploaded')

    def create_assistant_on_init(self):
    
        kwargs = {"name": self.name, "instructions": self.instructions, "model": self.model}
        try:
            assistant = self.client.beta.assistants.create(**kwargs)
            self.assistant =  assistant           
            print("New assistant created " + self.assistant.id)
            return self.assistant

        except Exception as e:
            print(str(e))
            return str(e)



