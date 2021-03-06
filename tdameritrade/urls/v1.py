#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## URL Endpoints [v1]            ##
##-------------------------------##

## Constants
version: str = "/v1/"
oauth2: str = f"{version}oauth2/token"
market_data: str = f"{version}marketdata/"
options: str = market_data + "chains"


## Functions
def accounts(account_id: int | None = None) -> str:
    """Account endpoints"""
    return f"{version}accounts" + ('' if account_id is None else f"/{account_id}")


def historicals(symbol: str) -> str:
    """Market historical endpoint"""
    return market_data + f"{symbol}/pricehistory"


def instruments(cusip: str | None = None) -> str:
    """Instrumental data endpoints"""
    return f"{version}/instruments" + ('' if cusip is None else f"/{cusip}")


def orders(account_id: int | None = None, order_id: int | None = None) -> str:
    """Profile + account order endpoints"""
    if account_id is None:
        return f"{version}orders"
    return accounts(account_id) + "/orders" + (
        '' if order_id is None else f"/{order_id}"
    )


def market_hours(market: str | None = None) -> str:
#-TODO: MAKE ENUM -- EQUITY, OPTION, FUTURE, BOND, FOREX
    """Market hour endpoints"""
    return market_data + ('' if market is None else f"{market}/") + "hours"


def movers(index: str) -> str:
#-TODO: MAKE ENUM -- COMPX, DJI, SPX.X
    """Market mover endpoint"""
    return market_data + index + "/movers"


def preferences(account_id: int) -> str:
    """Account preferences endpoint"""
    return accounts(account_id) + "/preferences"


def quotes(symbol: str | None = None) -> str:
    """Market quote endpoints"""
    return market_data + ('' if symbol is None else f"{symbol}/") + "quotes"


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
