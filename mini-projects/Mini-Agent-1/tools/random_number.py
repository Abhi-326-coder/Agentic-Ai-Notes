import random


def random_number(minimum: int, maximum: int) -> int:

    if minimum > maximum:
        raise ValueError(
            "minimum cannot be greater than maximum."
        )

    return random.randint(
        minimum,
        maximum
    )