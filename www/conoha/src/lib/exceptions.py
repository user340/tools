#!/usr/bin/env python


class Error(Exception):
    """Base class for exceptions in this module.
    """
    pass


class BadStatusCodeError(Error):
    """Called when returned HTTP status code is bad.
    """
    def __init__(self, message):
        self.message = message


class BadRequestError(Error):
    """Called when returned HTTP status code is 400.
    """
    def __init__(self, message):
        self.message = message


class ConflictingRequestError(Error):
    """Called when HTTP status code is 409.
    """
    def __init__(self, message):
        self.message = message


class JsonDecodeError(Error):
    """Called when faled decode response body. It used for requests module.
    """
    def __init__(self):
        self.message = 'Decode response body was failed'


class InvalidArgumentError(Error):
    """Called when unexpected/invalid arguments are given.
    """
    def __init__(self, message):
        self.message = message


class NothingFlavorIDError(Error):
    """Called when flavor_id is None.
    """
    def __init__(self, message):
        self.message = message


class NothingServerIDError(Error):
    """Called when server_id is None.
    """
    def __init__(self, message):
        self.message = message


class ServerNotFoundError(Error):
    """Mostly, It called when HTTP status code is 404.
    """
    def __init__(self, message):
        self.message = message


class UnexceptedServerStatusError(Error):
    """Called when returned unexcepted server status
    """
    def __init__(self, message):
        self.message = message
