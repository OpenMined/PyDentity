from aiohttp import web
from aries_basic_controller.aries_controller import AriesAgentController
import qrcode
import asyncio
import async_timeout
import requests
from bs4 import BeautifulSoup

WEBHOOK_HOST = "0.0.0.0"
WEBHOOK_PORT = 8052
WEBHOOK_BASE = ""
ADMIN_URL = "http://opus-agent:8051"

# Based on the aca-py agent you wish to control
agent_controller = AriesAgentController(webhook_host=WEBHOOK_HOST, webhook_port=WEBHOOK_PORT,
                                   webhook_base=WEBHOOK_BASE, admin_url=ADMIN_URL)

asyncio.get_event_loop().run_until_complete(agent_controller.listen_webhooks())


async def hello(request):

    # ownership_proof = secrets.token_hex(16)
    ownership_proof = "53a4198707658f2b0402af57441aa380"

    str = open('templates/form.html', 'r').read()
    str = str.replace("$$OPUS$$", ownership_proof, 2)

    return web.Response(text=str, content_type='text/html')

async def github_openmined_credential(request):
    data = await request.post()
    user = data['user']
    ownership_proof= data['ownership_proof']

    #Retrieve Page
    http_response = requests.get("https://github.com/"+user)

    #Parse Account info for ownership token
    soup = BeautifulSoup(http_response.text)
    ownership_token = soup.findAll("div", {"class": "user-profile-bio"})[0].findAll("div")[0].text.strip()
    ownership_token = ownership_token.split("#OPUS ",1)[1].split("==",1)[0]

    # If the ownership proof is present
    if ownership_token == ownership_proof:
        soup = BeautifulSoup(http_response.text)

        orgsSection = soup.findAll("div", {"class": "border-top pt-3 mt-3 clearfix hide-sm hide-md"})[0].findAll('img')
        myOrgs = set(tag['alt'] for tag in orgsSection)

        # If the user is a member of OpenMined
        if '@OpenMined' in myOrgs:


            #Set the credential
            credential_attributes = [
                {"name": "Username", "value": user},
                {"name": "OpenMined Member", "value": "1"}
            ]

            #Send the credential to the user
            #TODO: 
                # - link connection in this session to connection initiated previously
                # - define credential and scheme on ledger
            record = await agent_controller.issuer.send_credential(connection_id, schema_id, cred_def_id, credential_attributes, trace=False)

        else:
            return web.Response(text="Unable to link to OpenMined.", content_type='text/html')
    else:
        return web.Response(text="Unable to link.", content_type='text/html')


async def connect(request):
    # Create Invitation
    # wait for the coroutine to finish
    invite = None
    with async_timeout.timeout(2):

        invite = await agent_controller.connections.create_invitation()
        return web.Response(text=invite["invitation_url"])



if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/', hello),
                    web.post('/github_openmined_credential', github_openmined_credential),
                    web.get('/connect', connect)])
    web.run_app(app, path="0.0.0.0", port="5000")
