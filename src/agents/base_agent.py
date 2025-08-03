class BaseAgent:
    """
    Base class for all financial assistant agents.
    Provides common interface and shared utilities.
    """
    def __init__(self, name: str):
        self.name = name

    def process(self, query: str, context: dict = None) -> dict:
        """
        Main method to process user queries.
        Should be overridden by subclasses.
        """
        raise NotImplementedError("process() must be implemented by agent subclasses.")
