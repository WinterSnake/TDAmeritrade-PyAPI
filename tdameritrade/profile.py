#!/usr/bin/python
##-------------------------------##
## TDAmeritrade PyAPI            ##
## Written By: Ryan Smith        ##
##-------------------------------##
## TDAmeritrade Profile          ##
##-------------------------------##

## Imports
from .. import urls
from ..session import ClientSession
from ..websocket import ClientWebSocket


## Classes
class Profile:
    """TDAmeritrade Profile"""

    # -Constructor
    def __init__(self, session: ClientSession) -> None:
        self._session: ClientSession = session

    # -Instance Methods
    async def user_principals(
        self, preferences: bool = False, surrogate_ids: bool = False,
        streamer_keys: bool = False, streamer_info: bool = False,
    ) -> None:
        '''Get user principals and additional information for profile and accounts'''
        # -Populate fields
        fields: list[str] = []
        if preferences:
            fields.append("preferences")
        if surrogate_ids:
            fields.append("surrogateIds")
        if streamer_keys:
            fields.append("streamerSubscriptionKeys")
        if streamer_info:
            fields.append("streamerConnectionInfo")
        return await self._session.get(urls.v1.user_principals(), params={'fields': fields})
