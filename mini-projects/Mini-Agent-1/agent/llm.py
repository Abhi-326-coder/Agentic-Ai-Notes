import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()



def ask_llm(contents, tool):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to your .env file before running the agent."
        )

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=contents,
        config=types.GenerateContentConfig(
            tools=[tool]
        ),
    )

    return response
