from aiohttp import (
    ClientSession,
)
from dataclasses import dataclass
from pubsub import pub

from .controllers.connections import ConnectionsController
from .controllers.messaging import MessagingController
from .controllers.mediation import MediationController
from .controllers.schema import SchemaController
from .controllers.wallet import WalletController
from .controllers.definitions import DefinitionsController
from .controllers.issuer import IssuerController
from .controllers.proof import ProofController
from .controllers.ledger import LedgerController
from .controllers.credential import CredentialController
from .controllers.multitenant import MultitenancyController
from .controllers.server import ServerController
from .controllers.oob import OOBController
from .controllers.action_menu import ActionMenuController
from .controllers.revocation import RevocationController

from .aries_webhook_listener import AriesWebhookListener

import logging

logger = logging.getLogger("aries_controller")


@dataclass
class AriesAgentController:
    """The Aries Agent Controller class

    This class allows you to interact with Aries by exposing the aca-py API.

    Attributes:
    ----------
    admin_url : str
        The URL for the Admin API
    is_multitenant : bool
        Initialise the multitenant interface (default is False)
    mediation : bool
        Initialise the mediation interface (default is False)
    api_key : str
        The API key (default is None)
    """

    admin_url: str
    is_multitenant: bool = False
    api_key: str = None

    def __post_init__(self):
        """Constructs additional attributes and logic
        Creates headers, instantiates a client sessions and initialises
        the controller interfaces for the aries swagger API.
        """

        self.webhook_site = None
        self.connections_controller = None

        # Construct headers for Client Session and the session itself
        self.headers = {}

        if self.api_key:
            self.headers.update({"X-API-Key": self.api_key})

        self.client_session: ClientSession = ClientSession(
            headers=self.headers)

        # Instantiate controllers
        self.connections = ConnectionsController(
            self.admin_url,
            self.client_session)

        self.messaging = MessagingController(
            self.admin_url,
            self.client_session)

        self.proofs = ProofController(
            self.admin_url,
            self.client_session)

        self.ledger = LedgerController(
            self.admin_url,
            self.client_session)

        self.credentials = CredentialController(
            self.admin_url,
            self.client_session)

        self.server = ServerController(
            self.admin_url,
            self.client_session)

        self.oob = OOBController(
            self.admin_url,
            self.client_session)

        if self.is_multitenant:
            self.multitenant = MultitenancyController(
                self.admin_url,
                self.client_session)

        self.mediation = MediationController(
            self.admin_url,
            self.client_session)

        self.schema = SchemaController(
            self.admin_url,
            self.client_session)

        self.wallet = WalletController(
            self.admin_url,
            self.client_session)

        self.definitions = DefinitionsController(
            self.admin_url,
            self.client_session)

        self.issuer = IssuerController(
            self.admin_url,
            self.client_session,
            self.connections,
            self.wallet,
            self.definitions)

        self.action_menu = ActionMenuController(
            self.admin_url,
            self.client_session)

        self.revocations = RevocationController(
            self.admin_url,
            self.client_session
        )

    def webhook_listener(
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
        self.webhook_listener: AriesWebhookListener = AriesWebhookListener(
            webhook_host=webhook_host,
            webhook_port=webhook_port,
            webhook_base=webhook_base,
            is_multitenant=self.is_multitenant)

    def update_api_key(self, api_key: str):
        """Update the API Key attribute and the header

        Args:
        ----
        api_key : str
            The API Key
        """
        self.api_key = api_key
        self.headers.update({"X-API-Key": api_key})
        self.client_session.headers.update(self.headers)

    def remove_api_key(self):
        """Removes the API key attribute and corresponding headers
        from the Client Session"""
        self.api_key = None
        if 'X-API-Key' in self.client_session.headers:
            del self.client_session.headers['X-API-Key']
            del self.headers['X-API-Key']

    def register_listeners(self, listeners, defaults=True):
        """Registers the webhook listners

        Args:
        ----
        listeners : [dict]
            A collection of dictionaries comprised of "handler": handler (fct)
            and "topic":"topicname" key-value pairs
        defaults : bool
            Whether to connect to the default handlers for connections,
            basicmessage and present_proof (default is True)
        """
        try:
            if defaults:
                if self.connections:
                    pub.subscribe(
                        self.connections.default_handler,
                        "connections")
                if self.messaging:
                    pub.subscribe(
                        self.messaging.default_handler,
                        "basicmessages")
                if self.proofs:
                    pub.subscribe(
                        self.proofs.default_handler,
                        "present_proof")

            for listener in listeners:
                self.add_listener(listener)
        except Exception as exc:
            logger.warning(
                f"Register webhooks listeners failed! {exc!r} occurred.")

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

    def remove_listener(self, listener):
        """Remove a listener for a topic

        Args:
        ----
        listener : dict
            A dictionary comprised of "handler": handler (fct) and
            "topic":"topicname" key-value pairs
        """
        try:
            if pub.isSubscribed(listener["handler"], listener["topic"]):
                pub.unsubscribe(listener["handler"], listener["topic"])
            else:
                logger.debug("Listener not subscribed", listener)
        except Exception as exc:
            logger.warning(
                f"Removing webhooks listener failed! {exc!r} occurred.")

    def remove_all_listeners(self, topic: str = None):
        """Remove all listeners for one or all topics

        Args:
        ----
        topic : str
            The topic to stop listening for (default is None). Default will
            cause unsubscribing from all topics.
        """
        # Note: advanced use of function can include both listenerFilter and
        # topicFilter for this
        # Add when needed
        try:
            pub.unsubAll(topicName=topic)
        except Exception as exc:
            logger.warning(
                f"Removing all webhooks listeners failed! {exc!r} occurred.")

    async def listen_webhooks(self):
        try:
            await self.webhook_listener.listen_webhooks()
        except AttributeError:
            logger.warning("Missing webhook listener.")
        except Exception as exc:
            logger.warning(
                f"Listening webhooks failed! {exc!r} occurred.")

    async def terminate(self):
        await self.client_session.close()
        try:
            await self.webhook_listener.terminate()
        except AttributeError:
            # There is no webhook listener
            return
        except Exception as exc:
            logger.warning(
                f"Terminate webhooks listener exception!\n {exc!r} occurred.")
