import logging

from werkzeug.exceptions import HTTPException as BaseHTTPException

from srm import models as m
from .response_wrapper import wrap_response

_logger = logging.getLogger('api')


class HTTPException(BaseHTTPException):
    def __init__(self, code=400, message=None, errors=None):
        super().__init__(description=message, response=None)
        self.code = code
        self.errors = errors


class BadRequestException(HTTPException):
    def __init__(self, message='Bad Request', errors=None):
        super().__init__(code=400, message=message, errors=errors)


class NotFoundException(HTTPException):
    def __init__(self, message='Resource Not Found', errors=None):
        super().__init__(code=404, message=message, errors=errors)


class UnAuthorizedException(HTTPException):
    def __init__(self, message='UnAuthorized', errors=None):
        super().__init__(code=401, message=message, errors=errors)


class ForbiddenException(HTTPException):
    def __init__(self, message='Permission Denied', errors=None):
        super().__init__(code=403, message=message, errors=errors)


def global_error_handler(e):
    '''Catch all global exception'''
    # traceback.print_exc()
    code = 500
    errors = None
    if isinstance(e, BaseHTTPException):
        code = e.code
    if isinstance(e, HTTPException):
        errors = e.errors
    res = wrap_response(None, str(e), code)

    # check for internal APIs exception
    if e.errors and isinstance(e.errors, dict) and 'internal_response' in e.errors:
        return e.errors['internal_response'], e.code

    if errors:
        res[0]['extra'] = errors
    return res
