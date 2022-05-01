#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Hinting Utils            ##
##-------------------------------##

## Imports
from datetime import datetime
from typing import Any, TypedDict


## Classes
class ExpirationDict(TypedDict):
    """Session expiration timestamp structure"""
    access: datetime | None
    refresh: datetime | None


class Request_AuthorizationDict(TypedDict, total=False):
    """Session internal authorization structure"""
    access_type: str
    client_id: str  # REQUIRED
    code: str
    grant_type: str  # REQUIRED
    refresh_token: str
    redirect_uri: str


class Request_OrdersDict(TypedDict):
    """Session expiration timestamp structure"""
    fromEnteredTime: str
    maxResults: str
    status: str
    toEnteredTime: str


class Request_WebSocketDict(TypedDict):
    """WebSocket request message structure"""
    account: str
    command: str
    parameters: dict[str, Any]
    requestid: int
    service: str
    source: int
