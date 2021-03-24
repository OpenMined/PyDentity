from aiohttp import (
    web,
    ClientSession,
    ClientRequest,
)
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

class AriesAgentController:

    ## TODO rethink how to initialise. Too many args?
    ## is it important to let users config connections/issuer etc
    def __init__(
        self,
        webhook_host: str,
        webhook_port: int,
        admin_url: str,
        webhook_base: str = "",
        connections: bool = True,
        messaging: bool = True,
        multitenant: bool = False,
        mediation: bool = False,
        issuer: bool = True,
        action_menu: bool = True,
        revocations: bool = True,
        api_key: str = None,
        tennant_jwt: str = None,
    ):

        self.webhook_site = None
        self.admin_url = admin_url
        if webhook_base:
            self.webhook_base = webhook_base
        else:
            self.webhook_base = ""
        self.webhook_host = webhook_host
        self.webhook_port = webhook_port
        self.connections_controller = None

        headers = {}

        if api_key:
            headers.update({"X-API-Key": api_key})

        if tennant_jwt:
            headers.update({'Authorization': 'Bearer ' + tennant_jwt, 'content-type': "application/json"})

        self.client_session: ClientSession = ClientSession(headers=headers)
        

        if connections:
            self.connections = ConnectionsController(self.admin_url, self.client_session)
        if messaging:
            self.messaging = MessagingController(self.admin_url, self.client_session)

        self.proofs = ProofController(self.admin_url, self.client_session)
        self.ledger = LedgerController(self.admin_url, self.client_session)
        self.credentials = CredentialController(self.admin_url, self.client_session)
        self.server = ServerController(self.admin_url, self.client_session)
        self.oob = OOBController(self.admin_url, self.client_session)

        if multitenant:
            self.multitenant = MultitenancyController(self.admin_url, self.client_session)

        if mediation:
            self.mediation = MediationController(self.admin_url, self.client_session)

        if issuer:
            self.schema = SchemaController(self.admin_url, self.client_session)
            self.wallet = WalletController(self.admin_url, self.client_session)
            self.definitions = DefinitionsController(self.admin_url, self.client_session)
            self.issuer = IssuerController(self.admin_url, self.client_session, self.connections,
                                           self.wallet, self.definitions)

        if action_menu:
            self.action_menu = ActionMenuController(self.admin_url, self.client_session)

        if revocations:
            self.revocations = RevocationController(
                self.admin_url,
                self.client_session
            )

    # TODO: Determine whether we really want to essentially create a whole new ClientSession object as done below
    # Ideally we'd just update the existing session along the lines of self.client_session(headers) 
    # That does not work, though because it is not callable and updating cannot be achieved reliably 
    # because headers can be of different type
    # from https://docs.aiohttp.org/en/stable/client_reference.html :
    # "May be either iterable of key-value pairs or Mapping (e.g. dict, CIMultiDict)."
    # So for now let's create a new ClientSession and use all the instances current attributes 
    # to update every attr using ClientSession
    def update_tennant_jwt(self, tennant_jwt): 
        self.tennant_jwt = tennant_jwt
        headers = {'Authorization': 'Bearer ' + tennant_jwt, 'content-type': "application/json"}
        self.client_session: ClientSession = ClientSession(headers=headers)

        if self.connections:
            self.connections = ConnectionsController(self.admin_url, self.client_session)

        if self.messaging:
            self.messaging = MessagingController(self.admin_url, self.client_session)

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


    def register_listeners(self, listeners, defaults=True):
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
        try:
            pub.subscribe(listener["handler"], listener["topic"])
        except Exception as exc:
            print(f"Adding webhooks listener failed! {exc!r} occurred.")
            logger.warn(f"Adding webhooks listener failed! {exc!r} occurred.")
            

    def remove_listener(self, listener):
        try:
            if pub.isSubscribed(listener["handler"], listener["topic"]):
                pub.unsubscribe(listener["handler"], listener["topic"])
            else:
                logger.debug("Listener not subscribed", listener)
        except Exception as exc:
            print(f"Removing webhooks listener failed! {exc!r} occurred.")
            logger.warn(f"Removing webhooks listener failed! {exc!r} occurred.")
            

    def remove_all_listeners(self, topic: str = None):
        # Note advanced use of function can include both listenerFilter and topicFilter for this
        # Add when needed
        try:
            pub.unsubAll(topicName=topic)
        except Exception as exc:
            print(f"Removing all webhooks listeners failed! {exc!r} occurred.")
            logger.warn(f"Removing all webhooks listeners failed! {exc!r} occurred.")
            

    async def listen_webhooks(self):
        try:
            app = web.Application()
            app.add_routes([web.post(self.webhook_base + "/topic/{topic}/", self._receive_webhook)])
            runner = web.AppRunner(app)
            await runner.setup()
            self.webhook_site = web.TCPSite(runner, self.webhook_host, self.webhook_port)
            await self.webhook_site.start()
        except Exception as exc:
            print(f"Listening webhooks failed! {exc!r} occurred.")
            logger.warn(f"Listening webhooks failed! {exc!r} occurred.")


    async def _receive_webhook(self, request: ClientRequest):
        topic = request.match_info["topic"]
        try:
            payload = await request.json()
            await self._handle_webhook(topic, payload)
            return web.Response(status=200)
        except Exception as exc:
            logger.warn(f"Receiving webhooks failed! {exc!r} occurred.")
        

    async def _handle_webhook(self, topic, payload):
        try:
            logging.debug(f"Handle Webhook - {topic}", payload)
            pub.sendMessage(topic, payload=payload)
            # return web.Response(status=200)
        except Exception as exc:
            logger.warn(f"Handling webhooks failed! {exc!r} occurred when trying to handle this topic: {topic}")
            

    async def terminate(self):
        try:
            await self.client_session.close()
            if self.webhook_site:
                await self.webhook_site.stop()
        except Exception as exc:
            print(f"Terminating webhooks listener failed! {exc!r} occurred.")
            logger.warn(f"Terminating webhooks listener failed! {exc!r} occurred.")
