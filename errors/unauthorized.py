class Unauthorized(Exception):
    def __init__(self, message='Unauthorized'):
        self.args = (message,)