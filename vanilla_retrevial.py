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