from guardrails.input import validate_input
from guardrails.tools import validate_transfer

# this Below explains the workflow not actual code but is a pseudo code

def process_request(
    user_id: str,
    message: str
):

    # ----------------------
    # INPUT GUARDRAIL
    # ----------------------

    valid, reason = validate_input(
        message
    )

    if not valid:
        return {
            "status": "blocked",
            "reason": reason
        }

    # ----------------------
    # AGENT
    # ----------------------

    response = run_agent(
        message
    )

    # ----------------------
    # TOOL GUARDRAIL
    # ----------------------

    if response.tool == "transfer_money":

        validate_transfer(
            user_id,
            response.amount
        )

        return execute_transfer(
            response.amount
        )

    # ----------------------
    # OUTPUT
    # ----------------------

    return response