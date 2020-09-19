import os
import asyncio
import time

from aries_basic_controller.aries_controller import AriesAgentController

from dotenv import load_dotenv


load_dotenv()

BLUE_ADMIN_URL = os.getenv('BLUE_ADMIN_URL')
BLUE_WEBHOOK_PORT = os.getenv('BLUE_WEBHOOK_PORT')
BLUE_WEBHOOK_HOST = os.getenv('BLUE_WEBHOOK_HOST')
BLUE_WEBHOOK_BASE = os.getenv('BLUE_WEBHOOK_BASE')

RED_ADMIN_URL = os.getenv('RED_ADMIN_URL')
RED_WEBHOOK_PORT = os.getenv('RED_WEBHOOK_PORT')
RED_WEBHOOK_HOST = os.getenv('RED_WEBHOOK_HOST')
RED_WEBHOOK_BASE = os.getenv('RED_WEBHOOK_BASE')

YELLOW_ADMIN_URL = os.getenv('YELLOW_ADMIN_URL')
YELLOW_WEBHOOK_PORT = os.getenv('YELLOW_WEBHOOK_PORT')
YELLOW_WEBHOOK_HOST = os.getenv('YELLOW_WEBHOOK_HOST')
YELLOW_WEBHOOK_BASE = os.getenv('YELLOW_WEBHOOK_BASE')

ALICE_ADMIN_URL = os.getenv('ALICE_ADMIN_URL')
ALICE_WEBHOOK_PORT = os.getenv('ALICE_WEBHOOK_PORT')
ALICE_WEBHOOK_HOST = os.getenv('ALICE_WEBHOOK_HOST')
ALICE_WEBHOOK_BASE = os.getenv('ALICE_WEBHOOK_BASE')


async def start_agent():

    time.sleep(6)

    # Define vote controllers
    red_agent_controller = AriesAgentController(webhook_host=RED_WEBHOOK_HOST, webhook_port=RED_WEBHOOK_PORT,
                                               webhook_base=RED_WEBHOOK_BASE, admin_url=RED_ADMIN_URL)

    blue_agent_controller = AriesAgentController(webhook_host=BLUE_WEBHOOK_HOST, webhook_port=BLUE_WEBHOOK_PORT,
                                               webhook_base=BLUE_WEBHOOK_BASE, admin_url=BLUE_ADMIN_URL)

    yellow_agent_controller = AriesAgentController(webhook_host=YELLOW_WEBHOOK_HOST, webhook_port=YELLOW_WEBHOOK_PORT,
                                               webhook_base=YELLOW_WEBHOOK_BASE, admin_url=YELLOW_ADMIN_URL)

    await blue_agent_controller.listen_webhooks()
    await red_agent_controller.listen_webhooks()
    await yellow_agent_controller.listen_webhooks()

    red_agent_controller.register_listeners([], defaults=True)
    blue_agent_controller.register_listeners([], defaults=True)
    yellow_agent_controller.register_listeners([], defaults=True)

    # Define voters
    alice_agent_controller = AriesAgentController(webhook_host=ALICE_WEBHOOK_HOST, webook_port=ALICE_WEBHOOK_PORT,
                                                webhook_base=ALICE_WEBHOOK_BASE, admin_url=ALICE_ADMIN_URL)

    await alice_agent_controller.listen_webhooks()

    alice_agent_controller.register_listengers([], defaults=True)

    # Connect Red to Blue
    invite = await red_agent_controller.connections.create_invitation()
    print("Invite", invite)

    red_connection_id = invite["connection_id"]

    response = await blue_agent_controller.connections.accept_connection(invite["invitation"])
    print(response)

    print("Blue ID", response["connection_id"])
    blue_id = response["connection_id"]
    print("Invite Accepted")
    print(response)

    time.sleep(2)

    connection = await red_agent_controller.connections.accept_request(red_connection_id)
    print("ACCEPT REQUEST")
    print(connection)

    connection = await red_agent_controller.connections.get_connection(red_connection_id)
    print("RED AGENT CONNECTION")
    print(connection)

    while connection["state"] != "active":
        trust_ping = await red_agent_controller.messaging.trust_ping(red_connection_id, "hello")
        print("TUST PING TO ACTIVATE CONNECTION - RED -> RESEARCH")
        print(trust_ping)
        time.sleep(5)
        connection = await red_agent_controller.connections.get_connection(red_connection_id)

    trust_ping = await blue_agent_controller.messaging.trust_ping(blue_id,"hello")
    print("TUST PING TO ACTIVATE CONNECTION - RESEARCH -> RED")
    print(trust_ping)

    print("BLUE ID {} RED ID {}".format(blue_id, red_connection_id))

    connection = await red_agent_controller.connections.get_connection(red_connection_id)
    print("RED AGENT CONNECTION")
    print(connection)

    connection = await blue_agent_controller.connections.get_connection(blue_id)
    print("RESEARCH AGENT CONNECTION")
    print(connection)

    time.sleep(2)

    # Connect Red to Yellow
    invite = await red_agent_controller.connections.create_invitation()
    print("Invite", invite)

    red_connection_id = invite["connection_id"]

    response = await yellow_agent_controller.connections.accept_connection(invite["invitation"])
    print(response)

    print("Yellow ID", response["connection_id"])
    yellow_id = response["connection_id"]
    print("Invite Accepted")
    print(response)

    time.sleep(2)

    connection = await red_agent_controller.connections.accept_request(red_connection_id)
    print("ACCEPT REQUEST")
    print(connection)

    connection = await red_agent_controller.connections.get_connection(red_connection_id)
    print("RED AGENT CONNECTION")
    print(connection)

    while connection["state"] != "active":
        trust_ping = await red_agent_controller.messaging.trust_ping(red_connection_id, "hello")
        print("TUST PING TO ACTIVATE CONNECTION - RED -> YELLOW")
        print(trust_ping)
        time.sleep(5)
        connection = await red_agent_controller.connections.get_connection(red_connection_id)

    trust_ping = await yellow_agent_controller.messaging.trust_ping(yellow_id,"hello")
    print("TUST PING TO ACTIVATE CONNECTION - YELLOW -> RED")
    print(trust_ping)

    print("YELLOW ID {} RED ID {}".format(yellow_id, red_connection_id))

    connection = await red_agent_controller.connections.get_connection(red_connection_id)
    print("RED-YELLOW AGENT CONNECTION")
    print(connection)

    connection = await yellow_agent_controller.connections.get_connection(yellow_id)
    print("YELLOW-RED AGENT CONNECTION")
    print(connection)

    # Connect Red to Alice
    invite = await red_agent_controller.connections.create_invitation()
    print("Invite", invite)

    red_connection_id = invite["connection_id"]

    response = await alice_agent_controller.connections.accept_connection(invite["invitation"])
    print(response)

    print("Alice ID", response["connection_id"])
    alice_id = response["connection_id"]
    print("Invite Accepted")
    print(response)

    time.sleep(2)

    connection = await red_agent_controller.connections.accept_request(red_connection_id)
    print("ACCEPT REQUEST")
    print(connection)

    connection = await red_agent_controller.connections.get_connection(red_connection_id)
    print("RED AGENT CONNECTION")
    print(connection)

    while connection["state"] != "active":
        trust_ping = await red_agent_controller.messaging.trust_ping(red_connection_id, "hello")
        print("TUST PING TO ACTIVATE CONNECTION - RED -> ALICE")
        print(trust_ping)
        time.sleep(5)
        connection = await red_agent_controller.connections.get_connection(red_connection_id)

    trust_ping = await alice_agent_controller.messaging.trust_ping(alice_id,"hello")
    print("TUST PING TO ACTIVATE CONNECTION - ALICE -> RED")
    print(trust_ping)

    print("ALICE ID {} RED ID {}".format(alice_id, red_connection_id))

    connection = await red_agent_controller.connections.get_connection(red_connection_id)
    print("RED-ALICE AGENT CONNECTION")
    print(connection)

    connection = await alice_agent_controller.connections.get_connection(alice_id)
    print("ALICE-RED AGENT CONNECTION")
    print(connection)

    print("SUCCESS")
    time.sleep(2)

    # Clean up
    await red_agent_controller.terminate()
    await blue_agent_controller.terminate()
    await yellow_agent_controller.terminate()

    await alice_agent_controller.terminate()


if __name__ == "__main__":
    # time.sleep(60)
    try:
        asyncio.get_event_loop().run_until_complete(start_agent())
    except KeyboardInterrupt:
        os._exit(1)
