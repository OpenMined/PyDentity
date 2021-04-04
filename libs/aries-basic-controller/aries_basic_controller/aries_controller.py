from dataclasses import dataclass

from .aries_controller_base import AriesAgentControllerBase
from .aries_webhook_server import AriesWebhookServer

import logging

logger = logging.getLogger("aries_controller")


@dataclass
class AriesAgentController(AriesAgentControllerBase):
    """The Aries Agent Controller class

    This class allows you to interact with Aries by exposing the aca-py API.
    """

    def __post_init__(self):
        """Constructs additional attributes and logic
        Creates headers, instantiates a client sessions and initialises
        the controller interfaces for the aries swagger API.
        """

        super().__post_init__()

    def webhook_server(
                        self,
                        webhook_host: str = None,
                        webhook_port: str = None,
                        webhook_base: str = ""):
        """Create a webhooklisteners

        Args:
        ----
        webhook_host : str
            The url of the webhook host (default is None)
        webhook_port : int
            The exposed port for webhooks on the host (default is None)
        webhook_base : str
            The base url for webhooks (default is "")
        """
        self.webhook_server: AriesWebhookServer = AriesWebhookServer(
            webhook_host=webhook_host,
            webhook_port=webhook_port,
            webhook_base=webhook_base,
            is_multitenant=self.is_multitenant)

    def add_listener(self, listener):
        """Subscribe to a listeners for a topic

        Args:
        ----
        listener : dict
            A dictionary comprised of "handler": handler (fct) and
            "topic":"topicname" key-value pairs
        """
        try:
            pub_topic_path = listener['topic']
            print("Subscribing too: " + pub_topic_path)
            pub.subscribe(listener["handler"], pub_topic_path)
            logger.debug("Lister added for topic : ", pub_topic_path)
        except Exception as exc:
            logger.warning(
                f"Adding webhooks listener failed! {exc!r} occurred.")

    async def listen_webhooks(self):
        try:
            await self.webhook_server.listen_webhooks()
        except AttributeError:
            logger.warning("Missing webhook listener.")
        except Exception as exc:
            logger.warning(
                f"Listening webhooks failed! {exc!r} occurred.")
