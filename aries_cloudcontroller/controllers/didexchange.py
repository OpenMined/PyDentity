from .base import BaseController
from aiohttp import ClientSession
import logging

logger = logging.getLogger("aries_controller.didexchange")


class DidExchangeController(BaseController):
    def __init__(self, admin_url: str, client_session: ClientSession):
        super().__init__(admin_url, client_session)

    async def create_request_against_invite(
        self,
        their_pub_id: str,
        mediation_id: str = None,
        my_endpoint: str = None,
        my_label: str = None,
    ):
        params = {}
        if mediation_id:
            params["mediation_id"] = mediation_id
        if my_endpoint:
            params["my_endpoint"] = my_endpoint
        if my_label:
            params["my_label"] = my_label
        response = self.admin_POST(f"/didexchange/create-request", params=params)
        return response

    print(params)

    async def receive_request_against_invite(
        self,
        body: {} = None,
        alias: str = None,
        auto_accept: bool = None,
        mediation_id: str = None,
        my_endpoint: str = None,
    ):
        params = {}
        if alias:
            params["alias"] = alias
        if auto_accept:
            params["auto_accept"] = auto_accept
        if mediation_id:
            params["mediation_id"] = mediation_id
        if my_endpoint:
            params["my_endpoint"] = my_endpoint
        if body:
            response = self.admin_POST(
                f"/didexchange/receive-request", body=body, params=params
            )
        else:
            response = self.admin_POST(f"/didexchange/receive-request", params=params)
        return response

    async def accept_invitation(
        self, connection_id: str, my_endpoint: str = None, my_label: str = None
    ):
        params = {}
        if my_endpoint:
            params["my_endpoint"] = my_endpoint
        if my_label:
            params["my_label"] = my_label
        response = self.admin_POST(
            f"/didexchange/{connection_id}/accept-invitation", params=params
        )
        return response

    async def accept_stored_invite(
        self, connection_id: str, mediation_id: str = None, my_endpoint: str = None
    ):
        params = {}
        if mediation_id:
            params["mediation_id"] = mediation_id
        if my_endpoint:
            params["my_endpoint"] = my_endpoint
        response = self.admin_POST(
            f"/didexchange/{connection_id}/accept-request", params=params
        )
