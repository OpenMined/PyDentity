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

from aries_cloudcontroller.model.attribute_mime_types_result import (
    AttributeMimeTypesResult,
)
from aries_cloudcontroller.model.cred_info_list import CredInfoList
from aries_cloudcontroller.model.cred_revoked_result import CredRevokedResult
from aries_cloudcontroller.model.indy_cred_info import IndyCredInfo
from aries_cloudcontroller.model.vc_record import VCRecord
from aries_cloudcontroller.model.vc_record_list import VCRecordList
from aries_cloudcontroller.model.w3_c_credentials_list_request import (
    W3CCredentialsListRequest,
)


class CredentialsApi(Consumer):
    async def delete_record(self, *, credential_id: str) -> Dict:
        """Remove credential from wallet by id"""
        return await self.__delete_record(
            credential_id=credential_id,
        )

    async def delete_w3c_credential(self, *, credential_id: str) -> Dict:
        """Remove W3C credential from wallet by id"""
        return await self.__delete_w3c_credential(
            credential_id=credential_id,
        )

    async def get_credential_mime_types(
        self, *, credential_id: str
    ) -> AttributeMimeTypesResult:
        """Get attribute MIME types from wallet"""
        return await self.__get_credential_mime_types(
            credential_id=credential_id,
        )

    async def get_record(self, *, credential_id: str) -> IndyCredInfo:
        """Fetch credential from wallet by id"""
        return await self.__get_record(
            credential_id=credential_id,
        )

    async def get_records(
        self,
        *,
        count: Optional[str] = None,
        start: Optional[str] = None,
        wql: Optional[str] = None
    ) -> CredInfoList:
        """Fetch credentials from wallet"""
        return await self.__get_records(
            count=count,
            start=start,
            wql=wql,
        )

    async def get_revocation_status(
        self,
        *,
        credential_id: str,
        from_: Optional[str] = None,
        to: Optional[str] = None
    ) -> CredRevokedResult:
        """Query credential revocation status by id"""
        return await self.__get_revocation_status(
            credential_id=credential_id,
            from_=from_,
            to=to,
        )

    async def get_w3c_credential(self, *, credential_id: str) -> VCRecord:
        """Fetch W3C credential from wallet by id"""
        return await self.__get_w3c_credential(
            credential_id=credential_id,
        )

    async def get_w3c_credentials(
        self,
        *,
        count: Optional[str] = None,
        start: Optional[str] = None,
        wql: Optional[str] = None,
        body: Optional[W3CCredentialsListRequest] = None
    ) -> VCRecordList:
        """Fetch W3C credentials from wallet"""
        return await self.__get_w3c_credentials(
            count=count,
            start=start,
            wql=wql,
            body=body,
        )

    @returns.json
    @delete("/credential/{credential_id}")
    def __delete_record(self, *, credential_id: str) -> Dict:
        """Internal uplink method for delete_record"""

    @returns.json
    @delete("/credential/w3c/{credential_id}")
    def __delete_w3c_credential(self, *, credential_id: str) -> Dict:
        """Internal uplink method for delete_w3c_credential"""

    @returns.json
    @get("/credential/mime-types/{credential_id}")
    def __get_credential_mime_types(
        self, *, credential_id: str
    ) -> AttributeMimeTypesResult:
        """Internal uplink method for get_credential_mime_types"""

    @returns.json
    @get("/credential/{credential_id}")
    def __get_record(self, *, credential_id: str) -> IndyCredInfo:
        """Internal uplink method for get_record"""

    @returns.json
    @get("/credentials")
    def __get_records(
        self, *, count: Query = None, start: Query = None, wql: Query = None
    ) -> CredInfoList:
        """Internal uplink method for get_records"""

    @returns.json
    @get("/credential/revoked/{credential_id}")
    def __get_revocation_status(
        self, *, credential_id: str, from_: Query = None, to: Query = None
    ) -> CredRevokedResult:
        """Internal uplink method for get_revocation_status"""

    @returns.json
    @get("/credential/w3c/{credential_id}")
    def __get_w3c_credential(self, *, credential_id: str) -> VCRecord:
        """Internal uplink method for get_w3c_credential"""

    @returns.json
    @json
    @post("/credentials/w3c")
    def __get_w3c_credentials(
        self,
        *,
        count: Query = None,
        start: Query = None,
        wql: Query = None,
        body: Body(type=W3CCredentialsListRequest) = {}
    ) -> VCRecordList:
        """Internal uplink method for get_w3c_credentials"""
