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
class AuthorizationDict(TypedDict, total=False):
    """Session internal authorization structure"""
    access_type: str
    client_id: str  # -required
    code: str
    grant_type: str  # -required
    refresh_token: str
    redirect_uri: str


class ExpirationDict(TypedDict):
    """Session expiration timestamp structure"""
    access: datetime | None
    refresh: datetime | None


class RequestDict(TypedDict):
    """WebSocket request message structure"""
    account: str
    command: str
    parameters: dict[str, Any]
    requestid: int
    service: str
    source: int
