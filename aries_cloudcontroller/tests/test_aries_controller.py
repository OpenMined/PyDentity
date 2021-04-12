import logging
import pytest

from ..aries_webhook_server import AriesWebhookServer
from ..controllers.multitenant import MultitenancyController

from ..aries_controller import AriesAgentController

LOGGER = logging.getLogger(__name__)


class TestAriesAgentController():

    admin_url = "0.0.0.0"
    webhook_host = ""
    webhook_port = 8000
    webhook_base = ""

    @pytest.mark.asyncio
    async def test_init_args_missing(self):
        with pytest.raises(TypeError) as te:
            AriesAgentController()
            assert "__init__() missing 1 required positional argument: \
                'admin_url'" in str(te.value)

    @pytest.mark.asyncio
    async def test_init_args_multi_default(self):
        ac = AriesAgentController(admin_url=self.admin_url)
        assert not ac.is_multitenant

    @pytest.mark.asyncio
    async def test_init_args_multi_true(self):
        ac = AriesAgentController(
            admin_url=self.admin_url,
            is_multitenant=True)
        assert ac.is_multitenant
        assert type(ac.multitenant) == MultitenancyController
        assert ac.multitenant.admin_url == self.admin_url
        assert ac.multitenant.client_session.headers == {}
        await ac.terminate()

    @pytest.mark.asyncio
    async def test_init_webhook_server(self):
        ac = AriesAgentController(
            admin_url=self.admin_url,
            is_multitenant=True)
        ac.init_webhook_server(
            self.webhook_host,
            self.webhook_port,
            self.webhook_base
        )
        assert type(ac.webhook_server) == AriesWebhookServer
        assert ac.webhook_server.webhook_base == self.webhook_base
        assert ac.webhook_server.webhook_port == self.webhook_port
        assert ac.webhook_server.webhook_host == self.webhook_host
        assert ac.webhook_server.is_multitenant
        await ac.terminate()

    @pytest.mark.asyncio
    async def test_listen_webhooks_error(self, caplog):
        caplog.set_level(logging.WARNING)
        ac = AriesAgentController(
            admin_url=self.admin_url,
            is_multitenant=True)
        with pytest.raises(AttributeError) as ae:
            await ac.listen_webhooks()
        assert "Webhook server not initialised." in str(ae.value)
        assert "Webhook server not initialised." in caplog.text
        await ac.terminate()

    @pytest.mark.asyncio
    async def test_init_webhook_server_terminate(self, caplog):
        caplog.set_level(logging.INFO)
        ac = AriesAgentController(
            admin_url=self.admin_url,
            is_multitenant=True)
        ac.init_webhook_server(
            self.webhook_host,
            self.webhook_port,
            self.webhook_base
        )
        await ac.listen_webhooks()
        assert "Webhook server started." in caplog.text
        res = await ac.webhook_server.terminate()
        assert "Webhook server terminated." in caplog.text
        assert res is None
        await ac.terminate()
