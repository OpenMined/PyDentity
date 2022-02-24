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


class DefaultApi(Consumer):
    async def get_features(self):
        """"""
        return await self.__get_features()

    @get("/features")
    def __get_features(self):
        """Internal uplink method for get_features"""
