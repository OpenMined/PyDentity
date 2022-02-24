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

from aries_cloudcontroller.model.admin_config import AdminConfig
from aries_cloudcontroller.model.admin_modules import AdminModules
from aries_cloudcontroller.model.admin_status import AdminStatus
from aries_cloudcontroller.model.admin_status_liveliness import AdminStatusLiveliness
from aries_cloudcontroller.model.admin_status_readiness import AdminStatusReadiness


class ServerApi(Consumer):
    async def check_liveliness(self) -> AdminStatusLiveliness:
        """Liveliness check"""
        return await self.__check_liveliness()

    async def get_config(self) -> AdminConfig:
        """Fetch the server configuration"""
        return await self.__get_config()

    async def get_plugins(self) -> AdminModules:
        """Fetch the list of loaded plugins"""
        return await self.__get_plugins()

    async def get_ready_state(self) -> AdminStatusReadiness:
        """Readiness check"""
        return await self.__get_ready_state()

    async def get_status(self) -> AdminStatus:
        """Fetch the server status"""
        return await self.__get_status()

    async def reset_statistics(self) -> Dict:
        """Reset statistics"""
        return await self.__reset_statistics()

    async def shutdown_server(self) -> Dict:
        """Shut down server"""
        return await self.__shutdown_server()

    @returns.json
    @get("/status/live")
    def __check_liveliness(self) -> AdminStatusLiveliness:
        """Internal uplink method for check_liveliness"""

    @returns.json
    @get("/status/config")
    def __get_config(self) -> AdminConfig:
        """Internal uplink method for get_config"""

    @returns.json
    @get("/plugins")
    def __get_plugins(self) -> AdminModules:
        """Internal uplink method for get_plugins"""

    @returns.json
    @get("/status/ready")
    def __get_ready_state(self) -> AdminStatusReadiness:
        """Internal uplink method for get_ready_state"""

    @returns.json
    @get("/status")
    def __get_status(self) -> AdminStatus:
        """Internal uplink method for get_status"""

    @returns.json
    @post("/status/reset")
    def __reset_statistics(self) -> Dict:
        """Internal uplink method for reset_statistics"""

    @returns.json
    @get("/shutdown")
    def __shutdown_server(self) -> Dict:
        """Internal uplink method for shutdown_server"""
