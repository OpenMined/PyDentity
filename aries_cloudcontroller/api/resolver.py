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

from aries_cloudcontroller.model.resolution_result import ResolutionResult


class ResolverApi(Consumer):
    async def get_did(self, *, did: str) -> ResolutionResult:
        """Retrieve doc for requested did"""
        return await self.__get_did(
            did=did,
        )

    @returns.json
    @get("/resolver/resolve/{did}")
    def __get_did(self, *, did: str) -> ResolutionResult:
        """Internal uplink method for get_did"""
