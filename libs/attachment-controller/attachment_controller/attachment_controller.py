from aries_basic_controller.aries_controller import AriesAgentController
from .protocol_controller import ProtocolController

from dataclasses import dataclass


@dataclass
class AttachmentController(AriesAgentController):

    def __post_init__(self):
        super().__post_init__()

        self.protocol = ProtocolController(
            self.admin_url, self.client_session, self.connections)
