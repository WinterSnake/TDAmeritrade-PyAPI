#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## URL Endpoints                 ##
##-------------------------------##

## Constants
base: str = "https://api.tdameritrade.com"
auth_callback: str = (
    "https://auth.tdameritrade.com/auth?response_type"
    "=code&client_id={}&redirect_uri={}"
)
