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

from aries_cloudcontroller.model.clear_pending_revocations_request import (
    ClearPendingRevocationsRequest,
)
from aries_cloudcontroller.model.cred_rev_record_result import CredRevRecordResult
from aries_cloudcontroller.model.publish_revocations import PublishRevocations
from aries_cloudcontroller.model.rev_reg_create_request import RevRegCreateRequest
from aries_cloudcontroller.model.rev_reg_issued_result import RevRegIssuedResult
from aries_cloudcontroller.model.rev_reg_result import RevRegResult
from aries_cloudcontroller.model.rev_reg_update_tails_file_uri import (
    RevRegUpdateTailsFileUri,
)
from aries_cloudcontroller.model.rev_regs_created import RevRegsCreated
from aries_cloudcontroller.model.revoke_request import RevokeRequest


class RevocationApi(Consumer):
    async def clear_pending_revocations(
        self, *, body: Optional[ClearPendingRevocationsRequest] = None
    ) -> PublishRevocations:
        """Clear pending revocations"""
        return await self.__clear_pending_revocations(
            body=body,
        )

    async def create_registry(
        self, *, body: Optional[RevRegCreateRequest] = None
    ) -> RevRegResult:
        """Creates a new revocation registry"""
        return await self.__create_registry(
            body=body,
        )

    async def download_tails_file(self, *, rev_reg_id: str) -> bytes:
        """Download tails file"""
        return await self.__download_tails_file(
            rev_reg_id=rev_reg_id,
        )

    async def get_active_registry_for_cred_def(
        self, *, cred_def_id: str
    ) -> RevRegResult:
        """Get current active revocation registry by credential definition id"""
        return await self.__get_active_registry_for_cred_def(
            cred_def_id=cred_def_id,
        )

    async def get_created_registries(
        self, *, cred_def_id: Optional[str] = None, state: Optional[str] = None
    ) -> RevRegsCreated:
        """Search for matching revocation registries that current agent created"""
        return await self.__get_created_registries(
            cred_def_id=cred_def_id,
            state=state,
        )

    async def get_registry(self, *, rev_reg_id: str) -> RevRegResult:
        """Get revocation registry by revocation registry id"""
        return await self.__get_registry(
            rev_reg_id=rev_reg_id,
        )

    async def get_registry_issued_credentials_count(
        self, *, rev_reg_id: str
    ) -> RevRegIssuedResult:
        """Get number of credentials issued against revocation registry"""
        return await self.__get_registry_issued_credentials_count(
            rev_reg_id=rev_reg_id,
        )

    async def get_revocation_status(
        self,
        *,
        cred_ex_id: Optional[str] = None,
        cred_rev_id: Optional[str] = None,
        rev_reg_id: Optional[str] = None
    ) -> CredRevRecordResult:
        """Get credential revocation status"""
        return await self.__get_revocation_status(
            cred_ex_id=cred_ex_id,
            cred_rev_id=cred_rev_id,
            rev_reg_id=rev_reg_id,
        )

    async def publish_rev_reg_def(
        self,
        *,
        rev_reg_id: str,
        conn_id: Optional[str] = None,
        create_transaction_for_endorser: Optional[bool] = None
    ) -> RevRegResult:
        """Send revocation registry definition to ledger"""
        return await self.__publish_rev_reg_def(
            rev_reg_id=rev_reg_id,
            conn_id=conn_id,
            create_transaction_for_endorser=bool_query(create_transaction_for_endorser),
        )

    async def publish_rev_reg_entry(
        self,
        *,
        rev_reg_id: str,
        conn_id: Optional[str] = None,
        create_transaction_for_endorser: Optional[bool] = None
    ) -> RevRegResult:
        """Send revocation registry entry to ledger"""
        return await self.__publish_rev_reg_entry(
            rev_reg_id=rev_reg_id,
            conn_id=conn_id,
            create_transaction_for_endorser=bool_query(create_transaction_for_endorser),
        )

    async def publish_revocations(
        self,
        *,
        conn_id: Optional[str] = None,
        create_transaction_for_endorser: Optional[bool] = None,
        body: Optional[PublishRevocations] = None
    ) -> PublishRevocations:
        """Publish pending revocations to ledger"""
        return await self.__publish_revocations(
            conn_id=conn_id,
            create_transaction_for_endorser=bool_query(create_transaction_for_endorser),
            body=body,
        )

    async def revoke_credential(self, *, body: Optional[RevokeRequest] = None) -> Dict:
        """Revoke an issued credential"""
        return await self.__revoke_credential(
            body=body,
        )

    async def set_registry_state(self, *, rev_reg_id: str, state: str) -> RevRegResult:
        """Set revocation registry state manually"""
        return await self.__set_registry_state(
            rev_reg_id=rev_reg_id,
            state=state,
        )

    async def update_registry(
        self, *, rev_reg_id: str, body: Optional[RevRegUpdateTailsFileUri] = None
    ) -> RevRegResult:
        """Update revocation registry with new public URI to its tails file"""
        return await self.__update_registry(
            rev_reg_id=rev_reg_id,
            body=body,
        )

    async def upload_tails_file(self, *, rev_reg_id: str) -> Dict:
        """Upload local tails file to server"""
        return await self.__upload_tails_file(
            rev_reg_id=rev_reg_id,
        )

    @returns.json
    @json
    @post("/revocation/clear-pending-revocations")
    def __clear_pending_revocations(
        self, *, body: Body(type=ClearPendingRevocationsRequest) = {}
    ) -> PublishRevocations:
        """Internal uplink method for clear_pending_revocations"""

    @returns.json
    @json
    @post("/revocation/create-registry")
    def __create_registry(
        self, *, body: Body(type=RevRegCreateRequest) = {}
    ) -> RevRegResult:
        """Internal uplink method for create_registry"""

    @get("/revocation/registry/{rev_reg_id}/tails-file")
    def __download_tails_file(self, *, rev_reg_id: str) -> bytes:
        """Internal uplink method for download_tails_file"""

    @returns.json
    @get("/revocation/active-registry/{cred_def_id}")
    def __get_active_registry_for_cred_def(self, *, cred_def_id: str) -> RevRegResult:
        """Internal uplink method for get_active_registry_for_cred_def"""

    @returns.json
    @get("/revocation/registries/created")
    def __get_created_registries(
        self, *, cred_def_id: Query = None, state: Query = None
    ) -> RevRegsCreated:
        """Internal uplink method for get_created_registries"""

    @returns.json
    @get("/revocation/registry/{rev_reg_id}")
    def __get_registry(self, *, rev_reg_id: str) -> RevRegResult:
        """Internal uplink method for get_registry"""

    @returns.json
    @get("/revocation/registry/{rev_reg_id}/issued")
    def __get_registry_issued_credentials_count(
        self, *, rev_reg_id: str
    ) -> RevRegIssuedResult:
        """Internal uplink method for get_registry_issued_credentials_count"""

    @returns.json
    @get("/revocation/credential-record")
    def __get_revocation_status(
        self,
        *,
        cred_ex_id: Query = None,
        cred_rev_id: Query = None,
        rev_reg_id: Query = None
    ) -> CredRevRecordResult:
        """Internal uplink method for get_revocation_status"""

    @returns.json
    @post("/revocation/registry/{rev_reg_id}/definition")
    def __publish_rev_reg_def(
        self,
        *,
        rev_reg_id: str,
        conn_id: Query = None,
        create_transaction_for_endorser: Query = None
    ) -> RevRegResult:
        """Internal uplink method for publish_rev_reg_def"""

    @returns.json
    @post("/revocation/registry/{rev_reg_id}/entry")
    def __publish_rev_reg_entry(
        self,
        *,
        rev_reg_id: str,
        conn_id: Query = None,
        create_transaction_for_endorser: Query = None
    ) -> RevRegResult:
        """Internal uplink method for publish_rev_reg_entry"""

    @returns.json
    @json
    @post("/revocation/publish-revocations")
    def __publish_revocations(
        self,
        *,
        conn_id: Query = None,
        create_transaction_for_endorser: Query = None,
        body: Body(type=PublishRevocations) = {}
    ) -> PublishRevocations:
        """Internal uplink method for publish_revocations"""

    @returns.json
    @json
    @post("/revocation/revoke")
    def __revoke_credential(self, *, body: Body(type=RevokeRequest) = {}) -> Dict:
        """Internal uplink method for revoke_credential"""

    @returns.json
    @patch("/revocation/registry/{rev_reg_id}/set-state")
    def __set_registry_state(self, *, rev_reg_id: str, state: Query) -> RevRegResult:
        """Internal uplink method for set_registry_state"""

    @returns.json
    @json
    @patch("/revocation/registry/{rev_reg_id}")
    def __update_registry(
        self, *, rev_reg_id: str, body: Body(type=RevRegUpdateTailsFileUri) = {}
    ) -> RevRegResult:
        """Internal uplink method for update_registry"""

    @returns.json
    @put("/revocation/registry/{rev_reg_id}/tails-file")
    def __upload_tails_file(self, *, rev_reg_id: str) -> Dict:
        """Internal uplink method for upload_tails_file"""
