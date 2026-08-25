from dataclasses import dataclass, field


@dataclass
class AgentState:
    contents: list = field(default_factory=list)
    iteration: int = 0
    max_iterations: int = 10