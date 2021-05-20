from aiohttp import (
    ClientResponse,
    ClientError,
)

import logging

import json


LOGGER = logging.getLogger("__name__")


class repr_json:
    def __init__(self, val):
        self.val = val

    def __repr__(self) -> str:
        if isinstance(self.val, str):
            return self.val
        return json.dumps(self.val, indent=4)


class BaseController:
    def __init__(self, admin_url: str, client_session):
        self.admin_url = admin_url
        self.client_session = client_session
        self.color = None
        self.prefix = None

    @property
    def prefix_str(self):
        if self.prefix:
            return f"{self.prefix:10s} |"

    async def admin_request(
        self, method, path, json_data=None, text=False, params=None, data=None
    ) -> ClientResponse:
        params = {k: v for (k, v) in (params or {}).items() if v is not None}
        async with self.client_session.request(
            method, self.admin_url + path, json=json_data, params=params, data=data
        ) as resp:
            resp.raise_for_status()
            resp_text = await resp.text()
            if not resp_text and not text:
                return None
            if not text:
                try:
                    return json.loads(resp_text)
                except json.JSONDecodeError as e:
                    raise Exception(f"Error decoding JSON: {resp_text}") from e
            return resp_text

    async def admin_GET(self, path, text=False, params=None) -> ClientResponse:
        try:
            LOGGER.debug("Controller GET %s request to Agent", path)
            response = await self.admin_request("GET", path, None, text, params)
            LOGGER.debug(
                "Response from GET %s received: \n%s",
                path,
                repr_json(response),
            )
            return response
        except ClientError as e:
            LOGGER.error(f"Error during GET {path}: {str(e)}")
            raise

    async def admin_POST(
        self, path, json_data=None, text=False, params=None, data=None
    ) -> ClientResponse:
        try:
            LOGGER.debug(
                "Controller POST %s request to Agent%s",
                path,
                (" with data: \n{}".format(repr_json(json_data)) if json_data else ""),
            )
            response = await self.admin_request(
                "POST", path, json_data, text, params, data
            )
            LOGGER.debug(
                "Response from POST %s received: \n%s",
                path,
                repr_json(response),
            )
            return response
        except ClientError as e:
            LOGGER.error(f"Error during POST {path}: {str(e)}")
            raise

    async def admin_PATCH(
        self, path, json_data=None, text=False, params=None, data=None
    ) -> ClientResponse:
        try:
            LOGGER.debug(
                "Controller PATCH %s request to Agent%s",
                path,
                (" with data: \n{}".format(repr_json(json_data)) if json_data else ""),
            )
            response = await self.admin_request(
                "PATCH", path, json_data, text, params, data
            )
            LOGGER.debug(
                "Response from PATCH %s received: \n%s", path, repr_json(response)
            )
            return response
        except ClientError as e:
            LOGGER.error(f"Error during PATCH {path}: {str(e)}")
            raise

    async def admin_PUT(
        self, path, json_data=None, text=False, params=None, data=None
    ) -> ClientResponse:
        try:
            LOGGER.debug(
                "Controller PUT %s request to Agent%s",
                path,
                (" with data: \n{}".format(repr_json(json_data)) if json_data else ""),
            )
            response = await self.admin_request(
                "PUT", path, json_data, text, params, data
            )
            LOGGER.debug(
                "Response from PUT %s received: \n%s", path, repr_json(response)
            )
            return response
        except ClientError as e:
            LOGGER.error(f"Error during PUT {path}: {str(e)}")
            raise

    async def admin_DELETE(self, path, text=False, params=None) -> ClientResponse:
        try:
            LOGGER.debug("Controller DELETE %s request to Agent", path)

            response = await self.admin_request("DELETE", path, None, text, params)
            LOGGER.debug(
                "Response from DELETE %s received: \n%s",
                path,
                repr_json(response),
            )
            return response
        except ClientError as e:
            LOGGER.error(f"Error during DELETE {path}: {str(e)}")
            raise
