import openai
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def send_gptprompt(prompt,tokens=15,temperature=0,model="text-davinci-003"):
    text = openai.Completion.create(
      model=model,
      prompt=str(prompt),
      max_tokens=tokens,
      temperature=temperature
    )

    # I want specifically to remove the '\n\n' at the beginning of the response hence the [2:]
    return text['choices'][0]['text'][2:]