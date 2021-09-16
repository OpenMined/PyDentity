from typing import Optional
from aiohttp.client import ClientSession

from aries_cloudcontroller.client import Client
from aries_cloudcontroller.util.pydantic_converter import PydanticConverter


class AcaPyClient(Client):
    def __init__(
        self,
        base_url: str,
        *,
        api_key: Optional[str] = None,
        admin_insecure: Optional[bool] = False,
        tenant_jwt: Optional[str] = None,
    ):

        if not api_key and not admin_insecure:
            raise Exception(
                "api_key property is missing. Use admin_insecure=True if you want"
                " to use the controller without authentication."
            )

        headers = {}

        if api_key:
            headers["x-api-key"] = api_key
        if tenant_jwt:
            headers["authorization"] = f"Bearer {tenant_jwt}"

        client_session = ClientSession(
            headers=headers,
            raise_for_status=True,
        )

        super().__init__(
            base_url,
            client=client_session,
            extra_service_params={"converter": PydanticConverter()},
        )
