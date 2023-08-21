from werkzeug.exceptions import HTTPException


class InternalServiceException(HTTPException):
    def __init__(self, message):
        self.message = "Internal Service Error: " + message
        super().__init__(self.message)
        self.code = 500
