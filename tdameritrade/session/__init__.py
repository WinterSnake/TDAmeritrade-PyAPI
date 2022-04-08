#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## TDAmeritrade Session          ##
##-------------------------------##

## Imports
from datetime import datetime
from typing import TypedDict
from urllib.parse import quote

import aiohttp

from . import urls

## Constants
ExpirationDict = TypedDict(
    "ExpirationDict", {'access': datetime | None, 'refresh': datetime | None}
)


## Classes
class ClientSession(aiohttp.ClientSession):
    """TDAmeritrade Client Session"""

    # -Constructor
    def __init__(
        self, id_: str, callback_url: tuple[str, int],
        *args, refresh_token: str | None = None,
        refresh_token_expiration: datetime | None = None, **kwargs
    ) -> None:
        super().__init__(base_url=urls.base,*args, **kwargs)
        self.id: str = id_
        self._callback_url: tuple[str, int] = callback_url
        self.refresh_token: str | None = refresh_token
        self.expirations: ExpirationDict = {
            'access': None, 'refresh': refresh_token_expiration
        }

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
