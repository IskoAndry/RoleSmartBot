import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


async def get_response(prompt: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=prompt, max_tokens=200
    )
    return response.choices[0].text.strip()
