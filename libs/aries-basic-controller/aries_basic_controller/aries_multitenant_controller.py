from dataclasses import dataclass

from .aries_controller import AriesAgentController

import logging

logger = logging.getLogger("aries_controller")


@dataclass
class AriesMultitenantController(AriesAgentController):
    """The Aries Agent Controller class

    This class allows you to interact with Aries by exposing the aca-py API. 

    Attributes:
    ----------
    admin_url : str
        The URL for the Admin API
    webhook_host : str
        The url of the webhook host
    webhook_port : int
        The exposed port for webhooks on the host
    webhook_base : str
        The base url for webhooks (default is "")
    mediation : bool
        Initialise the mediation interface (default is False)
    api_key : str
        The API key (default is None)
    wallet_id : str
        The tenant wallet identifier (default is None)
    is_multitenant : bool
        Initialise the multitenant interface (default is True)
    tenant_jwt : str
        The tenant JW token (default is None)
    """

    is_multitenant: bool = True
    tenant_jwt: str = None

    def __post_init__(self):
        """Constructs additional attributes,
        and logic defined by attributes set during instantiation
        """

        super().__post_init__()

        if self.api_key:
            self.headers.update({"X-API-Key": self.api_key})

        if self.tenant_jwt:
            self.headers.update(
                {'Authorization': 'Bearer ' + self.tenant_jwt,
                    'content-type': "application/json"})

        # Update the current client session instantiated in the parent class
        self.client_session.headers.update(self.headers)

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
