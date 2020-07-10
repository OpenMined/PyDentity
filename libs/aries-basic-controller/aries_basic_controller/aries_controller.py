from aiohttp import (
    web,
    ClientSession,
    ClientRequest,
    ClientResponse,
    ClientError,
    ClientTimeout,
)
from pubsub import pub
import asyncio

from .utils import log_msg
from .connections_controller import ConnectionsController
from .messaging_controller import MessagingController
from .schema_controller import SchemaController
from .wallet_controller import WalletController
from .definitions_controller import DefinitionsController
from .issuer_controller import IssuerController

import logging

logger = logging.getLogger("aries_controller")

class AriesAgentController:

    ## TODO rethink how to initialise. Too many args?
    def __init__(self, webhook_host: str, webhook_port: int, admin_url: str, webhook_base: str = "",
                 connections: bool = True, messaging: bool = True, issuer: bool = True):

        self.webhook_site = None
        self.admin_url = admin_url
        if webhook_base:
            self.webhook_base = webhook_base
        else:
            self.webhook_base = ""
        self.webhook_host = webhook_host
        self.webhook_port = webhook_port
        self.connections_controller = None
        self.client_session: ClientSession = ClientSession()
        if connections:
            self.connections = ConnectionsController(self.admin_url, self.client_session)
        if messaging:
            self.messaging = MessagingController(self.admin_url, self.client_session)
        self.proc = None
        if issuer:
            self.schema = SchemaController(self.admin_url, self.client_session)
            self.wallet = WalletController(self.admin_url, self.client_session)
            self.definitions = DefinitionsController(self.admin_url, self.client_session)
            self.issuer = IssuerController(self.admin_url, self.client_session, self.connections,
                                           self.wallet, self.definitions)


    def register_listeners(self, listeners, defaults=True):
        if defaults:
            if self.connections:
                pub.subscribe(self.connections.default_handler, "connections")
            if self.messaging:
                pub.subscribe(self.messaging.default_handler, "basic_messages")


        for listener in listeners:
            pub.subscribe(listener["handler"], listener["topic"])

    async def listen_webhooks(self):
        app = web.Application()
        app.add_routes([web.post(self.webhook_base + "/topic/{topic}/", self._receive_webhook)])
        runner = web.AppRunner(app)
        await runner.setup()
        self.webhook_site = web.TCPSite(runner, self.webhook_host, self.webhook_port)
        await self.webhook_site.start()

    async def _receive_webhook(self, request: ClientRequest):
        topic = request.match_info["topic"]
        payload = await request.json()
        await self.handle_webhook(topic, payload)
        return web.Response(status=200)

    async def handle_webhook(self, topic, payload):
        # log_msg(f"Hanlde {topic}")
        # log_msg(payload)
        logging.debug(f"Handle Webhook - {topic}", payload)
        pub.sendMessage(topic, payload=payload)
        return web.Response(status=200)


    async def terminate(self):
        await self.client_session.close()
        if self.webhook_site:
            await self.webhook_site.stop()



