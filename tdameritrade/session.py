#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## TDAmeritrade Session          ##
##-------------------------------##

## Imports
from collections.abc import Sequence
from datetime import (
    date, datetime, timedelta, timezone
)
from typing import Any, Type
from urllib.parse import unquote

import aiohttp
from yarl import URL

from . import urls
from .typing import (
    ExpirationDict,
    Request_AuthorizationDict, Request_OrdersDict,
    Response_AuthorizationDict
)
from .websocket import ClientWebSocket

## Constants
FORMAT_DATE: str = "%Y-%m-%d"


## Classes
class ClientSession(aiohttp.ClientSession):
    """TDAmeritrade Client Session"""

    # -Constructor
    def __init__(
        self, id_: str, callback_address: tuple[str, int],
        websocket: Type[aiohttp.ClientWebSocketResponse] = ClientWebSocket,
        **kwargs: Any
    ) -> None:
        super().__init__(
            urls.base, raise_for_status=True,
            ws_response_class=websocket, **kwargs
        )
        self.id: str = id_
        self.callback_address: tuple[str, int] = callback_address
        self.refresh_token: str = None  #type: ignore
        self.expirations: ExpirationDict = {'access': None, 'refresh': None}  #type: ignore

    # -Instance Methods: Private
    # --Internal
    def _build_url(self, url: str | URL) -> URL:
        url = URL(url)
        if self._base_url and not url.is_absolute():
            url = self._base_url.join(url)
        return url

    # --Authorization
    async def _authorize(self, auth_dict: Request_AuthorizationDict) -> None:
        '''Internal authorization handling'''
        auth_dict['client_id'] = self.authorization_id
        async with self.post(urls.v1.oauth2, data=auth_dict) as response:
            dt_utc: datetime = datetime.utcnow().replace(tzinfo=timezone.utc)
            response_dict: Response_AuthorizationDict = await response.json()
            # -Handle: Access Token
            self.headers.update({
                'AUTHORIZATION': f"Bearer {response_dict['access_token']}"
            })
            self.expirations['access'] = dt_utc + timedelta(
                seconds=response_dict['expires_in']
            )
            # -Handle: Refresh Token
            if 'refresh_token' not in response_dict:
                return
            self.refresh_token = response_dict['refresh_token']
            self.expirations['refresh'] = dt_utc + timedelta(
                seconds=response_dict['refresh_token_expires_in']
            )

    # --Accounts
    async def _account(
        self, url: str, orders: bool, positions: bool
    ) -> aiohttp.ClientResponse:
        '''Internal'''
        fields: list[str] = []
        if orders:
            fields.append("orders")
        if positions:
            fields.append("positions")
        return await self.get(
            url, params={'fields': ','.join(field for field in fields)}
        )

    # --Orders
    async def _orders(
        self, url: str, from_date: date | None, max_results: int | None,
        status: str | None, to_date: date | None
    ) -> aiohttp.ClientResponse:
        '''Internal'''
    #-TODO: MAKE 'status' ENUM
    # -- AWAITING_CONDITION, AWAITING_PARENT_ORDER, AWAITING_REVIEW, AWAITING_UR_OUT,
    # -- ACCEPTED, PENDING_ACTIVATION, QUEUED, WORKING, REJECTED, PENDING_CANCEL,
    # -- CANCELLED, PENDING_REPLACE, REPLACED, FILLED, EXPIRED
        params: Request_OrdersDict = {}
        if from_date:
            params['fromEnteredTime'] = from_date.strftime(FORMAT_DATE)
        if max_results:
            params['maxResults'] = max_results
        if status:
            params['status'] = status
        if to_date:
            params['toEnteredTime'] = to_date.strftime(FORMAT_DATE)
        return await self.get(url, params=params)

    # -Instance Methods: Public
    # --Authorization
    async def renew_tokens(self, renew_refresh_token: bool = False) -> None:
        '''Renew access (and optionally refresh) tokens'''
        auth_dict: Request_AuthorizationDict = {
            'grant_type': "refresh_token",
            'refresh_token': self.refresh_token,
        }
        if renew_refresh_token:
            auth_dict['access_type'] = "offline"
        await self._authorize(auth_dict)

    async def request_tokens(self, code: str, decode: bool = True) -> None:
        '''Request initial access + refresh tokens'''
        auth_dict: Request_AuthorizationDict = {
            'access_type': "offline",
            'code': unquote(code) if decode else code,
            'grant_type': "authorization_code",
            'redirect_uri': self.callback_url,
        }
        await self._authorize(auth_dict)

    # --Accounts
    async def get_account(
        self, account_id: int, orders: bool = False, positions: bool = False
    ) -> aiohttp.ClientResponse:
        '''Return HTTP response of account endpoint'''
        return await self._account(urls.v1.accounts(account_id), orders, positions)

    async def get_accounts(
        self, orders: bool = False, positions: bool = False
    ) -> aiohttp.ClientResponse:
        '''Return HTTP response of accounts endpoint'''
        return await self._account(urls.v1.accounts(), orders, positions)

    # --Orders
    async def cancel_order(self, account_id: int, order_id: int) -> None:
        '''Cancel order'''
        await self.delete(urls.v1.orders(account_id, order_id))

    async def get_order(self, account_id: int, order_id: int) -> aiohttp.ClientResponse:
        '''Return HTTP response of order endpoint'''
        return await self.get(urls.v1.orders(account_id, order_id))

    async def get_orders_by_path(
        self, account_id: int, from_date: date | None = None,
        max_results: int | None = None, status: str | None = None,
        to_date: date | None = None
    ) -> aiohttp.ClientResponse:
    # -TODO: MAKE 'status'  ENUM -- Check _orders method
        '''Return HTTP response of orders endpoint'''
        return await self._orders(
            urls.v1.orders(account_id), from_date, max_results, status, to_date
        )

    async def get_orders_by_query(
        self, from_date: date | None = None, max_results: int | None = None,
        status: str | None = None, to_date: date | None = None
    ) -> aiohttp.ClientResponse:
    # -TODO: MAKE 'status'  ENUM -- Check _orders method
        '''Return HTTP response of orders endpoint'''
        return await self._orders(
            urls.v1.orders(), from_date, max_results, status, to_date
        )

    async def place_order(self, account_id: int) -> aiohttp.ClientResponse:
        '''Place order and return HTTP response of order endpoint'''
        raise NotImplementedError("ClientSession.place_order")

    async def replace_order(self, account_id: int, order_id: int) -> aiohttp.ClientResponse:
        '''Replace order and return HTTP response of order endpoint'''
        raise NotImplementedError("ClientSession.replace_order")

    # --Stocks
    async def get_quote(self, symbol: str) -> aiohttp.ClientResponse:
        '''Return HTTP response of quote endpoint'''
        return await self.get(urls.v1.quotes(symbol))

    async def get_quotes(self, symbols: Sequence[str]) -> aiohttp.ClientResponse:
        '''Return HTTP response of quotes endpoint'''
        return await self.get(
            urls.v1.quotes(), params={'symbol': ','.join(symbol for symbol in symbols)}
        )

    async def get_price_history(
        self, symbol: str, frequency: tuple[str, int],
        extended_hours: bool = False, from_date: date | None = None,
        period: tuple[str, int] | None = None, to_date: date | None = None
    ) -> aiohttp.ClientResponse:
    # -TODO: MAKE 'frequency' ENUM -- MINUTE, WEEKLY, MONTHLY
    # -TODO: MAKE 'period' ENUM -- DAY, MONTH, YEAR, YEAR_TO_DATE
        '''Return HTTP response of historicals endpoint'''
        params = {
            'frequency': frequency[1],
            'frequencyType': frequency[0],
        }
        if extended_hours:
            params['needExtendedHoursData'] = extended_hours
        if from_date:
            dt = datetime(from_date.year, from_date.month, from_date.day)
            params['startDate'] = int(dt.timestamp() * 1000)
        if period:
            params['period'] = period[1]
            params['periodType'] = period[0]
        if to_date:
            dt = datetime(to_date.year, to_date.month, to_date.day)
            params['endDate'] = int(dt.timestamp() * 1000)
        return await self.get(urls.v1.historicals(symbol), params=params)

    # --User Principals/Preferences
    async def get_preferences(self, account_id: int) -> aiohttp.ClientResponse:
        '''Return HTTP response of account preferences endpoint'''
        return await self.get(urls.v1.preferences(account_id))

    async def get_streamer_keys(self, account_ids: Sequence[int]) -> aiohttp.ClientResponse:
        '''Return HTTP response of streamer keys endpoint'''
        return await self.get(
            urls.v1.user_principals(subscription_keys=True),
            params={'accountIds': ','.join(str(account_id) for account_id in account_ids)}
        )

    async def get_user_principals(
        self, preferences: bool = False, streamer_info: bool = False,
        streamer_keys: bool = False, surrogate_ids: bool = False
    ) -> aiohttp.ClientResponse:
        '''Return HTTP response of user principals endpoint'''
        fields: list[str] = []
        if preferences:
            fields.append("preferences")
        if streamer_info:
            fields.append("streamerConnectionInfo")
        if streamer_keys:
            fields.append("streamerSubscriptionKeys")
        if surrogate_ids:
            fields.append("surrogateIds")
        return await self.get(
            urls.v1.user_principals(),
            params={'fields': ','.join(field for field in fields)}
        )

    async def update_preferences(self, account_id: int) -> None:
        '''Update account preferences'''
        raise NotImplementedError("Session.update_preferences")

    # -Properties
    @property
    def authorization_id(self) -> str:
        return self.id + "@AMER.OAUTHAP"

    @property
    def authorization_url(self) -> str:
        return urls.callback(self.authorization_id, self.callback_address)

    @property
    def access_token_expiration(self) -> datetime | None:
        return self.expirations['access']

    @property
    def callback_url(self) -> str:
        return f"{self.callback_address[0]}:{self.callback_address[1]}"

    @property
    def refresh_token_expiration(self) -> datetime | None:
        return self.expirations['refresh']
