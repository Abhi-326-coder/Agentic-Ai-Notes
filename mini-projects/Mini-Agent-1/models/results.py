from dataclasses import dataclass, field


@dataclass
class AgentResult:

    final_answer: str | None = None

    iterations: int = 0

    tool_calls: list = field(
        default_factory=list
    )

    observations: list = field(
        default_factory=list
    )

    success: bool = True