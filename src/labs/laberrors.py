class LabError(BaseException):
    def __init__(self, message, object=None):
        self.message = message
