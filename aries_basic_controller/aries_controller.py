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


class AriesAgentController:

    def __init__(self, webhook_host: str, webhook_port: int, admin_url: str, connections: bool, webhook_base: str = ""):

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
        self.proc = None


    def register_listeners(self, listeners, defaults=True):
        if defaults:
            if self.connections:
                pub.subscribe(self.connections.default_handler, "connections")
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
        pub.sendMessage(topic, payload=payload)
        return web.Response(status=200)


    async def terminate(self):
        # loop = asyncio.get_event_loop()
        # if self.proc:
        #     await loop.run_in_executor(None, self._terminate)
        await self.client_session.close()
        if self.webhook_site:
            await self.webhook_site.stop()



