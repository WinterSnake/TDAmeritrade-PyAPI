#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## URL Endpoints [v1]            ##
##-------------------------------##

## Imports
from . import v1

## Constants
base: str = "https://api.tdameritrade.com"
callback: str = (
    "https://auth.tdameritrade.com/auth?response_type"
    "=code&client_id={}&redirect_uri={}"
)
__all__ = (
    v1, base, callback
)
