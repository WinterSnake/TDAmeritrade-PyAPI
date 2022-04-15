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
    return f"{version}accounts" + ('' if id_ is None else f"/{id_}")


def orders(account_id: int | None = None, order_id: int | None = None) -> str:
    """Profile + account order endpoints"""
    if account_id is None:
        return f"{version}orders"
    return accounts(account_id) + "/orders" + (
        '' if order_id is None else f"/{order_id}"
    )


def preferences(id_: int) -> str:
    """Account preferences endpoint"""
    return accounts(id_) + "/preferences"


def saved_orders(account_id: int, saved_order_id: int | None = None) -> str:
    """Account saved order endpoints"""
    return accounts(account_id) + "/savedorders" + (
        '' if saved_order_id is None else f"/{saved_order_id}"
    )


def transactions(account_id: int, transaction_id: int | None = None) -> str:
    """Account transaction endpoints"""
    return accounts(account_id) + "/transactions" + (
        '' if transaction_id is None else f"/{transaction_id}"
    )


def user_principals(subscription_keys: bool = False) -> str:
    """Session user principal + subscription endpoints"""
    return f"{version}userprincipals" + (
        "/streamersubscriptionkeys" if subscription_keys else ''
    )


def watchlists(account_id: int | None = None, watchlist_id: int | None = None) -> str:
    """Profile + account watchlist endpoints"""
    if account_id is None:
        return accounts() + "/watchlists"
    return accounts(account_id) + "/watchlists" + (
        '' if watchlist_id is None else f"/{watchlist_id}"
    )
