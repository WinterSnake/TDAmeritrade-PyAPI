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
auth_token: str = "/v1/oauth2/token"


## Functions
def user_principals(subscription_keys: bool = False) -> str:
    """"""
    return "/v1/userprincipals" + (
        "/streamersubscriptionkeys" if subscription_keys else ''
    )
