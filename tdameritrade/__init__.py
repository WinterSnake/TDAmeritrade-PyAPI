#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
from .profile import Profile
from .session import ClientSession
from .websocket import ClientWebSocket

## Constants
__author__ = "Ryan Smith"
__title__ = "TDAmeritrade PyAPI"
__version__ = (1, 0, 0)
__all__ = (
    "ClientSession", "ClientWebSocket", "Profile"
)


## Functions
def get_version_string() -> str:
    """Project version as a string"""
    return '.'.join(str(i) for i in __version__)
