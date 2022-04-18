#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## TDAmeritrade Profile          ##
##-------------------------------##

## Imports
from datetime import datetime

from . import urls
from .session import ClientSession
from .websocket import ClientWebSocket


## Classes
class Profile:
    """TDAmeritrade Profile"""

    # -Constructor
    def __init__(self, session: ClientSession) -> None:
        self._session: ClientSession = session

    # -Instance Methods
    async def user_principals(
        self, preferences: bool = False, streamer_keys: bool = False,
        streamer_info: bool = False, surrogate_ids: bool = False,
    ) -> None:
        '''Get user principals and additional information for profile and accounts'''
        fields: list[str] = []
        if preferences:
            fields.append("preferences")
        if streamer_keys:
            fields.append("streamerSubscriptionKeys")
        if streamer_info:
            fields.append("streamerConnectionInfo")
        if surrogate_ids:
            fields.append("surrogateIds")
        return await self._session.get(
            urls.v1.user_principals(), params={'fields': ','.join(field for field in fields)}
        )

    async def websocket(self) -> ClientWebSocket:
        '''Create and authenticate a websocket object'''
        data: dict = await self.user_principals(
            streamer_keys=True, streamer_info=True
        )
        data = await data.json()
        account: dict = data['accounts'][0]
        stream_info: dict = data['streamerInfo']
        url: str = "wss://" + stream_info['streamerSocketUrl']  + "/ws"
        websocket = await self._session.ws_connect(url)
        await websocket.login(
            stream_info['appId'], account['accountId'], stream_info['token'],
            stream_info['userGroup'], account['company'], account['segment'],
            account['accountCdDomainId'], stream_info['accessLevel'],
            datetime.strptime(stream_info['tokenTimestamp'], "%Y-%m-%dT%H:%M:%S%z"),
            stream_info['acl']
        )
        return websocket
