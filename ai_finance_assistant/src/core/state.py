class ConversationState:
    """
    Maintains conversation/session state for context preservation.
    """
    def __init__(self):
        self.history = []
        self.user_profile = {}

    def add_message(self, message: dict):
        self.history.append(message)

    def get_history(self):
        return self.history

    def set_user_profile(self, profile: dict):
        self.user_profile = profile

    def get_user_profile(self):
        return self.user_profile
