
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key=os.getenv("NVIDIA_API_KEY")
client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=api_key)

def get_answer(user_message):
    completion = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role":"user", "content": user_message}]

    )
    return completion.choices[0].message.content



