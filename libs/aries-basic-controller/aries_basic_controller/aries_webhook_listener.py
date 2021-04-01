from aiohttp import (
    web,
    ClientRequest,
)
from dataclasses import dataclass
from pubsub import pub
import logging

logger = logging.getLogger("aries_webhook_listener")


@dataclass
class AriesWebhookListener:
    """The Aries Webhook Listener class

    This class allows you to interact with Aries by exposing the aca-py API.

    Attributes:
    ----------
    webhook_host : str
        The url of the webhook host
    webhook_port : int
        The exposed port for webhooks on the host
    webhook_base : str
        The base url for webhooks (default is "")
    wallet_id : str
        The tenant wallet identifier
    is_multitenant : bool
        Initialise the multitenant interface (default is False)
    """

    webhook_host: str
    webhook_port: int
    webhook_base: str = ""
    is_multitenant: bool = False

    async def listen_webhooks(self):
        """Create a server to listen to webhooks"""
        try:
            app = web.Application()
            app.add_routes([web.post(
                self.webhook_base + "/topic/{topic}/",
                self._receive_webhook)])
            if self.is_multitenant:
                app.add_routes(
                    [web.post(
                        self.webhook_base + "/{wallet_id}/topic/{topic}/",
                        self._receive_webhook)])
            runner = web.AppRunner(app)
            await runner.setup()
            self.webhook_site = web.TCPSite(
                runner,
                self.webhook_host,
                self.webhook_port)
            await self.webhook_site.start()
        except Exception as exc:
            logger.warning(f"Listening webhooks failed! {exc!r} occurred.")

    async def _receive_webhook(self, request: ClientRequest):
        """Helper to receive webhooks by requesting it

        Args:
        ----
        request : ClientRequest
            The client request to which the corresponding webhooks
            shall be received

        Returns:
        -------
        Response:
            A response with status 200
        """
        topic = request.match_info["topic"]
        wallet_id = None
        if self.is_multitenant:
            wallet_id = request.match_info["wallet_id"]
        print("wallet", wallet_id)
        try:
            payload = await request.json()
            await self._handle_webhook(wallet_id, topic, payload)
            return web.Response(status=200)
        except Exception as exc:
            logger.warning(f"Receiving webhooks failed! {exc!r} occurred.")

    async def _handle_webhook(self, wallet_id, topic, payload):
        """Helper handling a webhook

        Args:
        ----
        wallet_id: str
            The identifier for the wallet the webhook is for
        topic : str
            The topic to handle webhooks for
        payload : dict
            A JSON-like dictionary representation of the payload
        """
        try:
            pub_topic_path = topic
            if wallet_id:
                pub_topic_path = f"{wallet_id}.{topic}"
            logging.debug(f"Handle Webhook - {pub_topic_path}", payload)
            pub.sendMessage(pub_topic_path, payload=payload)
            # return web.Response(status=200)
        except Exception as exc:
            logger.warning(
                (f"Handling webhooks failed! {exc!r} occurred"
                    f" when trying to handle this topic: {topic}"))

    async def terminate(self):
        """Terminate the controller client session and webhook listeners"""
        try:
            await self.webhook_site.stop()
        except AttributeError:
            # Do nothing if no webhook site server is running
            return
        except Exception as exc:
            logger.warning(
                f"Terminating webhooks listener failed! {exc!r} occurred.")
