
PROTOCOL_URI ="did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/attachmentprotocol/1.0"

ATTACHMENT_PROTOCOL = f"{PROTOCOL_URI}/attachmentprotocol"

NEW_PROTOCOL_URI ="https://didcomm.org/attachmentprotocol/1.0"

NEW_ATTACHMENT_PROTOCOL = f"{NEW_PROTOCOL_URI}/attachmentprotocol"

PROTOCOL_PACKAGE ="attachment_protocol.v1_0"

MESSAGE_TYPES = {
    ATTACHMENT_PROTOCOL: f"{PROTOCOL_PACKAGE}.messaging.attachmentprotocol.AttachmentProtocol",
    NEW_ATTACHMENT_PROTOCOL: f"{PROTOCOL_PACKAGE}.messages.attachmentprotocol.AttachmentProtocol",
}