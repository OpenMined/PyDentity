import logging
import re
import pytest

from ..aries_webhook_server import AriesWebhookServer

LOGGER = logging.getLogger(__name__)


class TestAriesWebhookServer():

    webhook_host = ""
    webhook_port = 8000
    webhook_base = ""

    @pytest.mark.asyncio
    async def test_init_args_missing_webhook_host(self):
        with pytest.raises(
                TypeError,
                match=re.escape(
                    "__init__() missing 1 required positional argument: 'webhook_host'"
                )):
            AriesWebhookServer(
                webhook_port=self.webhook_port,
                webhook_base=self.webhook_base)

    @pytest.mark.asyncio
    async def test_init_args_missing_webhook_port(self):
        with pytest.raises(
                TypeError, 
                match=re.escape(
                    "__init__() missing 1 required positional argument: 'webhook_port'"
                )):
            AriesWebhookServer(
                webhook_host=self.webhook_host,
                webhook_base=self.webhook_base)

    @pytest.mark.asyncio
    async def test_listen_webhooks(self, caplog):
        caplog.set_level(logging.INFO)
        aws = AriesWebhookServer(
                webhook_host=self.webhook_host,
                webhook_port=self.webhook_port)
        await aws.listen_webhooks()
        assert f"Listening Webhooks on {aws.webhook_host}:{aws.webhook_port}" in caplog.text
        await aws.terminate()

    # TODO create mocks for pubsub webhook handling
    # Not quite sure how to do this best

    @pytest.mark.asyncio
    async def test_terminate(self, caplog):
        caplog.set_level(logging.INFO)
        aws = AriesWebhookServer(
                webhook_host=self.webhook_host,
                webhook_port=self.webhook_port)
        assert await aws.terminate() is None

        aws = AriesWebhookServer(
                webhook_host=self.webhook_host,
                webhook_port=self.webhook_port)
        await aws.listen_webhooks()
        await aws.terminate()
        assert "Webhook server terminated." in caplog.text
