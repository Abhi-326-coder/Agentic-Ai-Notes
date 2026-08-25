import random


def random_number(minimum: int, maximum: int) -> int:
    if minimum > maximum:
        raise ValueError("minimum must be less than or equal to maximum.")

    return random.randint(minimum, maximum)
