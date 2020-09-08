import os
import asyncio
import time

from aries_basic_controller.aries_controller import AriesAgentController

from dotenv import load_dotenv
load_dotenv()

ALICE_ADMIN_URL = os.getenv('ALICE_ADMIN_URL')
ALICE_WEBHOOK_PORT = os.getenv('ALICE_WEBHOOK_PORT')
ALICE_WEBHOOK_HOST = os.getenv('ALICE_WEBHOOK_HOST')
ALICE_WEBHOOK_BASE = os.getenv('ALICE_WEBHOOK_BASE')
ALICE_API_KEY = os.getenv('ALICE_API_KEY')

BOB_ADMIN_URL = os.getenv('BOB_ADMIN_URL')
BOB_WEBHOOK_PORT = os.getenv('BOB_WEBHOOK_PORT')
BOB_WEBHOOK_HOST = os.getenv('BOB_WEBHOOK_HOST')
BOB_WEBHOOK_BASE = os.getenv('BOB_WEBHOOK_BASE')





async def start_agent():

    time.sleep(6)

    bob_agent_controller = AriesAgentController(webhook_host=BOB_WEBHOOK_HOST, webhook_port=BOB_WEBHOOK_PORT,
                                               webhook_base=BOB_WEBHOOK_BASE, admin_url=BOB_ADMIN_URL)



    alice_agent_controller = AriesAgentController(webhook_host=ALICE_WEBHOOK_HOST, webhook_port=ALICE_WEBHOOK_PORT,
                                               webhook_base=ALICE_WEBHOOK_BASE, admin_url=ALICE_ADMIN_URL, api_key=ALICE_API_KEY)


    await alice_agent_controller.listen_webhooks()

    await bob_agent_controller.listen_webhooks()


    bob_agent_controller.register_listeners([], defaults=True)
    alice_agent_controller.register_listeners([], defaults=True)

    invite = await bob_agent_controller.connections.create_invitation()
    print("Invite", invite)

    bob_connection_id = invite["connection_id"]

    response = await alice_agent_controller.connections.accept_connection(invite["invitation"])
    print(response)


    print("Alice ID", response["connection_id"])
    alice_id = response["connection_id"]
    print("Invite Accepted")
    print(response)


    time.sleep(2)

    connection = await bob_agent_controller.connections.accept_request(bob_connection_id)
    print("ACCEPT REQUEST")
    print(connection)

    connection = await bob_agent_controller.connections.get_connection(bob_connection_id)
    print("BOB AGENT CONNECTION")
    print(connection)

    while connection["state"] != "active":
        trust_ping = await bob_agent_controller.messaging.trust_ping(bob_connection_id, "hello")
        print("TUST PING TO ACTIVATE CONNECTION - BOB -> RESEARCH")
        print(trust_ping)
        time.sleep(5)
        connection = await bob_agent_controller.connections.get_connection(bob_connection_id)

    trust_ping = await alice_agent_controller.messaging.trust_ping(alice_id,"hello")
    print("TUST PING TO ACTIVATE CONNECTION - RESEARCH -> BOB")
    print(trust_ping)

    print("ALICE ID {} BOB ID {}".format(alice_id, bob_connection_id))

    connection = await bob_agent_controller.connections.get_connection(bob_connection_id)
    print("BOB AGENT CONNECTION")
    print(connection)

    connection = await alice_agent_controller.connections.get_connection(alice_id)
    print("RESEARCH AGENT CONNECTION")
    print(connection)

    print("SUCCESS")
    time.sleep(2)
    await bob_agent_controller.terminate()
    await alice_agent_controller.terminate()


if __name__ == "__main__":
    # time.sleep(60)
    try:
        asyncio.get_event_loop().run_until_complete(start_agent())
    except KeyboardInterrupt:
        os._exit(1)

