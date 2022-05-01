#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## TDAmeritrade Websocket        ##
##-------------------------------##

## Imports
from datetime import datetime
from urllib.parse import urlencode

import aiohttp

from .typing import Request_WebSocketDict


## Classes
class ClientWebSocket(aiohttp.ClientWebSocketResponse):
    """TDAmeritrade Client WebSocket"""

    # -Constructor
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.id: str | None = None
        self.source: int | None = None
        self.request_counter: int = 0

    # -Instance Methods: Public Primary
    async def login(
        self, id_: str, source_id: int, token: str,
        company: str, segment: str, domain: str, user_group: str, access_level: str,
        dt: datetime, acl: str, qos: int = 2  # -TODO: MAKE ENUM
    ) -> None:
        '''Login request'''
        self.id = id_
        self.source = source_id
        msg: RequestDict = self.create_message(
            "ADMIN", "LOGIN", token=token, version="1.0",
            qoslevel=qos, credential=urlencode({
                'accesslevel': access_level,
                'acl': acl,
                'appid': id_,
                'authorized': "Y",
                'cddomain': domain,
                'company': company,
                'segment': segment,
                'timestamp': int(dt.timestamp() * 1000),
                'token': token,
                'usergroup': user_group,
                'userid': source_id,
            })
        )
        await self.send_messages(msg)

    async def logout(self) -> None:
        '''Logout request'''
        msg: Request_WebSocketDict = self.create_message("ADMIN", "LOGOUT")
        await self.send_messages(msg)

    async def quality_of_service(self, qos: int) -> None:  # -TODO: MAKE ENUM
        '''Change data rate speed request'''
        msg: Request_WebSocketDict = self.create_message("ADMIN", "QOS", qoslevel=qos)
        await self.send_messages(msg)

    # -Instance Methods: Public Secondary
    def create_message(
        self, service: str, command: str, **kwargs
    ) -> Request_WebSocketDict:
        '''Create a formatted message request for sending'''
        request: Request_WebSocketDict = {
            'account': self.id,
            'command': command,
            'parameters': kwargs if kwargs else {},
            'requestid': self.request_counter,
            'service': service,
            'source': self.source,
        }
        self.request_counter += 1
        return request

    async def send_messages(
        self, requests: Request_WebSocketDict | list[Request_WebSocketDict]
    ) -> None:
        '''Send formatted message request or list of requests'''
        if not isinstance(requests, list):
            requests = [requests]
        await self.send_json({'requests': requests})
