#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## TDAmeritrade Websocket        ##
##-------------------------------##

## Imports
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

    # -Dunder Methods
    # -Instance Methods: Private
    # -Instance Methods: Public
    async def send_message(self, service: str, command: str, **kwargs) -> None:
        '''Send formatted request through websocket'''
        await self.send_json({
            "requests": [{
                'service': service,
                'command': command,
                'requestid': self.request_id,
                'account': self.app_id,
                'source': self.account_id,
                'parameters': kwargs
            }]
        })
        self.request_id += 1
