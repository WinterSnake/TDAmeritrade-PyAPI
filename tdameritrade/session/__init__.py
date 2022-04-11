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
from urllib.parse import quote, unquote, urlencode

import aiohttp
from yarl import URL

from . import urls
from .websocket import ClientWebSocket

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
        super().__init__(
            base_url=urls.base, raise_for_status=True,
            ws_response_class=ClientWebSocket, *args, **kwargs
        )
        self.id: str = id_
        self.refresh_token: str | None = None
        self.expirations: ExpirationDict = {
            'access': None, 'refresh': None
        }
        self._callback_url: tuple[str, int] = callback_url

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

    def _build_url(self, url: str | URL) -> URL:
        url = URL(url)
        if self._base_url and not url.is_absolute():
            url = self._base_url.join(url)
        return url

    # -Instance Methods: Public
    async def ws_connect(self) -> ClientWebSocket:
        async with self.get(
            urls.user_principals(), params={
                'fields': ["streamerConnectionInfo", "streamerSubscriptionKeys"]
            }
        ) as response:
            dict_ = await response.json()
            account: dict = dict_['accounts'][0]
            account_id: int = account['accountId']
            streamer_info: dict = dict_['streamerInfo']
            app_id: str = streamer_info['appId']
            token: str = streamer_info['token']
            url: str = "wss://" + streamer_info['streamerSocketUrl'] + "/ws"
            credentials = {
                'userid': account_id,
                'token': token,
                'company': account['company'],
                'segment': account['segment'],
                'cddomain': account['accountCdDomainId'],
                'usergroup': streamer_info['userGroup'],
                'accesslevel': streamer_info['accessLevel'],
                'authorized': "Y",
                'timestamp': int(datetime.strptime(
                    streamer_info['tokenTimestamp'], "%Y-%m-%dT%H:%M:%S%z"
                ).timestamp() * 1000),
                'appid': app_id,
                'acl': streamer_info['acl'],
            }
            websocket = await self._ws_connect(url)
            websocket.app_id = app_id
            websocket.account_id = account_id
            await websocket.send_message(
                "ADMIN", "LOGIN", token=token, version="1.0",
                credential=urlencode(credentials)
            )
            return websocket

    async def renew_tokens(self, renew_refresh_token: bool = False) -> None:
        '''Renew access + refresh tokens for TDA Session'''
        auth_dict: AuthorizationDict = {
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