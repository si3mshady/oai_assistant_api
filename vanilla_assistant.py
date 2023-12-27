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
        self.instructions = self.update_system_prompt()
        self.model = model
        self.assistant = self.create_assistant_on_init()
    
    def update_system_prompt(self):
        schema = {
        "workout_plan_name":"Beginner Workout",
        "goal":"Weight Loss",
        "workouts":[{
            "name":"Dumbell Curls",
            "sets":3,
            "repetitions":3,
            "rest":"20",
            "rest_unit":"minutes",
            "difficulty":"easy",
            "body_part_focus":"chest",
            "equipments_needed":["Dumbell", "Bench"],
            "excercise_category":"Muscle Gain"
        },{}]}

        val = f"{self.instructions} in the format {json.dumps(schema)}"

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


       
        