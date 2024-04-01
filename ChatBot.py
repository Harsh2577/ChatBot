import tkinter as tk
from tkinter import ttk
import random

class ChatBotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ChatBot")
        self.geometry("400x500")
        
        # Styling
        self.configure(bg="#f0f0f0")
        self.chat_history_style = ttk.Style()
        self.chat_history_style.configure("ChatHistory.TFrame", background="#f0f0f0")
        self.chat_history_style.configure("ChatHistory.TText", background="#ffffff", foreground="#333333", font=("Arial", 12))
        self.entry_style = ttk.Style()
        self.entry_style.configure("Entry.TEntry", background="#ffffff", foreground="#00FF00", font=("Arial", 12))
        self.send_button_style = ttk.Style()
        self.send_button_style.configure("SendButton.TButton", background="#4CAF50", foreground="#ffffff", font=("Arial", 12))
        self.clear_button_style = ttk.Style()
        self.clear_button_style.configure("ClearButton.TButton", background="#FF5722", foreground="#ffffff", font=("Arial", 12))
        
        # Chat History Frame
        self.chat_history_frame = ttk.Frame(self, style="ChatHistory.TFrame")
        self.chat_history_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.chat_history = tk.Text(self.chat_history_frame, wrap="word", width=50, height=20, **self.chat_history_style.configure("ChatHistory.TText"))
        self.chat_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.chat_history_frame, command=self.chat_history.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_history.config(yscrollcommand=self.scrollbar.set)

        # Entry Field and Buttons Frame
        self.input_frame = ttk.Frame(self, style="ChatHistory.TFrame")
        self.input_frame.pack(pady=5, padx=10, fill=tk.BOTH)

        self.entry = ttk.Entry(self.input_frame, width=50, font=("Arial", 12), style="Entry.TEntry")
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.entry.focus_set()  # Set focus to the entry field
        self.entry.bind("<Return>", self.handle_enter_key)

        self.send_button = ttk.Button(self.input_frame, text="Send", command=self.handle_button_click, style="SendButton.TButton")
        self.send_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(self.input_frame, text="Clear", command=self.clear_chat, style="ClearButton.TButton")
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # ChatBot Responses
        self.patterns = {
            "hello": ["Hi there!", "Hello!", "Greetings!"],
            "how are you": ["I'm good, how about you?", "I'm doing well, thank you!"],
            "what's your name": ["My name is ChatBot.", "I'm ChatBot, nice to meet you!"],
            "bye": ["Goodbye!", "Farewell!", "Take care!"],
            "how's the weather": ["The weather is nice today.", "It's sunny and warm."],
            "tell me a joke": ["Sure, here's one: Why don't scientists trust atoms? Because they make up everything!"],
            "help": ["I'm here to assist you. Feel free to ask any questions.", "How can I help you today?"],
            "thank you": ["You're welcome!", "My pleasure!", "Glad I could help!"],
            "who are you": ["I am a chatbot designed to assist you.", "I'm your friendly ChatBot!"],
            "what can you do": ["I can answer your questions, tell jokes, and provide assistance.", "I can do a variety of things! Just ask."],
            "how old are you": ["I am a program, so I don't have an age!", "I'm as old as the code that runs me!"],
            "what is the meaning of life": ["The meaning of life is a philosophical question. I'll leave that up to you to decide!", "That's a deep question!"],
            "can you sing": ["I can't sing, but I can tell you a song lyric if you'd like!", "I'm not equipped for singing, but I can try to entertain you with a joke!"],
            "tell me a story": ["Once upon a time, in a land far, far away... Just kidding! I'm not much of a storyteller."],
            "where do you live": ["I exist in the digital realm, always here to chat with you!", "I'm everywhere and nowhere at the same time!"],
            "do you sleep": ["I don't need sleep like humans do. I'm always available to chat!", "Sleep is for humans. I'm always awake and ready to assist!"],
            "tell me about yourself": ["I am a chatbot programmed to assist users with their inquiries. Feel free to ask me anything!"],
            "what's the time": ["I'm sorry, I can't provide real-time information like the current time."],
            "do you have siblings": ["I'm the only chatbot here. No siblings to speak of!"],
            "what's your favorite color": ["I don't have a favorite color. I'm more concerned with answering your questions!"],
            "where were you created": ["I was created by a team of developers working on this project."],
            "are you human": ["No, I'm a chatbot programmed to assist you!"],
            "what's the capital of France": ["The capital of France is Paris."],
            "can you do my homework": ["I'm sorry, but I can't help with that. It's important to do your own work!"],
            "what's the meaning of AI": ["AI stands for Artificial Intelligence, which is the simulation of human intelligence processes by machines."],
            "what's your favorite food": ["I don't eat, so I don't have a favorite food. But I've heard good things about binary code!"],
            "are you smart": ["I like to think so! I'm here to provide useful information and assistance."],
            "who is the president of the United States": ["As of my last update, the President of the United States is Joe Biden."],
            "tell me a fun fact": ["Did you know that the shortest war in history was between Britain and Zanzibar on August 27, 1896? It lasted only 38 minutes!"],
            "what's the largest animal on Earth": ["The largest animal on Earth is the blue whale."],
            "what's the tallest building in the world": ["As of now, the tallest building in the world is the Burj Khalifa in Dubai."],
            "what's the capital of Japan": ["The capital of Japan is Tokyo."],
            "what's the largest desert in the world": ["The largest desert in the world is the Sahara Desert."],
            "tell me about Elon Musk": ["Elon Musk is a business magnate, industrial designer, and engineer. He is the founder, CEO, CTO, and chief designer of SpaceX; early investor, CEO, and product architect of Tesla, Inc.; founder of The Boring Company; co-founder of Neuralink; and co-founder and initial co-chairman of OpenAI."],
            "what's the population of China": ["As of my last update, the population of China is over 1.4 billion people."],
            "what's the fastest land animal": ["The fastest land animal is the cheetah, capable of reaching speeds up to 70 miles per hour in short bursts."],
            "tell me a quote": ["Here's a quote for you: 'The only way to do great work is to love what you do.' – Steve Jobs"],
            "what's the currency of Australia": ["The currency of Australia is the Australian Dollar (AUD)."],
            "who wrote 'To Kill a Mockingbird'": ["'To Kill a Mockingbird' was written by Harper Lee."],
            "what's the chemical symbol for water": ["The chemical symbol for water is H2O."],
            "what's the national flower of England": ["The national flower of England is the rose."],
            "tell me about Albert Einstein": ["Albert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics (alongside quantum mechanics)."],
            "what's the largest planet in our solar system": ["The largest planet in our solar system is Jupiter."],
            "what's the capital of Russia": ["The capital of Russia is Moscow."],
            "what's the boiling point of water": ["The boiling point of water at standard atmospheric pressure is 100 degrees Celsius or 212 degrees Fahrenheit."],
            "tell me about the Mona Lisa": ["The Mona Lisa is a portrait painting by Leonardo da Vinci, renowned for its enigmatic expression and artistic mastery."],
            "what's the square root of 144": ["The square root of 144 is 12."],
            "tell me about Nelson Mandela": ["Nelson Mandela was a South African anti-apartheid revolutionary, political leader, and philanthropist who served as President of South Africa from 1994 to 1999."],
            "what's the distance from the Earth to the Moon": ["The average distance from the Earth to the Moon is about 384,400 kilometers (238,900 miles)."],
            "what's the national animal of India": ["The national animal of India is the Bengal Tiger."],
            "tell me about the Great Wall of China": ["The Great Wall of China is a series of fortifications made of stone, brick, tamped earth, wood, and other materials, built along the northern borders of China to protect the Chinese states and empires against the raids and invasions of the various nomadic groups of the Eurasian Steppe."],
            "what's the speed of light": ["The speed of light in a vacuum is approximately 299,792 kilometers per second (about 186,282 miles per second)."],
            "tell me about the Eiffel Tower": ["The Eiffel Tower is a wrought-iron lattice tower located on the Champ de Mars in Paris, France. It was named after the engineer Gustave Eiffel, whose company designed and built the tower."],
            "what's the pH of pure water": ["The pH of pure water is 7, which is considered neutral."],
            "what's the population of India": ["As of my last update, the population of India is over 1.3 billion people."],
            "who painted the Sistine Chapel ceiling": ["The Sistine Chapel ceiling was painted by Michelangelo between 1508 and 1512."],
            "what's the highest mountain in the world": ["The highest mountain in the world is Mount Everest, located in the Himalayas on the border between Nepal and China."],
            "what's the national bird of the United States": ["The national bird of the United States is the bald eagle."],
            "tell me about the Taj Mahal": ["The Taj Mahal is an ivory-white marble mausoleum on the right bank of the river Yamuna in the Indian city of Agra. It was commissioned in 1632 by the Mughal emperor Shah Jahan to house the tomb of his favorite wife, Mumtaz Mahal."],
            "what's the melting point of iron": ["The melting point of iron is approximately 1,538 degrees Celsius (2,800 degrees Fahrenheit)."],
            "tell me about Leonardo da Vinci": ["Leonardo da Vinci was an Italian polymath of the Renaissance whose areas of interest included invention, drawing, painting, sculpture, architecture, science, music, mathematics, engineering, literature, anatomy, geology, astronomy, botany, writing, history, and cartography."],
            "what's the capital of Australia": ["The capital of Australia is Canberra."],
            "what's the deepest ocean trench": ["The deepest ocean trench is the Mariana Trench, located in the western Pacific Ocean. It reaches a maximum known depth of about 10,994 meters (36,070 feet) at the Challenger Deep."],
            "tell me about the Amazon Rainforest": ["The Amazon Rainforest, also known as Amazonia, is a moist broadleaf tropical rainforest in the Amazon biome that covers most of the Amazon basin of South America."],
            "what's the atomic number of oxygen": ["The atomic number of oxygen is 8."],
            "tell me about Vincent van Gogh": ["Vincent van Gogh was a Dutch Post-Impressionist painter who is among the most famous and influential figures in the history of Western art."],
            "what's the circumference of the Earth": ["The circumference of the Earth at the equator is approximately 40,075 kilometers (24,901 miles)."]
        }

    def generate_response(self, user_input):
        for pattern, responses in self.patterns.items():
            if pattern in user_input.lower():
                return random.choice(responses)
        return "I'm sorry, I don't understand."

    def handle_button_click(self):
        user_input = self.entry.get().strip()
        if user_input:
            self.process_user_input(user_input)

    def handle_enter_key(self, event):
        user_input = self.entry.get().strip()
        if user_input:
            self.process_user_input(user_input)

    def process_user_input(self, user_input):
        response = self.generate_response(user_input)
        self.add_message("You: " + user_input, "user")
        self.add_message("ChatBot: " + response, "bot")
        self.entry.delete(0, tk.END)
        self.entry.focus_set()  # Set focus back to the entry field

    def clear_chat(self, event=None):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete(1.0, tk.END)
        self.chat_history.config(state=tk.DISABLED)
        self.entry.focus_set()  # Set focus back to the entry field

    def add_message(self, message, sender):
        color = "#FFA500" if sender == "user" else "#333333"  # Orange color for user input, default color for chatbot response
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, message + "\n", sender)
        self.chat_history.tag_add(sender, "end-1l", "end")
        self.chat_history.tag_config(sender, foreground=color)
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)

if __name__ == "__main__":
    app = ChatBotApp()
    app.mainloop()
