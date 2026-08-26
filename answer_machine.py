
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key=os.getenv("NVIDIA_API_KEY")
client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=api_key)
# Das LLM selbst durchsucht dein Dokument nicht. 
# Unser eigener Retrieval-Code sucht zuerst den relevanten Inhalt. 
# Das LLM bekommt anschließend nur den gefundenen Kontext und soll daraus die Antwort formulieren.


def get_answer(user_message, context):
    completion = client.chat.completions.create(
        model="meta/llama-3.3-70b-instruct",
    messages=[
    {
        "role": "user",
        "content": f"""
Beantworte die Frage ausschließlich anhand des folgenden Kontexts.

Kontext:
{context}

Frage:
{user_message}

Wenn die Antwort nicht im Kontext steht, sage:
"Ich kann diese Frage anhand des Dokuments nicht beantworten."
"""}
]
    )
    return completion.choices[0].message.content



