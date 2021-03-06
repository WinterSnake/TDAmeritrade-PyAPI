#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## TDAmeritrade Profile          ##
##-------------------------------##

## Imports
from datetime import datetime
from typing import cast

import aiohttp

from . import urls
from .session import ClientSession
from .websocket import ClientWebSocket


## Classes
class Profile:
    """TDAmeritrade Profile"""

    # -Constructor
    def __init__(self, session: ClientSession) -> None:
        assert(issubclass(session._ws_response_class, ClientWebSocket))
        self._session: ClientSession = session

    # -Instance Methods
    async def create_websocket(self, quality_of_service: int = 2) -> ClientWebSocket:
        '''Create and authenticate a websocket object'''
        response: aiohttp.ClientResponse = await self._session.get_user_principals(
            streamer_keys=True, streamer_info=True
        )
        data: dict = await response.json()
        account: dict = data['accounts'][0]
        stream_info: dict = data['streamerInfo']
        url: str = "wss://" + stream_info['streamerSocketUrl']  + "/ws"
        websocket: ClientWebSocket = cast(ClientWebSocket, await self._session.ws_connect(url))
        assert isinstance(websocket, ClientWebSocket)
        await websocket.login(
            stream_info['appId'], account['accountId'], stream_info['token'],
            account['company'], account['segment'], account['accountCdDomainId'],
            stream_info['userGroup'], stream_info['accessLevel'],
            datetime.strptime(stream_info['tokenTimestamp'], "%Y-%m-%dT%H:%M:%S%z"),
            stream_info['acl'], quality_of_service
        )
        return websocket
