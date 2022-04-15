#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## URL Endpoints [v1]            ##
##-------------------------------##

## Constants
version: str = "/v1/"
auth: str = f"{version}oauth2/token"


## Functions
def accounts(id_: int | None = None) -> str:
    """Account endpoints"""
    return f"{version}accounts" + (f"/{id_}" if id_ else '')


def preferences(id_: int) -> str:
    """Account preferences endpoint"""
    return accounts(id_) + "/preferences"


def user_principals(subscription_keys: bool = False) -> str:
    """Session user principal + subscription endpoints"""
    return f"{version}userprincipals" + (
        "/streamersubscriptionkeys" if subscription_keys else ''
    )
