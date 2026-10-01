def create_task(title: str):
    return {
        "title": title,
        "status": "pending"
    }


def complete_task(task):
    task["status"] = "completed"
    return task