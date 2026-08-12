class AuthExpiredException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TrueLayerError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
