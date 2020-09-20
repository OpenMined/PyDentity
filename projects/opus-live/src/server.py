from quart import Quart
from aries_basic_controller.aries_controller import AriesAgentController
import qrcode
import asyncio

app = Quart(__name__)

WEBHOOK_HOST = "0.0.0.0"
WEBHOOK_PORT = 8052
WEBHOOK_BASE = ""
ADMIN_URL = "http://opus-agent:8051"

# Based on the aca-py agent you wish to control
agent_controller = AriesAgentController(webhook_host=WEBHOOK_HOST, webhook_port=WEBHOOK_PORT,
                                   webhook_base=WEBHOOK_BASE, admin_url=ADMIN_URL)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

@app.route('/')
def home():
    return "Hello"

@app.route("/connect")
async def connect():
    # Create Invitation
    invite = await agent_controller.connections.create_invitation()
    # wait for the coroutine to finish


    connection_id = invite["connection_id"]
    inviteURL = invite['invitation_url']
    # Link for connection invitation
    input_data = inviteURL
    # Creating an instance of qrcode
    qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5)
    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('issuer_agent_invite_QRcode.png')
    from IPython.display import Image
    qr_code = Image(width=400, filename='./issuer_agent_invite_QRcode.png')
    return qr_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
