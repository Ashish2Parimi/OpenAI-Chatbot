from werkzeug.exceptions import HTTPException


class BadRequest(HTTPException):
    def __init__(self, message):
        self.message = "Bad Request: " + message
        super().__init__(self.message)
        self.code = 400
