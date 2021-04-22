from .base import BaseController
from aiohttp import ClientSession
import logging

logger = logging.getLogger("aries_controller.messaging")


class MessagingController(BaseController):
    def __init__(self, admin_url: str, client_session: ClientSession):
        super().__init__(admin_url, client_session)

    def default_handler(self, payload):
        logger.debug("Message Received ", payload)

    async def send_message(self, connection_id, msg):
        response = await self.admin_POST(
            f"/connections/{connection_id}/send-message",
            {
                "content": msg,
            },
        )
        return response

    async def trust_ping(self, connection_id: str, comment_msg: str = None):
        if comment_msg:
            response = await self.admin_POST(
                f"/connections/{connection_id}/send-ping", {"comment": comment_msg}
            )
        else:
            response = await self.admin_POST(f"/connections/{connection_id}/send-ping", {})
        return response
