import asyncio

from aries_cloudcontroller import AcaPyClient, CreateInvitationRequest

client = AcaPyClient(base_url="https://agent.community.animo.id", admin_insecure=True)


async def run():
    result = await client.connection.create_invitation(
        body=CreateInvitationRequest(my_label="Cloud Controller")
    )

    connection = await client.connection.receive_invitation(body=result.invitation)

    print(connection)


asyncio.get_event_loop().run_until_complete(run())
