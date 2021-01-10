from flask import flash

class ApplicationError(Exception):

    def __init__(self, message, status_code):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return { "message": self.message }


def __handle_error(error):
    flash(error.message, "error")
    #TODO ???
    return ""


def register_error_handlers(app):
    app.register_error_handler(ApplicationError, __handle_error)
