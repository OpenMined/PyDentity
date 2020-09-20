from aiohttp import web
from aries_basic_controller.aries_controller import AriesAgentController
import qrcode
import asyncio
import async_timeout

WEBHOOK_HOST = "0.0.0.0"
WEBHOOK_PORT = 8052
WEBHOOK_BASE = ""
ADMIN_URL = "http://opus-agent:8051"

# Based on the aca-py agent you wish to control
agent_controller = AriesAgentController(webhook_host=WEBHOOK_HOST, webhook_port=WEBHOOK_PORT,
                                   webhook_base=WEBHOOK_BASE, admin_url=ADMIN_URL)

asyncio.get_event_loop().run_until_complete(agent_controller.listen_webhooks())


async def hello(request):
    return web.Response(text="Hello, world")



async def connect(request):
    # Create Invitation
    # wait for the coroutine to finish
    invite = None
    with async_timeout.timeout(2):

        invite = await agent_controller.connections.create_invitation()
        return web.Response(text=invite["invitation_url"])



if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/', hello),
                    web.get('/connect', connect)])
    web.run_app(app, path="0.0.0.0", port="5000")