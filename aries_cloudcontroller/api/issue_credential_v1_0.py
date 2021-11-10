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

from aries_cloudcontroller.model.v10_credential_bound_offer_request import (
    V10CredentialBoundOfferRequest,
)
from aries_cloudcontroller.model.v10_credential_conn_free_offer_request import (
    V10CredentialConnFreeOfferRequest,
)
from aries_cloudcontroller.model.v10_credential_create import V10CredentialCreate
from aries_cloudcontroller.model.v10_credential_exchange import V10CredentialExchange
from aries_cloudcontroller.model.v10_credential_exchange_list_result import (
    V10CredentialExchangeListResult,
)
from aries_cloudcontroller.model.v10_credential_free_offer_request import (
    V10CredentialFreeOfferRequest,
)
from aries_cloudcontroller.model.v10_credential_issue_request import (
    V10CredentialIssueRequest,
)
from aries_cloudcontroller.model.v10_credential_problem_report_request import (
    V10CredentialProblemReportRequest,
)
from aries_cloudcontroller.model.v10_credential_proposal_request_mand import (
    V10CredentialProposalRequestMand,
)
from aries_cloudcontroller.model.v10_credential_proposal_request_opt import (
    V10CredentialProposalRequestOpt,
)
from aries_cloudcontroller.model.v10_credential_store_request import (
    V10CredentialStoreRequest,
)


class IssueCredentialV10Api(Consumer):
    async def create_credential(
        self, *, body: Optional[V10CredentialCreate] = None
    ) -> V10CredentialExchange:
        """Send holder a credential, automating entire flow"""
        return await self.__create_credential(
            body=body,
        )

    async def create_offer(
        self, *, body: Optional[V10CredentialConnFreeOfferRequest] = None
    ) -> V10CredentialExchange:
        """Create a credential offer, independent of any proposal or connection"""
        return await self.__create_offer(
            body=body,
        )

    async def delete_record(self, *, cred_ex_id: str) -> Dict:
        """Remove an existing credential exchange record"""
        return await self.__delete_record(
            cred_ex_id=cred_ex_id,
        )

    async def get_record(self, *, cred_ex_id: str) -> V10CredentialExchange:
        """Fetch a single credential exchange record"""
        return await self.__get_record(
            cred_ex_id=cred_ex_id,
        )

    async def get_records(
        self,
        *,
        connection_id: Optional[str] = None,
        role: Optional[str] = None,
        state: Optional[str] = None,
        thread_id: Optional[str] = None
    ) -> V10CredentialExchangeListResult:
        """Fetch all credential exchange records"""
        return await self.__get_records(
            connection_id=connection_id,
            role=role,
            state=state,
            thread_id=thread_id,
        )

    async def issue_credential(
        self, *, cred_ex_id: str, body: Optional[V10CredentialIssueRequest] = None
    ) -> V10CredentialExchange:
        """Send holder a credential"""
        return await self.__issue_credential(
            cred_ex_id=cred_ex_id,
            body=body,
        )

    async def issue_credential_automated(
        self, *, body: Optional[V10CredentialProposalRequestMand] = None
    ) -> V10CredentialExchange:
        """Send holder a credential, automating entire flow"""
        return await self.__issue_credential_automated(
            body=body,
        )

    async def report_problem(
        self,
        *,
        cred_ex_id: str,
        body: Optional[V10CredentialProblemReportRequest] = None
    ) -> Dict:
        """Send a problem report for credential exchange"""
        return await self.__report_problem(
            cred_ex_id=cred_ex_id,
            body=body,
        )

    async def send_offer(
        self, *, cred_ex_id: str, body: Optional[V10CredentialBoundOfferRequest] = None
    ) -> V10CredentialExchange:
        """Send holder a credential offer in reference to a proposal with preview"""
        return await self.__send_offer(
            cred_ex_id=cred_ex_id,
            body=body,
        )

    async def send_offer_free(
        self, *, body: Optional[V10CredentialFreeOfferRequest] = None
    ) -> V10CredentialExchange:
        """Send holder a credential offer, independent of any proposal"""
        return await self.__send_offer_free(
            body=body,
        )

    async def send_proposal(
        self, *, body: Optional[V10CredentialProposalRequestOpt] = None
    ) -> V10CredentialExchange:
        """Send issuer a credential proposal"""
        return await self.__send_proposal(
            body=body,
        )

    async def send_request(self, *, cred_ex_id: str) -> V10CredentialExchange:
        """Send issuer a credential request"""
        return await self.__send_request(
            cred_ex_id=cred_ex_id,
        )

    async def store_credential(
        self, *, cred_ex_id: str, body: Optional[V10CredentialStoreRequest] = None
    ) -> V10CredentialExchange:
        """Store a received credential"""
        return await self.__store_credential(
            cred_ex_id=cred_ex_id,
            body=body,
        )

    @returns.json
    @json
    @post("/issue-credential/create")
    def __create_credential(
        self, *, body: Body(type=V10CredentialCreate) = {}
    ) -> V10CredentialExchange:
        """Internal uplink method for create_credential"""

    @returns.json
    @json
    @post("/issue-credential/create-offer")
    def __create_offer(
        self, *, body: Body(type=V10CredentialConnFreeOfferRequest) = {}
    ) -> V10CredentialExchange:
        """Internal uplink method for create_offer"""

    @returns.json
    @delete("/issue-credential/records/{cred_ex_id}")
    def __delete_record(self, *, cred_ex_id: str) -> Dict:
        """Internal uplink method for delete_record"""

    @returns.json
    @get("/issue-credential/records/{cred_ex_id}")
    def __get_record(self, *, cred_ex_id: str) -> V10CredentialExchange:
        """Internal uplink method for get_record"""

    @returns.json
    @get("/issue-credential/records")
    def __get_records(
        self,
        *,
        connection_id: Query = None,
        role: Query = None,
        state: Query = None,
        thread_id: Query = None
    ) -> V10CredentialExchangeListResult:
        """Internal uplink method for get_records"""

    @returns.json
    @json
    @post("/issue-credential/records/{cred_ex_id}/issue")
    def __issue_credential(
        self, *, cred_ex_id: str, body: Body(type=V10CredentialIssueRequest) = {}
    ) -> V10CredentialExchange:
        """Internal uplink method for issue_credential"""

    @returns.json
    @json
    @post("/issue-credential/send")
    def __issue_credential_automated(
        self, *, body: Body(type=V10CredentialProposalRequestMand) = {}
    ) -> V10CredentialExchange:
        """Internal uplink method for issue_credential_automated"""

    @returns.json
    @json
    @post("/issue-credential/records/{cred_ex_id}/problem-report")
    def __report_problem(
        self,
        *,
        cred_ex_id: str,
        body: Body(type=V10CredentialProblemReportRequest) = {}
    ) -> Dict:
        """Internal uplink method for report_problem"""

    @returns.json
    @json
    @post("/issue-credential/records/{cred_ex_id}/send-offer")
    def __send_offer(
        self, *, cred_ex_id: str, body: Body(type=V10CredentialBoundOfferRequest) = {}
    ) -> V10CredentialExchange:
        """Internal uplink method for send_offer"""

    @returns.json
    @json
    @post("/issue-credential/send-offer")
    def __send_offer_free(
        self, *, body: Body(type=V10CredentialFreeOfferRequest) = {}
    ) -> V10CredentialExchange:
        """Internal uplink method for send_offer_free"""

    @returns.json
    @json
    @post("/issue-credential/send-proposal")
    def __send_proposal(
        self, *, body: Body(type=V10CredentialProposalRequestOpt) = {}
    ) -> V10CredentialExchange:
        """Internal uplink method for send_proposal"""

    @returns.json
    @post("/issue-credential/records/{cred_ex_id}/send-request")
    def __send_request(self, *, cred_ex_id: str) -> V10CredentialExchange:
        """Internal uplink method for send_request"""

    @returns.json
    @json
    @post("/issue-credential/records/{cred_ex_id}/store")
    def __store_credential(
        self, *, cred_ex_id: str, body: Body(type=V10CredentialStoreRequest) = {}
    ) -> V10CredentialExchange:
        """Internal uplink method for store_credential"""
