import random

def get_answer(unser_message):
    answers = ["Hello!", 
               "Please repeat slowly.", 
               "How can I help you?",
               "Hmmm...",
               "Good to see you!"
               ]
    return random.choice(answers)