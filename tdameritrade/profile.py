#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## TDAmeritrade Profile          ##
##-------------------------------##

## Imports
from .session import ClientSession
from .websocket import ClientWebSocket


## Classes
class Profile:
    """TDAmeritrade Profile"""

    # -Constructor
    def __init__(self, session: ClientSession) -> None:
        self._session: ClientSession = session
