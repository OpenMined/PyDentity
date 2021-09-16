import logging
import re
import pytest

from aries_cloudcontroller.acapy_client import AcaPyClient

LOGGER = logging.getLogger(__name__)


class TestAcaPyClient:
    admin_host = "http://localhost:1000"
    api_key = "api_key"

    @pytest.mark.asyncio
    async def test_init_acapy_client(self):
        client = AcaPyClient(self.admin_host, api_key=self.api_key)
        assert type(client) is AcaPyClient

    @pytest.mark.asyncio
    async def test_init_args_missing_api_key_no_insecure_mode(self):
        with pytest.raises(
            Exception,
            match=re.escape("api_key property is missing"),
        ):
            AcaPyClient(self.admin_host)
