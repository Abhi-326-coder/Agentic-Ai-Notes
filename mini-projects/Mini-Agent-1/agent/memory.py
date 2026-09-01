class ConversationMemory:

    def __init__(self):
        self.contents = []

    def add(self, content):
        self.contents.append(content)

    def clear(self):
        """Remove all saved conversation messages."""
        self.contents.clear()

    def get_contents(self):
        return self.contents
