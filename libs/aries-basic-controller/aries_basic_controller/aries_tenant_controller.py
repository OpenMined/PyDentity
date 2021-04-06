from dataclasses import dataclass
from pubsub import pub

from .aries_controller_base import AriesAgentControllerBase

import logging

logger = logging.getLogger("aries_tenant_controller")


@dataclass
class AriesTenantController(AriesAgentControllerBase):
    """The Aries Agent Controller class

    This class allows you to interact with Aries by exposing the aca-py API.

    Attributes:
    ----------
    wallet_id : str
        The tenant wallet identifier
    tenant_jwt : str
        The tenant JW token
    """

    wallet_id: str
    tenant_jwt: str

    def __post_init__(self):
        """Constructs additional attributes,
        and logic defined by attributes set during instantiation
        """

        super().__post_init__()

        if self.tenant_jwt:
            self.headers.update(
                {'Authorization': 'Bearer ' + self.tenant_jwt,
                    'content-type': "application/json"})

        # Update the current client session instantiated in the parent class
        self.client_session.headers.update(self.headers)

    def init_webhook_server(self):
        raise NotImplementedError(
            ("Please, use an AriesAgentController to start a webhook server\n"
                "Webhook server fct is disallowed for tenant controllers."))

    def listen_webhooks(self):
        raise NotImplementedError(
            ("Please, use an AriesAgentController to start a webhook server\n"
                "Webhook server fct is disallowed for tenant controllers."))

    def add_listener(self, listener):
        """Subscribe to a listeners for a topic
        Overrides parent method and uses the tenant's wallet ID to
        listen for that wallet's webhooks under the url defined
        by the wallet ID.

        Args:
        ----
        listener : dict
            A dictionary comprised of "handler": handler (fct) and
            "topic":"topicname" key-value pairs
        """
        try:
            pub_topic_path_base = listener['topic']
            pub_topic_path = f"{self.wallet_id}.{pub_topic_path_base}"
            pub.subscribe(listener["handler"], pub_topic_path)
            logger.debug("Lister added for topic : ", pub_topic_path)
        except self.wallet_id == "":
            logger.error(
                "Cannot add listener for empty wallet_id.")
        except Exception as exc:
            logger.warning(
                f"Adding webhooks listener failed! {exc!r} occurred.")

    def update_wallet_id(self, wallet_id: str):
        """This wallet_id is used to register for webhooks
        specific to this sub_wallet

        Args:
        ----
        wallet_id : str
            The tenant wallet identifier
        """
        try:
            self.wallet_id = wallet_id
        except wallet_id == "":
            raise Exception("wallet_id must not be empty")

    def update_tenant_jwt(self, tenant_jwt: str, wallet_id: str):
        """Update the tenant JW token attribute and the header

        Args:
        ----
        tenant_jwt : str
            The tenant's JW token
        wallet_id : str
            The tenant wallet identifier
        """
        try:
            self.tenant_jwt = tenant_jwt
            self.update_wallet_id(wallet_id)
            self.headers.update(
                {'Authorization': 'Bearer ' + tenant_jwt,
                    'content-type': "application/json"})
            self.client_session.headers.update(self.headers)
        except tenant_jwt == "":
            raise Exception("tenant_jwt must not be empty")
        except Exception as exc:
            logger.warning(
                (f"Updating tenant JW token"
                    f" failed! {exc!r} occurred."))

    def remove_tenant_jwt(self):
        """Removes the tenant's JW Token attribute and corresponding
        headers from the Client Session"""
        try:
            self.tenant_jwt = None
            if 'Authorization' in self.client_session.headers:
                del self.client_session.headers['Authorization']
                del self.headers['Authorization']
            if 'content-type' in self.client_session.headers:
                del self.client_session.headers['content-type']
                del self.headers['content-type']
        except Exception as exc:
            logger.warning(
                f"Removing JW token failed! {exc!r} occurred.")
