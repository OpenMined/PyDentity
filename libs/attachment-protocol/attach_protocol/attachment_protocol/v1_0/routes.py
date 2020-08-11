# Attachment Protocol admin routes

from marshmallow import fields, Schema
from aiohttp import web
from aiohttp_apispec import docs, match_info_schema, form_schema, request_schema, response_schema
from aries_cloudagent.connections.models.connection_record import ConnectionRecord
from aries_cloudagent.messaging.valid import UUIDFour
from aries_cloudagent.storage.error import StorageNotFoundError

from .messages.attachment import Attachment

class FileSchema(Schema):
    upfile = fields.Raw(
        description="File upload", required=True, type="file",
    )


class AttachmentMessageSchema(Schema):
    content = fields.Str(description="Message content", example="What UP!")

class ConnIdMatchInfoSchema(Schema):
    """Path parameters and validators for request taking connection id."""

    conn_id = fields.Str(
        description="Connection identifier", required=True, example=UUIDFour.EXAMPLE
    )

@docs(tags=["attachment protocol routes"], summary= "Attach file")
@match_info_schema(ConnIdMatchInfoSchema())
@form_schema(FileSchema())
async def connections_send_message(request: web.BaseRequest):
    """
    Request Handler to send attachment protocol
    """
    context = request.app["request_context"]
    connection_id = request.match_info["conn_id"]
    outbound_handler = request.app["outbound_message_router"]

    # WARNING: don't do that if you plan to receive large files!
    data = await request.post()

    upfile = data['upfile']


    # .filename contains the name of the file in string format.
    filename = upfile.filename
    print("filename", filename)
    content_type = upfile.content_type

    # .file contains the actual file data that needs to be stored somewhere.
    file = upfile.file

    content = file.read()

    try:
        connection = await ConnectionRecord.retrieve_by_id(context, connection_id)
    except StorageNotFoundError:
        raise web.HTTPNotFound()

    if not connection.is_ready:
        raise web.HTTPBadRequest()


    # await outbound_handler(msg, connection_id=connection_id)



    return web.Response(text="success")

async def register(app: web.Application):
    """Register routes."""

    app.add_routes(
        [web.post("/connections/{conn_id}/test-attachmentprotocol", connections_send_message)]
    )