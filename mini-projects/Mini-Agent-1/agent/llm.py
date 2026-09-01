import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from agent.llm_base import LLM


load_dotenv()


class GeminiLLM(LLM):

    def __init__(
        self,
        model: str = "gemini-2.5-flash"
    ):

        self.model = model

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def generate(
        self,
        contents,
        tools
    ):

        return self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        function_declarations=tools
                    )
                ]
            ),
        )