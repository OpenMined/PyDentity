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

from aries_cloudcontroller.model.admin_api_message_tracing import AdminAPIMessageTracing
from aries_cloudcontroller.model.indy_cred_precis import IndyCredPrecis
from aries_cloudcontroller.model.v20_pres_create_request_request import (
    V20PresCreateRequestRequest,
)
from aries_cloudcontroller.model.v20_pres_ex_record import V20PresExRecord
from aries_cloudcontroller.model.v20_pres_ex_record_list import V20PresExRecordList
from aries_cloudcontroller.model.v20_pres_problem_report_request import (
    V20PresProblemReportRequest,
)
from aries_cloudcontroller.model.v20_pres_proposal_request import V20PresProposalRequest
from aries_cloudcontroller.model.v20_pres_send_request_request import (
    V20PresSendRequestRequest,
)
from aries_cloudcontroller.model.v20_pres_spec_by_format_request import (
    V20PresSpecByFormatRequest,
)


class PresentProofV20Api(Consumer):
    async def create_proof_request(
        self, *, body: Optional[V20PresCreateRequestRequest] = None
    ) -> V20PresExRecord:
        """Creates a presentation request not bound to any proposal or connection"""
        return await self.__create_proof_request(
            body=body,
        )

    async def delete_record(self, *, pres_ex_id: str) -> Dict:
        """Remove an existing presentation exchange record"""
        return await self.__delete_record(
            pres_ex_id=pres_ex_id,
        )

    async def get_matching_credentials(
        self,
        *,
        pres_ex_id: str,
        count: Optional[str] = None,
        extra_query: Optional[str] = None,
        referent: Optional[str] = None,
        start: Optional[str] = None
    ) -> List[IndyCredPrecis]:
        """Fetch credentials from wallet for presentation request"""
        return await self.__get_matching_credentials(
            pres_ex_id=pres_ex_id,
            count=count,
            extra_query=extra_query,
            referent=referent,
            start=start,
        )

    async def get_record(self, *, pres_ex_id: str) -> V20PresExRecord:
        """Fetch a single presentation exchange record"""
        return await self.__get_record(
            pres_ex_id=pres_ex_id,
        )

    async def get_records(
        self,
        *,
        connection_id: Optional[str] = None,
        role: Optional[str] = None,
        state: Optional[str] = None,
        thread_id: Optional[str] = None
    ) -> V20PresExRecordList:
        """Fetch all present-proof exchange records"""
        return await self.__get_records(
            connection_id=connection_id,
            role=role,
            state=state,
            thread_id=thread_id,
        )

    async def report_problem(
        self, *, pres_ex_id: str, body: Optional[V20PresProblemReportRequest] = None
    ) -> Dict:
        """Send a problem report for presentation exchange"""
        return await self.__report_problem(
            pres_ex_id=pres_ex_id,
            body=body,
        )

    async def send_presentation(
        self, *, pres_ex_id: str, body: Optional[V20PresSpecByFormatRequest] = None
    ) -> V20PresExRecord:
        """Sends a proof presentation"""
        return await self.__send_presentation(
            pres_ex_id=pres_ex_id,
            body=body,
        )

    async def send_proposal(
        self, *, body: Optional[V20PresProposalRequest] = None
    ) -> V20PresExRecord:
        """Sends a presentation proposal"""
        return await self.__send_proposal(
            body=body,
        )

    async def send_request(
        self, *, pres_ex_id: str, body: Optional[AdminAPIMessageTracing] = None
    ) -> V20PresExRecord:
        """Sends a presentation request in reference to a proposal"""
        return await self.__send_request(
            pres_ex_id=pres_ex_id,
            body=body,
        )

    async def send_request_free(
        self, *, body: Optional[V20PresSendRequestRequest] = None
    ) -> V20PresExRecord:
        """Sends a free presentation request not bound to any proposal"""
        return await self.__send_request_free(
            body=body,
        )

    async def verify_presentation(self, *, pres_ex_id: str) -> V20PresExRecord:
        """Verify a received presentation"""
        return await self.__verify_presentation(
            pres_ex_id=pres_ex_id,
        )

    @returns.json
    @json
    @post("/present-proof-2.0/create-request")
    def __create_proof_request(
        self, *, body: Body(type=V20PresCreateRequestRequest) = {}
    ) -> V20PresExRecord:
        """Internal uplink method for create_proof_request"""

    @returns.json
    @delete("/present-proof-2.0/records/{pres_ex_id}")
    def __delete_record(self, *, pres_ex_id: str) -> Dict:
        """Internal uplink method for delete_record"""

    @returns.json
    @get("/present-proof-2.0/records/{pres_ex_id}/credentials")
    def __get_matching_credentials(
        self,
        *,
        pres_ex_id: str,
        count: Query = None,
        extra_query: Query = None,
        referent: Query = None,
        start: Query = None
    ) -> List[IndyCredPrecis]:
        """Internal uplink method for get_matching_credentials"""

    @returns.json
    @get("/present-proof-2.0/records/{pres_ex_id}")
    def __get_record(self, *, pres_ex_id: str) -> V20PresExRecord:
        """Internal uplink method for get_record"""

    @returns.json
    @get("/present-proof-2.0/records")
    def __get_records(
        self,
        *,
        connection_id: Query = None,
        role: Query = None,
        state: Query = None,
        thread_id: Query = None
    ) -> V20PresExRecordList:
        """Internal uplink method for get_records"""

    @returns.json
    @json
    @post("/present-proof-2.0/records/{pres_ex_id}/problem-report")
    def __report_problem(
        self, *, pres_ex_id: str, body: Body(type=V20PresProblemReportRequest) = {}
    ) -> Dict:
        """Internal uplink method for report_problem"""

    @returns.json
    @json
    @post("/present-proof-2.0/records/{pres_ex_id}/send-presentation")
    def __send_presentation(
        self, *, pres_ex_id: str, body: Body(type=V20PresSpecByFormatRequest) = {}
    ) -> V20PresExRecord:
        """Internal uplink method for send_presentation"""

    @returns.json
    @json
    @post("/present-proof-2.0/send-proposal")
    def __send_proposal(
        self, *, body: Body(type=V20PresProposalRequest) = {}
    ) -> V20PresExRecord:
        """Internal uplink method for send_proposal"""

    @returns.json
    @json
    @post("/present-proof-2.0/records/{pres_ex_id}/send-request")
    def __send_request(
        self, *, pres_ex_id: str, body: Body(type=AdminAPIMessageTracing) = {}
    ) -> V20PresExRecord:
        """Internal uplink method for send_request"""

    @returns.json
    @json
    @post("/present-proof-2.0/send-request")
    def __send_request_free(
        self, *, body: Body(type=V20PresSendRequestRequest) = {}
    ) -> V20PresExRecord:
        """Internal uplink method for send_request_free"""

    @returns.json
    @post("/present-proof-2.0/records/{pres_ex_id}/verify-presentation")
    def __verify_presentation(self, *, pres_ex_id: str) -> V20PresExRecord:
        """Internal uplink method for verify_presentation"""
