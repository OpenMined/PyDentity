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


class IntroductionApi(Consumer):
    async def start_introduction(
        self, *, conn_id: str, target_connection_id: str, message: Optional[str] = None
    ) -> Dict:
        """Start an introduction between two connections"""
        return await self.__start_introduction(
            conn_id=conn_id,
            target_connection_id=target_connection_id,
            message=message,
        )

    @returns.json
    @post("/connections/{conn_id}/start-introduction")
    def __start_introduction(
        self, *, conn_id: str, target_connection_id: Query, message: Query = None
    ) -> Dict:
        """Internal uplink method for start_introduction"""
