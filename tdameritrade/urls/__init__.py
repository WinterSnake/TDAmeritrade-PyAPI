#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## URL Endpoints [v1]            ##
##-------------------------------##

## Imports
from . import v1
from urllib.parse import quote

## Constants
__all__ = (
    "base", "callback", "v1"
)
base: str = "https://api.tdameritrade.com"


## Functions
def callback(id_: str, callback_address: tuple[str, int]) -> str:
    """Callback authorization endpoint"""
    address: str = f"{callback_address[0]}:{callback_address[1]}"
    return (
        "https://auth.tdameritrade.com/auth?response_type"
        f"=code&client_id={quote(id_)}&redirect_uri={quote(address)}"
    )
