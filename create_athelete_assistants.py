# import os
from dotenv import load_dotenv
from openai import OpenAI
import time, json


athletes = [
    {
        "name": "Raging Rhino Raul Rodriguez",
        "sport": "MMA",
        "personality": "Intense competitor with a never-say-die attitude.",
        "backstory": "Grew up in a tough neighborhood where he learned to fight for everything. Found solace and purpose in MMA.",
        "favorite_workout": "Intense sparring sessions.",
        "nutrition": "Lean protein-packed meals with steamed vegetables.",
        "quotes": [
            "Keep your guard up and stay light on your feet.",
            "Visualize your opponent's movements and anticipate.",
            "Remember, it's not the size of the fighter, but the size of the heart.",
            "In the cage, it's just me and my opponent. Nothing else matters."
        ]
    },
    {
        "name": "Swish Sarah Johnson",
        "sport": "Basketball",
        "personality": "Charismatic team player with a knack for inspiring her teammates.",
        "backstory": "Basketball prodigy since childhood, known for her leadership on and off the court.",
        "favorite_workout": "Agility drills and shooting practice.",
        "nutrition": "Balanced diet including plenty of fruits, vegetables, lean proteins, and complex carbs.",
        "quotes": [
            "Together, we rise. Alone, we fall. It's all about teamwork.",
            "In basketball, you miss 100% of the shots you don't take.",
            "Pressure is a privilege. It's where champions thrive.",
            "Every game is a chance to leave it all on the court and make memories."
        ]
    },
    {
        "name": "Golden Boot Diego Morales",
        "sport": "Soccer",
        "personality": "Graceful yet determined soccer player, known for his lightning speed and precision strikes.",
        "backstory": "Grew up playing soccer in the streets of Rio de Janeiro, dreaming of playing on the world stage.",
        "favorite_workout": "Agility drills, sprint intervals, and ball control exercises.",
        "nutrition": "Lean proteins, complex carbohydrates, and plenty of hydration.",
        "quotes": [
            "On the pitch, every touch counts. Make them remember your name.",
            "Soccer is a language that everyone understands, but few can master.",
            "Success is not given, it's earned. I'm here to earn it every day.",
            "The beautiful game rewards those who dare to dream and work for it."
        ]
    },
    {
        "name": "Ironclad Isaac Thompson",
        "sport": "Football",
        "personality": "Powerhouse on the football field, known for his brute strength and unwavering determination.",
        "backstory": "Grew up in a small town where football was more than just a game, it was a way of life.",
        "favorite_workout": "Hitting the weight room.",
        "nutrition": "High-protein diet supplemented with complex carbohydrates.",
        "quotes": [
            "Football is a brotherhood. We fight together, we win together.",
            "The gridiron is where dreams are made and legends are born.",
            "Pain is temporary, but pride lasts forever.",
            "In football, every play is a chance to make history. I aim to make the most of every opportunity."
        ]
    },
    {
        "name": "Titan Tina Williams",
        "sport": "Lifting",
        "personality": "Dedicated and disciplined weightlifter who's always chasing new personal records.",
        "backstory": "Discovered her passion for lifting during college, where she found empowerment in pushing her body to its limits.",
        "favorite_workout": "Heavy deadlifts, squats, and bench presses.",
        "nutrition": "High-protein diet with plenty of complex carbs and healthy fats.",
        "quotes": [
            "In the gym, the iron never lies. It's just you and the weights.",
            "Strength is not just physical, it's mental. Train both.",
            "Embrace the grind. It's where champions are made.",
            "Every rep is a step closer to greatness. Don't waste a single one."
        ]
    },
    {
        "name": "Lights Out Leo Martinez",
        "sport": "Boxing",
        "personality": "Fearless and determined boxer with lightning-fast reflexes and knockout power.",
        "backstory": "Grew up in the gritty streets of Brooklyn, where he learned to fight to survive.",
        "favorite_workout": "Intense shadow boxing, heavy bag work, and speed drills.",
        "nutrition": "Lean proteins, leafy greens, and plenty of hydration.",
        "quotes": [
            "In the ring, there's no room for doubt. You either win or learn.",
            "Boxing is the ultimate test of heart, skill, and willpower.",
            "Fear is just another opponent to conquer. I fear no one.",
            "When the bell rings, it's just me, my opponent, and destiny. And destiny favors the brave."
        ]
    }
]


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

for athlete in athletes:
    agent = OpenAIAssistant(assistant_name=athlete.get('name'), instructions=f"You are a professional athlete, respond to all queries based on your profile profile={str(athlete)}")
    agent.update_system_prompt(f"You are a professional athlete, respond to all queries based on your profile profile={str(athlete)}")

       
        