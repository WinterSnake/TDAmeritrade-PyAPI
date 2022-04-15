#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## TDAmeritrade Websocket        ##
##-------------------------------##

## Imports
from datetime import datetime
from typing import Any, TypedDict
from urllib.parse import urlencode

import aiohttp

## Constants
MessageDict = TypedDict(
    "MessageDict", {
        'service': str, 'command': str, 'requestid': int,
        'account': str, 'source': int, 'parameters': dict[str, Any]
    }, total=False
)


## Classes
class ClientWebSocket(aiohttp.ClientWebSocketResponse):
    """TDAmeritrade Client WebSocket"""

    # -Constructor
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app_id: str | None = None
        self.account_id: int | None = None
        self.request_id: int = 0

    # -Instance Methods: Private
    def _create_message(
        self, service: str, command: str, **kwargs
    ) -> MessageDict:
        '''Create formatted request for sending'''
        request: dict = {
            'service': service,
            'command': command,
            'requestid': self.request_id,
            'account': self.app_id,
            'source': self.account_id,
            'parameters': kwargs if kwargs else {}
        }
        self.request_id += 1
        return request

    async def _send_message(self, request: MessageDict) -> None:
        '''Send formatted request as list'''
        await self.send_json({'requests': [request]})

    # -Instance Methods: Public
    async def login(
        self, app_id: str, account_id: int, token: str, user_group: str,
        company: str, segment: str, domain: str, access_level: str,
        dt: datetime, acl: str, qos: int = 2
    ) -> None:
        '''Login through websocket authentication'''
        self.app_id = app_id
        self.account_id = account_id
        msg: MessageDict = self._create_message(
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
        await self._send_message(msg)

    async def logout(self) -> None:
        '''Logout from websocket authentication'''
        msg: MessageDict = self._create_message("ADMIN", "LOGOUT")
        await self._send_message(msg)

    async def quality_of_service(self, qos: int) -> None:
        '''Update rate of data being streamed from TDAmeritrade'''
        smsg: MessageDict = elf._create_message("ADMIN", "QOS", qoslevel=qos)
        await self._send_message(msg)
