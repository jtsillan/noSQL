class ValidationError(Exception):
    def __init__(self, message="Validation error"):
        self.args = (message,)