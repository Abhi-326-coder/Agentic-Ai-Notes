MAX_TRANSFER = 10_000


def validate_transfer(
    user_id: str,
    amount: float
):

    if amount <= 0:
        raise ValueError(
            "Amount must be positive"
        )

    if amount > MAX_TRANSFER:
        raise PermissionError(
            "Amount exceeds limit"
        )

    if not user_is_authorized(user_id):
        raise PermissionError(
            "User is not authorized"
        )


def user_is_authorized(
    user_id: str
) -> bool:

    # Demo only
    return user_id.startswith(
        "trusted_"
    )