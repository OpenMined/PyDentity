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

from aries_cloudcontroller.model.v20_discovery_exchange_list_result import (
    V20DiscoveryExchangeListResult,
)
from aries_cloudcontroller.model.v20_discovery_exchange_result import (
    V20DiscoveryExchangeResult,
)


class DiscoverFeaturesV20Api(Consumer):
    async def discover_features20_queries_get(
        self,
        *,
        connection_id: Optional[str] = None,
        query_goal_code: Optional[str] = None,
        query_protocol: Optional[str] = None
    ) -> V20DiscoveryExchangeResult:
        """Query supported features"""
        return await self.__discover_features20_queries_get(
            connection_id=connection_id,
            query_goal_code=query_goal_code,
            query_protocol=query_protocol,
        )

    async def discover_features20_records_get(
        self, *, connection_id: Optional[str] = None
    ) -> V20DiscoveryExchangeListResult:
        """Discover Features v2.0 records"""
        return await self.__discover_features20_records_get(
            connection_id=connection_id,
        )

    @returns.json
    @get("/discover-features-2.0/queries")
    def __discover_features20_queries_get(
        self,
        *,
        connection_id: Query = None,
        query_goal_code: Query = None,
        query_protocol: Query = None
    ) -> V20DiscoveryExchangeResult:
        """Internal uplink method for discover_features20_queries_get"""

    @returns.json
    @get("/discover-features-2.0/records")
    def __discover_features20_records_get(
        self, *, connection_id: Query = None
    ) -> V20DiscoveryExchangeListResult:
        """Internal uplink method for discover_features20_records_get"""
