class ConversationMemory:
    """
    Maintains conversation memory for context preservation.
    """
    def __init__(self):
        self.memory = []

    def add(self, message):
        self.memory.append(message)

    def get(self):
        return self.memory
