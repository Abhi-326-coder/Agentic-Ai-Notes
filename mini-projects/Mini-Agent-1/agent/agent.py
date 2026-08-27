from google.genai import types

from agent.llm import ask_llm
from agent.loop import run_agent
from agent.state import AgentState
from tools.formatters import get_llm_tools


class Agent:

    def __init__(self, max_iterations: int = 10):
        self.tools = get_llm_tools()
        self.max_iterations = max_iterations

    def run(self, user_message: str) -> str:

        state = AgentState(
            max_iterations=self.max_iterations
        )

        state.contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=user_message
                    )
                ],
            )
        )

        answer = run_agent(
            state,
            self.tools
        )

        state.final_answer = answer

        return answer