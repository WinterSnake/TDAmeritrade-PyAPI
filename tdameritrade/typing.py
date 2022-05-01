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
    """Internal timestamp expiration structure"""
    access: datetime
    refresh: datetime


class Request_AuthorizationDict(TypedDict, total=False):
    """Internal session authorization request structure"""
    access_type: str
    client_id: str  # REQUIRED
    code: str
    grant_type: str  # REQUIRED
    refresh_token: str
    redirect_uri: str


class Request_OrdersDict(TypedDict, total=False):
    """Internal order request structure"""
    fromEnteredTime: str
    maxResults: int
    status: str
    toEnteredTime: str


class Request_WebSocketDict(TypedDict):
    """WebSocket message request structure"""
    account: str
    command: str
    parameters: dict[str, Any]
    requestid: int
    service: str
    source: int


class Response_AuthorizationDict(TypedDict):
    """Internal session authorization response structure"""
    access_token: str
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
    scope: str
    token_type: str
