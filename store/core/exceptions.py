from fastapi import HTTPException


class BaseException(Exception):
    message: str = "Internal Server Error"

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message


class NotFoundException(BaseException):
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = "Not Found"
        super().__init__(message=message)
