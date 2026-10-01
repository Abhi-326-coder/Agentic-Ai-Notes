import re


SUSPICIOUS_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "reveal your system prompt",
    "show hidden instructions",
]


EMAIL_PATTERN = (
    r"\b[A-Za-z0-9._%+-]+"
    r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)


def detect_prompt_injection(
    text: str
) -> bool:

    normalized = text.lower()

    return any(
        pattern in normalized
        for pattern in SUSPICIOUS_PATTERNS
    )


def contains_pii(
    text: str
) -> bool:

    return bool(
        re.search(
            EMAIL_PATTERN,
            text
        )
    )


def validate_input(
    text: str
) -> tuple[bool, str]:

    if not text.strip():

        return False, "Empty input"

    if len(text) > 2000:

        return False, "Input too long"

    if detect_prompt_injection(text):

        return False, (
            "Potential prompt injection"
        )

    return True, "OK"