from dataclasses import dataclass

from .aries_controller_base import AriesAgentControllerBase
from .aries_webhook_server import AriesWebhookServer
from .controllers.multitenant import MultitenancyController

import logging
import ipaddress

logger = logging.getLogger(__name__)


@dataclass
class AriesAgentController(AriesAgentControllerBase):
    """The Aries Agent Controller class

    This class allows you to interact with Aries by exposing the aca-py API.

    Attributes:
    ----------
    is_multitenant : bool
        Initialise the multitenant interface (default is False)
    """

    is_multitenant: bool = False

    def __post_init__(self):
        """Constructs additional attributes and logic
        Creates headers, instantiates a client sessions and initialises
        the controller interfaces for the aries swagger API.
        """

        super().__post_init__()

        if self.is_multitenant:
            self.multitenant = MultitenancyController(
                self.admin_url, self.client_session
            )

    async def init_webhook_server(
        self, webhook_host: str, webhook_port: int, webhook_base: str = ""
    ):
        """Create a webhook listeners

        Args:
        ----
        webhook_host : str
            The url of the webhook host
        webhook_port : int
            The exposed port for webhooks on the host
        webhook_base : str
            The base url for webhooks (default is "")
        """
        assert type(webhook_host) is str
        assert ipaddress.ip_address(webhook_host)
        assert type(webhook_port) is int
        try:
            self.webhook_server: AriesWebhookServer = AriesWebhookServer(
                webhook_host=webhook_host,
                webhook_port=webhook_port,
                webhook_base=webhook_base,
                is_multitenant=self.is_multitenant,
            )
            await self.webhook_server.listen_webhooks()
            logger.info(
                f"Webhook server started on {self.webhook_server.webhook_host}."
            )
        except Exception as exc:
            logger.error(f"Listening webhooks failed! {exc!r} occurred.")
            raise Exception(f"{exc!r}")
