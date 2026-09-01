from agent.llm import GeminiLLM
from agent.loop import run_agent
from agent.memory import ConversationMemory
from agent.state import AgentState
from tools.manager import ToolManager
from google.genai import types
from models.results import AgentResult


class Agent:

    def __init__(
        self,
        llm=None,
        max_iterations: int = 10
    ):

        self.llm = llm or GeminiLLM()

        self.tool_manager = ToolManager()

        self.max_iterations = max_iterations

        self.memory = ConversationMemory()

        self.state = None

    def run(self, user_message: str) -> str:

        state = AgentState(
            max_iterations=self.max_iterations,
            contents=list(
                self.memory.get_contents()
            )
        )
        
        self.tools = self.tool_manager.get_definitions()

        self.state = state

        user_content = types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=user_message
                )
            ],
        )

        state.contents.append(user_content)

        answer = run_agent(
            state,
            self.tools,
            self.llm,
            self.tool_manager,
        )

        state.final_answer = answer

        self.memory.contents = state.contents

        return AgentResult(
            final_answer=answer,
            iterations=state.iteration,
            tool_calls=state.tool_calls,
            observations=state.observations,
            success=True,
        )
    
    def get_state(self):
        return self.state
