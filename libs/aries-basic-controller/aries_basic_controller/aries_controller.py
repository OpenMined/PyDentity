from aiohttp import (
    web,
    ClientSession,
    ClientRequest,
)
from dataclasses import dataclass
from pubsub import pub
import sys

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

import logging

logger = logging.getLogger("aries_controller")


@dataclass
class AriesAgentController:
    """The Aries Agent Controller class
    
    This class allows you to interact with Aries by exposing the aca-py API. 
    
    Attributes
    ----------
    webhook_host : str
        The url of the webhook host 
    webhook_port : int 
        The exposed port for webhooks on the host
    admin_url : str
        The URL for the Admin API
    webhook_base : str
        The base url for webhooks (default is "")
    connections : bool
        Specify whether to create connecitons (default is True)
    messaging : bool
        Initialise the messaging interface (default is True)
    multitenant : bool
        Initialise the multitenant interface (default is False)
    mediation : bool
        Initialise the mediation interface (default is False)
    issuer : bool
        Initialise the issuer interface (defautl is True)
    action_menu : bool
        Initialise the action menu interface (default is True)
    revocations : bool
        Initialise revocation interface for credentials (default is True)
    api_key : str 
        The API key (default is None)
    tenant_jwt: str
        The tenant JW token (default is None)
    """
    
    ## TODO rethink how to initialise. Too many args?
    ## is it important to let users config connections/issuer etc
    webhook_host: str
    webhook_port: int
    admin_url: str
    webhook_base: str = ""
    connections: bool = True
    messaging: bool = True
    multitenant: bool = False
    mediation: bool = False
    issuer: bool = True
    action_menu: bool = True
    revocations: bool = True
    api_key: str = None
    tenant_jwt: str = None
    wallet_id: str = "base"


    def __post_init__(self):
        """Constructs additional attributes, 
        and logic defined by attributes set during initial instantiation
        """
        
        self.webhook_site = None
        self.connections_controller = None
        
        # Construct headers for Client Session and the session itself
        self.headers = {}
        
        if self.api_key:
            self.headers.update({"X-API-Key": self.api_key})

        if self.tenant_jwt:
            self.headers.update({'Authorization': 'Bearer ' + self.tenant_jwt, 'content-type': "application/json"})


        self.client_session: ClientSession = ClientSession(headers=self.headers)
    
        # Instantiate controllers based on the provided attributes
        if self.connections:
            self.connections = ConnectionsController(self.admin_url, self.client_session)
            
        if self.messaging:
            self.messaging = MessagingController(self.admin_url, self.client_session)

        self.proofs = ProofController(self.admin_url, self.client_session)
        self.ledger = LedgerController(self.admin_url, self.client_session)
        self.credentials = CredentialController(self.admin_url, self.client_session)
        self.server = ServerController(self.admin_url, self.client_session)
        self.oob = OOBController(self.admin_url, self.client_session)

        if self.multitenant:
            self.multitenant = MultitenancyController(self.admin_url, self.client_session)

        if self.mediation:
            self.mediation = MediationController(self.admin_url, self.client_session)

        if self.issuer:
            self.schema = SchemaController(self.admin_url, self.client_session)
            self.wallet = WalletController(self.admin_url, self.client_session)
            self.definitions = DefinitionsController(self.admin_url, self.client_session)
            self.issuer = IssuerController(self.admin_url, self.client_session, self.connections,
                                            self.wallet, self.definitions)

        if self.action_menu:
            self.action_menu = ActionMenuController(self.admin_url, self.client_session)

        if self.revocations:
            self.revocations = RevocationController(
                self.admin_url,
                self.client_session
            )


    
    def update_tenant_jwt(self, tenant_jwt: str): 
        """Update the tenant JW token attribute and the header
        
        Args:
        ----
        tenant_jwt : str 
            The tenant's JW token
        """
        self.tenant_jwt = tenant_jwt
        self.headers.update({'Authorization': 'Bearer ' + tenant_jwt, 'content-type': "application/json"})
        self.client_session.headers.update(self.headers)
        
        
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
        """Removes the API key attribute and corresponding headers from the Client Session"""
        self.api_key = None
        if 'X-API-Key' in self.client_session.headers:
            del self.client_session.headers['X-API-Key']
            del self.headers['X-API-Key']
      
      
    def remove_tenant_jwt(self):
        """Removes the tenant's JW Token attribute and corresponding headers from the Client Session"""
        self.tenant_jwt = None
        if 'Authorization' in self.client_session.headers:
            del self.client_session.headers['Authorization']
            del self.headers['Authorization']
        if 'content-type' in self.client_session.headers:
            del self.client_session.headers['content-type']
            del self.headers['content-type']


    def register_listeners(self, listeners, defaults=True):
        """Registers the webhook listners
        
        Args:
        ----
        listeners : [dict]
            A collection of dictionaries comprised of a "handler": handler (fct) and a "topic":"topicname" key-value pairs
        defaults : bool
            Whether to connect to the default handlers for connections, basicmessage and present_proof 
            (default is True)
        """
        try:
            if defaults:
                if self.connections:
                    pub.subscribe(self.connections.default_handler, "connections")
                if self.messaging:
                    pub.subscribe(self.messaging.default_handler, "basicmessages")
                if self.proofs:
                    pub.subscribe(self.proofs.default_handler, "present_proof")

            for listener in listeners:
                self.add_listener(listener)
        except Exception as exc:
            print(f"Register webhooks listeners failed! {exc!r} occurred.")
            logger.warn(f"Register webhooks listeners failed! {exc!r} occurred.")



    def add_listener(self, listener):
        """Subscribe to a listeners for a topic
        
        Args:
        ----
        listener : dict
            A dictionary comprised of a "handler": handler (fct) and a "topic":"topicname" key-value pairs
        """
        try:
            pub_topic_path = listener['topic']
            if self.wallet_id:
                pub_topic_path = f"{self.wallet_id}.{pub_topic_path}"
            print("Subscribing too: " + pub_topic_path)
            pub.subscribe(listener["handler"], pub_topic_path)

            logger.debug("Lister added for topic : ", pub_topic_path)
        except Exception as exc:
            print(f"Adding webhooks listener failed! {exc!r} occurred.")
            logger.warn(f"Adding webhooks listener failed! {exc!r} occurred.")
            


    def remove_listener(self, listener):
        """Remove a listener for a topic
        
        Args:
        ----
        listener : dict
            A dictionary comprised of a "handler": handler (fct) and a "topic":"topicname" key-value pairs
        """
        try:
            if pub.isSubscribed(listener["handler"], listener["topic"]):
                pub.unsubscribe(listener["handler"], listener["topic"])
            else:
                logger.debug("Listener not subscribed", listener)
        except Exception as exc:
            print(f"Removing webhooks listener failed! {exc!r} occurred.")
            logger.warn(f"Removing webhooks listener failed! {exc!r} occurred.")
            


    def remove_all_listeners(self, topic: str = None):
        """Remove all listeners for one or all topics
        
        Args:
        ----
        topic : str
            The topic to stop listening for (default is None). Default will cause unsubscribing from all topics.
        """
        # Note advanced use of function can include both listenerFilter and topicFilter for this
        # Add when needed
        try:
            pub.unsubAll(topicName=topic)
        except Exception as exc:
            print(f"Removing all webhooks listeners failed! {exc!r} occurred.")
            logger.warn(f"Removing all webhooks listeners failed! {exc!r} occurred.")
            


    async def listen_webhooks(self):
        """Create a server to listen to webhooks"""
        try:
            app = web.Application()
            app.add_routes([web.post(self.webhook_base + "/{wallet}/topic/{topic}/", self._receive_webhook)])
            runner = web.AppRunner(app)
            await runner.setup()
            self.webhook_site = web.TCPSite(runner, self.webhook_host, self.webhook_port)
            await self.webhook_site.start()
        except Exception as exc:
            print(f"Listening webhooks failed! {exc!r} occurred.")
            logger.warn(f"Listening webhooks failed! {exc!r} occurred.")



    async def _receive_webhook(self, request: ClientRequest):
        """Helper to receive webhooks by requesting it
        
        Args:
        ----
        request : ClientRequest
            The client request to which the corresponding webhooks shall be received
            
        Returns:
        -------
        Response:
            A response with status 200
        """
        topic = request.match_info["topic"]
        wallet = request.match_info["wallet"]
        print("wallet", wallet)
        try:
            payload = await request.json()
            await self._handle_webhook(wallet, topic, payload)
            return web.Response(status=200)
        except Exception as exc:
            logger.warn(f"Receiving webhooks failed! {exc!r} occurred.")
        


    async def _handle_webhook(self, wallet, topic, payload):
        """Helper handling a webhook
        
        Args:
        ----
        topic : str
            The topic to handle webhooks for
        payload : dict
            A JSON-like dictionary representation of the payload
        """
        try:
            pub_topic_path = f"{wallet}.{topic}"
            print(f"Handle Webhook - {pub_topic_path}", payload)
            logging.debug(f"Handle Webhook - {pub_topic_path}", payload)
            pub.sendMessage(pub_topic_path, payload=payload)
            # return web.Response(status=200)
        except Exception as exc:
            logger.warn(f"Handling webhooks failed! {exc!r} occurred when trying to handle this topic: {topic}")
            


    async def terminate(self):
        """Terminate the controller client session and webhook listeners"""
        try:
            await self.client_session.close()
            if self.webhook_site:
                await self.webhook_site.stop()
        except Exception as exc:
            print(f"Terminating webhooks listener failed! {exc!r} occurred.")
            logger.warn(f"Terminating webhooks listener failed! {exc!r} occurred.")
