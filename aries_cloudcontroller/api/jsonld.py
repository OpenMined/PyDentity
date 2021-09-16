from uplink import (
    Consumer,
    Path,
    Query,
    Body,
    Header,
    get,
    post,
    patch,
    put,
    delete,
    returns,
    json,
)

from typing import Dict, List, Optional, Union  # noqa: F401

from aries_cloudcontroller.model.sign_request import SignRequest
from aries_cloudcontroller.model.sign_response import SignResponse
from aries_cloudcontroller.model.verify_request import VerifyRequest
from aries_cloudcontroller.model.verify_response import VerifyResponse


class JsonldApi(Consumer):
    async def sign(self, *, body: Optional[SignRequest] = None) -> SignResponse:
        """Sign a JSON-LD structure and return it"""
        return await self.__sign(
            body=body,
        )

    async def verify(self, *, body: Optional[VerifyRequest] = None) -> VerifyResponse:
        """Verify a JSON-LD structure."""
        return await self.__verify(
            body=body,
        )

    @returns.json
    @json
    @post("/jsonld/sign")
    def __sign(self, *, body: Body(type=SignRequest) = {}) -> SignResponse:
        """Internal uplink method for sign"""

    @returns.json
    @json
    @post("/jsonld/verify")
    def __verify(self, *, body: Body(type=VerifyRequest) = {}) -> VerifyResponse:
        """Internal uplink method for verify"""
