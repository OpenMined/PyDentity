import logging
import re
import pytest
import pytest_asyncio
from aiohttp import (
    web,
    ClientSession,
)

from ..aries_webhook_server import AriesWebhookServer
from ..controllers.multitenant import MultitenancyController

from ..aries_tenant_controller import AriesTenantController

LOGGER = logging.getLogger(__name__)


class TestAriesTenantController():

    admin_url = "0.0.0.0"
    webhook_host = ""
    webhook_port = 8000
    webhook_base = ""
    wallet_id = "123456789"
    tenant_jwt = "987654321"

    @pytest.mark.asyncio
    async def test_init_args_missing_wallet_id(self):
        with pytest.raises(
                TypeError, 
                match=re.escape("__init__ missing required wallet_id (str)")):
            AriesTenantController(admin_url=self.admin_url)

    @pytest.mark.asyncio
    async def test_init_args_missing_tenant_jwt(self):
        with pytest.raises(
                TypeError, 
                match=re.escape("__init__ missing required tenant_jwt (str)")):
            AriesTenantController(admin_url=self.admin_url, wallet_id=self.wallet_id)

    @pytest.mark.asyncio
    async def test_init_webhook_server(self):
        ac = AriesTenantController(
            admin_url=self.admin_url,
            wallet_id=self.wallet_id,
            tenant_jwt=self.tenant_jwt)
        with pytest.raises(
                NotImplementedError,
                match=("Please, use an AriesAgentController to start a webhook server\n"
                    "Webhook server fct is disallowed for tenant controllers.")):
            ac.init_webhook_server()
        await ac.terminate()

    @pytest.mark.asyncio
    async def test_listen_webhooks(self):
        ac = AriesTenantController(
            admin_url=self.admin_url,
            wallet_id=self.wallet_id,
            tenant_jwt=self.tenant_jwt)
        with pytest.raises(
                NotImplementedError,
                match=("Please, use an AriesAgentController to start a webhook server\n"
                    "Webhook server fct is disallowed for tenant controllers.")):
            ac.listen_webhooks()
        await ac.terminate()

    @pytest.mark.asyncio
    async def test_update_wallet_id(self):
        new_wallet_id = "567438291"
        ac = AriesTenantController(
            admin_url=self.admin_url,
            wallet_id=self.wallet_id,
            tenant_jwt=self.tenant_jwt)
        assert ac.wallet_id != new_wallet_id
        ac.update_wallet_id(wallet_id=new_wallet_id)
        assert ac.wallet_id == new_wallet_id
        with pytest.raises(
                AssertionError,
                match="wallet_id must not be empty"):
            ac.update_wallet_id(wallet_id="")
        with pytest.raises(
                AssertionError,
                match="wallet_id must be a string"):
            ac.update_wallet_id(wallet_id=23456)
        await ac.terminate()

    @pytest.mark.asyncio
    async def test_update_tenant_jwt(self):
        new_tenant_jwt = "567438291"
        ac = AriesTenantController(
            admin_url=self.admin_url,
            wallet_id=self.wallet_id,
            tenant_jwt=self.tenant_jwt)
        assert ac.tenant_jwt != new_tenant_jwt
        ac.update_tenant_jwt(wallet_id=self.wallet_id, tenant_jwt=new_tenant_jwt)
        assert ac.tenant_jwt == new_tenant_jwt
        with pytest.raises(
                AssertionError,
                match="tenant_jwt must not be empty"):
            ac.update_tenant_jwt(wallet_id=self.wallet_id, tenant_jwt="")
        with pytest.raises(
                AssertionError,
                match="tenant_jwt must be a string"):
            ac.update_tenant_jwt(wallet_id=self.wallet_id, tenant_jwt=23456)
        await ac.terminate()

    @pytest.mark.asyncio
    async def test_remove_tenant_jwt(self):
        ac = AriesTenantController(
            admin_url=self.admin_url,
            wallet_id=self.wallet_id,
            tenant_jwt=self.tenant_jwt)
        ac.remove_tenant_jwt()
        assert not ac.tenant_jwt
        assert 'Authorization' not in ac.headers
        assert 'Authorization' not in  ac.client_session.headers
        assert 'content-type' not in  ac.client_session.headers
        assert 'content-type' not in  ac.headers
        await ac.terminate()
