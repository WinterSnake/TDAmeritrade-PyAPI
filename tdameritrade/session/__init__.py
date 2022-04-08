#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## TDAmeritrade Session          ##
##-------------------------------##

## Imports
from datetime import datetime, timedelta, timezone
from typing import TypedDict
from urllib.parse import quote, unquote

import aiohttp

from . import urls

## Constants
AuthorizationDict = TypedDict(
    "AuthorizationDict", {
        'access_type': str, 'code': str, 'client_id': str,
        'grant_type': str, 'redirect_uri': str, 'refresh_token': str,
    }, total=False
)
ExpirationDict = TypedDict(
    "ExpirationDict", {'access': datetime | None, 'refresh': datetime | None}
)


## Classes
class ClientSession(aiohttp.ClientSession):
    """TDAmeritrade Client Session"""

    # -Constructor
    def __init__(
        self, id_: str, callback_url: tuple[str, int], *args, **kwargs
    ) -> None:
        super().__init__(base_url=urls.base, raise_for_status=True,  *args, **kwargs)
        self.id: str = id_
        self._callback_url: tuple[str, int] = callback_url
        self.refresh_token: str | None = None
        self.expirations: ExpirationDict = {
            'access': None, 'refresh': None
        }

    # -Instance Methods: Private
    async def _authorize(self, dict_: AuthorizationDict) -> None:
        '''Update TDA Session authorization properties'''
        dict_['client_id'] = self.authorization_id
        async with self.post(urls.auth_token, data=dict_) as res:
            dt_utc = datetime.utcnow().replace(tzinfo=timezone.utc)
            res_dict: dict[str, str] = await res.json()
            # -Handle access token properties
            self.headers.update({
                'AUTHORIZATION': "Bearer " + res_dict['access_token']
            })
            self.expirations['access'] = dt_utc + timedelta(
                seconds=res_dict['expires_in']
            )
            if 'refresh_token' not in res_dict:
                return
            # -Handle refresh token properties
            self.refresh_token = res_dict['refresh_token']
            self.expirations['refresh'] = dt_utc + timedelta(
                seconds=res_dict['refresh_token_expires_in']
            )

    # -Instance Methods: Public
    async def renew_tokens(self, renew_refresh_token: bool = False) -> None:
        '''Renew access + refresh tokens for TDA Session'''
        auth_dict: AuthorizaionDict = {
            'grant_type': "refresh_token",
            'refresh_token': self.refresh_token,
        }
        if renew_refresh_token:
            auth_dict['access_type'] = "offline"
        await self._authorize(auth_dict)

    async def request_tokens(self, code: str, decode: bool = True) -> None:
        '''Request initial access + refresh tokens for TDA Session'''
        auth_dict: AuthorizationDict = {
            'grant_type': "authorization_code",
            'access_type': "offline",
            'redirect_uri': self.callback_url,
            'code': unquote(code) if decode else code,
        }
        await self._authorize(auth_dict)

    # -Properties
    @property
    def authorization_id(self) -> str:
        return self.id + "@AMER.OAUTHAP"

    @property
    def authorization_url(self) -> str:
        return urls.auth_callback.format(
            quote(self.authorization_id), quote(self.callback_url)
        )

    @property
    def callback_url(self) -> str:
        return self._callback_url[0] + ':' + str(self._callback_url[1])

    @property
    def access_token_expiration(self) -> datetime | None:
        return self.expirations['access']

    @property
    def refresh_token_expiration(self) -> datetime | None:
        return self.expirations['refresh']
