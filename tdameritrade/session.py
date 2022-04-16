#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## TDAmeritrade Session          ##
##-------------------------------##

## Imports
from datetime import datetime, timedelta, timezone
from urllib.parse import unquote

import aiohttp
from yarl import URL

from . import urls
from .typing import AuthorizationDict, ExpirationDict
from .websocket import ClientWebSocket


## Classes
class ClientSession(aiohttp.ClientSession):
    """TDAmeritrade Client Session"""

    # -Constructor
    def __init__(
        self, id_: str, callback_address: tuple[str, int], *args, **kwargs
    ) -> None:
        if 'ws_response_class' not in kwargs:
            kwargs['ws_response_class'] = ClientWebSocket
        super().__init__(
            base_url=urls.base, raise_for_status=True, *args, **kwargs
        )
        self.id: str = id_
        self.callback_address: tuple[str, int] = callback_address
        self.refresh_token: str | None = None
        self.expirations: ExpirationDict = {'access': None, 'refresh': None}

    # -Instance Methods: Private
    async def _authorize(self, auth_dict: AuthorizationDict) -> None:
        '''Internal authorization handling'''
        auth_dict['client_id'] = self.authorization_id
        async with self.post(urls.v1.oauth2, data=auth_dict) as response:
            dt_utc: datetime = datetime.utcnow().replace(tzinfo=timezone.utc)
            response_dict: dict = await response.json()
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

    # -Instance Methods: Public
    async def renew_tokens(self, renew_refresh_token: bool = False) -> None:
        '''Renew access (and optionally refresh) tokens'''
        auth_dict: AuthorizationDict = {
            'grant_type': "refresh_token",
            'refresh_token': self.refresh_token,
        }
        if renew_refresh_token:
            auth_dict['access_type'] = "offline"
        await self._authorize(auth_dict)

    async def request_tokens(self, code: str, decode: bool = True) -> None:
        '''Request initial access + refresh tokens'''
        auth_dict: AuthorizationDict = {
            'access_type': "offline",
            'code': unquote(code) if decode else code,
            'grant_type': "authorization_code",
            'redirect_uri': self.callback_url,
        }
        await self._authorize(auth_dict)

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
