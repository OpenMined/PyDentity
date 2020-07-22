""" Protocol for attachment message"""

from ..message_types import PROTOCOL_PACKAGE, ATTACHMENT_PROTOCOL

from marshmallow import fields

from aries_cloudagent.messaging.agent_message import AgentMessage, AgentMessageSchema

HANDLER_CLASS = f"{PROTOCOL_PACKAGE}.handlers.attachmentprotocol_handler.AttachmentProtocolHandler"

class AttachmentProtocol(AgentMessage):
    #Class representing message attachment

    class Meta:
        handler_class = HANDLER_CLASS
        message_type = ATTACHMENT_PROTOCOL
        schema_class = "AttachmentProtocolSchema"

    def __init__(

        self,
        *, 
        content: str = None,
        localization: str = None,
        **kwargs,
    ):
        super(AttachmentProtocol, self).__init__(**kwargs)
        self.content = content
        if localization:
            self._decorators["l10n"] = localization

        
class AttachmentProtocolSchema(AgentMessageSchema):
    #Schema for Attachment protocol class

    class Meta:
        #Metadata

        model_class = AttachmentProtocol
    
    content = fields.Str(required=True, description="Message content", example="Hello")
