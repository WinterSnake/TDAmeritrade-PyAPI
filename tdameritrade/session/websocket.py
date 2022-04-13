#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## TDAmeritrade Websocket        ##
##-------------------------------##

## Imports
from datetime import datetime
from typing import TypedDict
from urllib.parse import urlencode

import aiohttp


## Classes
class ClientWebSocket(aiohttp.ClientWebSocketResponse):
    """TDAmeritrade Client WebSocket"""

    # -Constructor
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app_id: str | None = None
        self.account_id: int | None = None
        self.request_id: int = 0
        self.requests: list[RequestDict] = []

    # -Instance Methods: Private
    def _create_message(
        self, service: str, command: str, *, require: bool = False, **kwargs
    ) -> None:
        '''Create formatted request for sending'''
        request: dict = {
            'service': service,
            'command': command,
            'requestid': self.request_id,
            'account': self.app_id,
            'source': self.account_id,
        }
        if kwargs:
            request['parameters'] = kwargs
        self.request_id += 1
        self.requests.append(request)

    # -Instance Methods: Public
    async def login(
        self, app_id: str, account_id: int, token: str, user_group: str,
        company: str, segment: str, domain: str, access_level: str,
        dt: datetime, acl: str, qos: int = 2
    ) -> None:
        '''Login through websocket authentication'''
        self.app_id = app_id
        self.account_id = account_id
        self._create_message(
            "ADMIN", "LOGIN", token=token, version="1.0",
            qoslevel=qos, credential=urlencode({
                'userid': account_id,
                'token': token,
                'company': company,
                'segment': segment,
                'cddomain': domain,
                'usergroup': user_group,
                'accesslevel': access_level,
                'authorized': "Y",
                'timestamp': int(dt.timestamp() * 1000),
                'appid': app_id,
                'acl': acl,
            })
        )

    async def logout(self) -> None:
        '''Logout from websocket authentication'''
        self._create_message("ADMIN", "LOGOUT")

    async def send_messages(self) -> None:
        '''Sends all stored requests and clears buffer'''
        await self.send_json({'requests': self.requests})
        self.requests = []

    async def quality_of_service(self, qos: int) -> None:
        '''Update rate of data being streamed from TDAmeritrade'''
        self._create_message("ADMIN", "QOS", qoslevel=qos)
