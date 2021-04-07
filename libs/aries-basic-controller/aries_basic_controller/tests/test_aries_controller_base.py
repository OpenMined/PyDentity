import pytest
import pytest_asyncio
from aiohttp import (
    ClientSession,
)

from ..aries_controller_base import AriesAgentControllerBase
from ..controllers.connections import ConnectionsController
from ..controllers.messaging import MessagingController
from ..controllers.mediation import MediationController
from ..controllers.schema import SchemaController
from ..controllers.wallet import WalletController
from ..controllers.definitions import DefinitionsController
from ..controllers.issuer import IssuerController
from ..controllers.proof import ProofController
from ..controllers.ledger import LedgerController
from ..controllers.credential import CredentialController
from ..controllers.server import ServerController
from ..controllers.oob import OOBController
from ..controllers.action_menu import ActionMenuController
from ..controllers.revocation import RevocationController

# @pytest.fixture()
# def base_controller(**kwargs):
#     return AriesAgentControllerBase(**kwargs)

class TestAriesAgentControllerBase():

    @pytest.mark.asyncio
    async def test_init_args_missing(self):
        with pytest.raises(TypeError) as te:
            AriesAgentControllerBase()
            assert "__init__() missing 1 required positional argument: 'admin_url'" \
                in str(tf.value)
    
    @pytest.mark.asyncio
    async def test_default_args(self):
        ac = AriesAgentControllerBase(admin_url="0.0.0.0")
        assert ac.admin_url == "0.0.0.0"
        assert ac.api_key == None
        assert ac.webhook_site == None
        assert ac.connections_controller == None
        assert type(ac.client_session) == ClientSession
        assert type(ac.connections) == ConnectionsController
        assert type(ac.messaging) == MessagingController
        assert type(ac.proofs) == ProofController
        assert type(ac.ledger) == LedgerController
        assert type(ac.credentials) == CredentialController
        assert type(ac.server) == ServerController
        assert type(ac.oob) == OOBController
        assert type(ac.mediation) == MediationController
        assert type(ac.schema) == SchemaController
        assert type(ac.wallet) == WalletController
        assert type(ac.definitions) == DefinitionsController
        assert type(ac.issuer) == IssuerController
        assert type(ac.action_menu) == ActionMenuController
        assert type(ac.revocations) == RevocationController
        await ac.terminate()

    @pytest.mark.asyncio
    async def test_headers(self):
        api_key = "123456789"
        ac = AriesAgentControllerBase(admin_url="", api_key=api_key)
        exp_headers = {"X-API-Key": api_key}
        assert ac.headers == exp_headers
        await ac.terminate()

    @pytest.mark.asyncio
    async def test_init_webhook_server(self):
        ac = AriesAgentControllerBase(admin_url="0.0.0.0")
        with pytest.raises(NotImplementedError):
            ac.init_webhook_server()
        await ac.terminate()

    @pytest.mark.asyncio
    async def test_update_api_key(self):
        api_key = "123456789"
        ac = AriesAgentControllerBase(admin_url="", api_key=api_key)
        exp_headers = {"X-API-Key": api_key}
        assert ac.headers == exp_headers
        assert ac.client_session.headers == exp_headers

        new_api_key = "987654321"
        ac.update_api_key(new_api_key)
        new_exp_headers = {"X-API-Key": new_api_key}
        assert ac.headers == new_exp_headers
        assert ac.client_session.headers == new_exp_headers

        await ac.terminate()
    
    @pytest.mark.asyncio
    async def test_remove_api_key(self):
        api_key = "123456789"
        ac = AriesAgentControllerBase(admin_url="", api_key=api_key)
        exp_headers = {"X-API-Key": api_key}
        ac.remove_api_key()
        assert ac.headers == {}
        assert ac.client_session.headers == {}
        await ac.terminate()
    
    # TODO create mock for pubsub listening webhooks
    # Maybe this makes more sense in aries_controller
    @pytest.mark.asyncio
    async def test_register_listners(self):
        pass

    @pytest.mark.asyncio
    async def test_add_listener(self):
        pass

    @pytest.mark.asyncio
    async def test_remove_listener(self):
        pass

    @pytest.mark.asyncio
    async def test_remove_all_listeners(self):
        pass

    @pytest.mark.asyncio
    async def test_listen_webhooks(self):
        ac = AriesAgentControllerBase(admin_url="0.0.0.0")
        with pytest.raises(NotImplementedError):
            await ac.listen_webhooks()
        await ac.terminate()

    @pytest.mark.asyncio
    async def test_terminate(self):
        ac = AriesAgentControllerBase(admin_url="0.0.0.0")
        await ac.terminate()
        assert ac.client_session.closed == True
        with pytest.raises(AttributeError):
            assert ac.webhook_server == None
        await ac.terminate()
