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

from aries_cloudcontroller.uplink_util import bool_query

from aries_cloudcontroller.model.v10_discovery_exchange_list_result import (
    V10DiscoveryExchangeListResult,
)
from aries_cloudcontroller.model.v10_discovery_exchange_result import (
    V10DiscoveryExchangeResult,
)


class DiscoverFeaturesApi(Consumer):
    async def discover_features_query_get(
        self,
        *,
        comment: Optional[str] = None,
        connection_id: Optional[str] = None,
        query: Optional[str] = None
    ) -> V10DiscoveryExchangeResult:
        """Query supported features"""
        return await self.__discover_features_query_get(
            comment=comment,
            connection_id=connection_id,
            query=query,
        )

    async def discover_features_records_get(
        self, *, connection_id: Optional[str] = None
    ) -> V10DiscoveryExchangeListResult:
        """Discover Features records"""
        return await self.__discover_features_records_get(
            connection_id=connection_id,
        )

    @returns.json
    @get("/discover-features/query")
    def __discover_features_query_get(
        self, *, comment: Query = None, connection_id: Query = None, query: Query = None
    ) -> V10DiscoveryExchangeResult:
        """Internal uplink method for discover_features_query_get"""

    @returns.json
    @get("/discover-features/records")
    def __discover_features_records_get(
        self, *, connection_id: Query = None
    ) -> V10DiscoveryExchangeListResult:
        """Internal uplink method for discover_features_records_get"""
