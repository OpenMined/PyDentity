from aries_basic_controller.aries_controller import AriesAgentController
from .protocol_controller import ProtocolController


class OMAriesController(AriesAgentController):

    def __init__(self, webhook_host: str, webhook_port: int, admin_url: str, webhook_base: str = "",
                 connections: bool = True, messaging: bool = True, issuer: bool = True):
        super().__init__(self, webhook_host, webhook_port, admin_url, webhook_base,
                         connections, messaging, issuer)

        self.protocol = ProtocolController(admin_url, self.client_session)
