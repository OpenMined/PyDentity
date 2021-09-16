from uplink import (
    Consumer,
    Path,
    Query,
    Body,
    Header,
    get,
    post,
    patch,
    put,
    delete,
    returns,
    json,
)

from typing import Dict, List, Optional, Union  # noqa: F401

from aries_cloudcontroller.model.send_message import SendMessage


class BasicmessageApi(Consumer):
    async def send_message(
        self, *, conn_id: str, body: Optional[SendMessage] = None
    ) -> Dict:
        """Send a basic message to a connection"""
        return await self.__send_message(
            conn_id=conn_id,
            body=body,
        )

    @returns.json
    @json
    @post("/connections/{conn_id}/send-message")
    def __send_message(
        self, *, conn_id: str, body: Body(type=SendMessage) = {}
    ) -> Dict:
        """Internal uplink method for send_message"""
