import requests
from groq import Groq

GROQ_API_KEY = ""

def all_models():

    api_key = GROQ_API_KEY
    url = "https://api.groq.com/openai/v1/models"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def ask_model(prompt , model="llama-3.1-70b-versatile"):
    client = Groq(api_key=GROQ_API_KEY)
    message = [
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": "",
        }
    ]
    message[-1]['content'] = prompt

    completion = client.chat.completions.create(
        model=model,
        messages=message,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return completion.choices[-1].message.content
