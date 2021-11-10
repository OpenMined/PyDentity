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

from aries_cloudcontroller.model.admin_api_message_tracing import AdminAPIMessageTracing
from aries_cloudcontroller.model.indy_cred_precis import IndyCredPrecis
from aries_cloudcontroller.model.indy_pres_spec import IndyPresSpec
from aries_cloudcontroller.model.v10_presentation_create_request_request import (
    V10PresentationCreateRequestRequest,
)
from aries_cloudcontroller.model.v10_presentation_exchange import (
    V10PresentationExchange,
)
from aries_cloudcontroller.model.v10_presentation_exchange_list import (
    V10PresentationExchangeList,
)
from aries_cloudcontroller.model.v10_presentation_problem_report_request import (
    V10PresentationProblemReportRequest,
)
from aries_cloudcontroller.model.v10_presentation_proposal_request import (
    V10PresentationProposalRequest,
)
from aries_cloudcontroller.model.v10_presentation_send_request_request import (
    V10PresentationSendRequestRequest,
)


class PresentProofV10Api(Consumer):
    async def create_proof_request(
        self, *, body: Optional[V10PresentationCreateRequestRequest] = None
    ) -> V10PresentationExchange:
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
        """Fetch credentials for a presentation request from wallet"""
        return await self.__get_matching_credentials(
            pres_ex_id=pres_ex_id,
            count=count,
            extra_query=extra_query,
            referent=referent,
            start=start,
        )

    async def get_record(self, *, pres_ex_id: str) -> V10PresentationExchange:
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
    ) -> V10PresentationExchangeList:
        """Fetch all present-proof exchange records"""
        return await self.__get_records(
            connection_id=connection_id,
            role=role,
            state=state,
            thread_id=thread_id,
        )

    async def report_problem(
        self,
        *,
        pres_ex_id: str,
        body: Optional[V10PresentationProblemReportRequest] = None
    ) -> Dict:
        """Send a problem report for presentation exchange"""
        return await self.__report_problem(
            pres_ex_id=pres_ex_id,
            body=body,
        )

    async def send_presentation(
        self, *, pres_ex_id: str, body: Optional[IndyPresSpec] = None
    ) -> V10PresentationExchange:
        """Sends a proof presentation"""
        return await self.__send_presentation(
            pres_ex_id=pres_ex_id,
            body=body,
        )

    async def send_proposal(
        self, *, body: Optional[V10PresentationProposalRequest] = None
    ) -> V10PresentationExchange:
        """Sends a presentation proposal"""
        return await self.__send_proposal(
            body=body,
        )

    async def send_request(
        self, *, pres_ex_id: str, body: Optional[AdminAPIMessageTracing] = None
    ) -> V10PresentationExchange:
        """Sends a presentation request in reference to a proposal"""
        return await self.__send_request(
            pres_ex_id=pres_ex_id,
            body=body,
        )

    async def send_request_free(
        self, *, body: Optional[V10PresentationSendRequestRequest] = None
    ) -> V10PresentationExchange:
        """Sends a free presentation request not bound to any proposal"""
        return await self.__send_request_free(
            body=body,
        )

    async def verify_presentation(self, *, pres_ex_id: str) -> V10PresentationExchange:
        """Verify a received presentation"""
        return await self.__verify_presentation(
            pres_ex_id=pres_ex_id,
        )

    @returns.json
    @json
    @post("/present-proof/create-request")
    def __create_proof_request(
        self, *, body: Body(type=V10PresentationCreateRequestRequest) = {}
    ) -> V10PresentationExchange:
        """Internal uplink method for create_proof_request"""

    @returns.json
    @delete("/present-proof/records/{pres_ex_id}")
    def __delete_record(self, *, pres_ex_id: str) -> Dict:
        """Internal uplink method for delete_record"""

    @returns.json
    @get("/present-proof/records/{pres_ex_id}/credentials")
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
    @get("/present-proof/records/{pres_ex_id}")
    def __get_record(self, *, pres_ex_id: str) -> V10PresentationExchange:
        """Internal uplink method for get_record"""

    @returns.json
    @get("/present-proof/records")
    def __get_records(
        self,
        *,
        connection_id: Query = None,
        role: Query = None,
        state: Query = None,
        thread_id: Query = None
    ) -> V10PresentationExchangeList:
        """Internal uplink method for get_records"""

    @returns.json
    @json
    @post("/present-proof/records/{pres_ex_id}/problem-report")
    def __report_problem(
        self,
        *,
        pres_ex_id: str,
        body: Body(type=V10PresentationProblemReportRequest) = {}
    ) -> Dict:
        """Internal uplink method for report_problem"""

    @returns.json
    @json
    @post("/present-proof/records/{pres_ex_id}/send-presentation")
    def __send_presentation(
        self, *, pres_ex_id: str, body: Body(type=IndyPresSpec) = {}
    ) -> V10PresentationExchange:
        """Internal uplink method for send_presentation"""

    @returns.json
    @json
    @post("/present-proof/send-proposal")
    def __send_proposal(
        self, *, body: Body(type=V10PresentationProposalRequest) = {}
    ) -> V10PresentationExchange:
        """Internal uplink method for send_proposal"""

    @returns.json
    @json
    @post("/present-proof/records/{pres_ex_id}/send-request")
    def __send_request(
        self, *, pres_ex_id: str, body: Body(type=AdminAPIMessageTracing) = {}
    ) -> V10PresentationExchange:
        """Internal uplink method for send_request"""

    @returns.json
    @json
    @post("/present-proof/send-request")
    def __send_request_free(
        self, *, body: Body(type=V10PresentationSendRequestRequest) = {}
    ) -> V10PresentationExchange:
        """Internal uplink method for send_request_free"""

    @returns.json
    @post("/present-proof/records/{pres_ex_id}/verify-presentation")
    def __verify_presentation(self, *, pres_ex_id: str) -> V10PresentationExchange:
        """Internal uplink method for verify_presentation"""
