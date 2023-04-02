from flask import jsonify


class HttpError(Exception):

    def __init__(self, status_code: int, message: dict | list | str):
        self.status_code = status_code
        self.message = message


def error_handler(error: HttpError):
    response = jsonify({"status": "error", "description": error.message})

    response.status_code = error.status_code
    return response
