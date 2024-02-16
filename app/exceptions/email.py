class BadResponse(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ImapConnectionFailed(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
