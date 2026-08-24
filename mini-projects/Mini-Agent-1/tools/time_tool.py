from datetime import datetime


def get_current_time() -> str:
    """
    Return the current local date and time.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")