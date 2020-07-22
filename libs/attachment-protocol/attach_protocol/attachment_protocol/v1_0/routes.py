# Attachment Protocol admin routes

from marshmallow import fields, Schema
from aiohttp import web
from aiohttp_apispec import docs, match_info_schema, request_schema, response_schema
from aries_cloudagent.connections.models.connection_record import ConnectionRecord
from aries_cloudagent.messaging.valid import UUIDFour
from aries_cloudagent.storage.error import StorageNotFoundError

from .messages.attachmentprotocol import AttachmentProtocol

class SendMessageSchema(Schema):
    content = fields.Str(description="Message content", example="What UP!")

class ConnIdMatchInfoSchema(Schema):
    """Path parameters and validators for request taking connection id."""

    conn_id = fields.Str(
        description="Connection identifier", required=True, example=UUIDFour.EXAMPLE
    )

@docs(tags=["attachment protocol routes"], summary= "Sending message")
@match_info_schema(ConnIdMatchInfoSchema())
@request_schema(SendMessageSchema())

async def connections_send_message(request: web.BaseRequest):
    """
    Request Handler to send attachment protocol
    """
    context = request.app["request_context"]
    connection_id = request.match_info["conn_id"]
    outbound_handler = request.app["outbound_message_router"]
    params = await request.json()
    try:
        connection = await ConnectionRecord.retrieve_by_id(context, connection_id)
    except StorageNotFoundError:
        raise web.HTTPNotFound()

    if connection.is_ready:
        msg = AttachmentProtocol(
            content=params["content"]
            )
        
        await outbound_handler(msg, connection_id=connection_id)

    return web.json_response({})   

async def register(app: web.Application):
    """Register routes."""

    app.add_routes(
        [web.post("/connections/{conn_id}/test-attachmentprotocol", connections_send_message)]
    )