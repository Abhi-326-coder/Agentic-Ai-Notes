from dataclasses import dataclass, field


@dataclass
class AgentState:
    # Information sent to Gemini
    contents: list = field(default_factory=list)

    # Agent execution information
    iteration: int = 0
    max_iterations: int = 10

    # Tool execution information
    tool_calls: list = field(default_factory=list)
    observations: list = field(default_factory=list)

    # Final result
    final_answer: str | None = None