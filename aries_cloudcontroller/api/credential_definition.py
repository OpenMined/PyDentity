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

from aries_cloudcontroller.model.credential_definition_get_result import (
    CredentialDefinitionGetResult,
)
from aries_cloudcontroller.model.credential_definition_send_request import (
    CredentialDefinitionSendRequest,
)
from aries_cloudcontroller.model.credential_definition_send_result import (
    CredentialDefinitionSendResult,
)
from aries_cloudcontroller.model.credential_definitions_created_result import (
    CredentialDefinitionsCreatedResult,
)
from aries_cloudcontroller.model.txn_or_credential_definition_send_result import (
    TxnOrCredentialDefinitionSendResult,
)


class CredentialDefinitionApi(Consumer):
    async def credential_definitions_cred_def_id_write_record_post(
        self, *, cred_def_id: str
    ) -> CredentialDefinitionGetResult:
        """Writes a credential definition non-secret record to the wallet"""
        return await self.__credential_definitions_cred_def_id_write_record_post(
            cred_def_id=cred_def_id,
        )

    async def get_created_cred_defs(
        self,
        *,
        cred_def_id: Optional[str] = None,
        issuer_did: Optional[str] = None,
        schema_id: Optional[str] = None,
        schema_issuer_did: Optional[str] = None,
        schema_name: Optional[str] = None,
        schema_version: Optional[str] = None
    ) -> CredentialDefinitionsCreatedResult:
        """Search for matching credential definitions that agent originated"""
        return await self.__get_created_cred_defs(
            cred_def_id=cred_def_id,
            issuer_did=issuer_did,
            schema_id=schema_id,
            schema_issuer_did=schema_issuer_did,
            schema_name=schema_name,
            schema_version=schema_version,
        )

    async def get_cred_def(self, *, cred_def_id: str) -> CredentialDefinitionGetResult:
        """Gets a credential definition from the ledger"""
        return await self.__get_cred_def(
            cred_def_id=cred_def_id,
        )

    async def publish_cred_def(
        self,
        *,
        conn_id: Optional[str] = None,
        create_transaction_for_endorser: Optional[bool] = None,
        body: Optional[CredentialDefinitionSendRequest] = None
    ) -> Union[CredentialDefinitionSendResult, TxnOrCredentialDefinitionSendResult]:
        """Sends a credential definition to the ledger"""
        return await self.__publish_cred_def(
            conn_id=conn_id,
            create_transaction_for_endorser=bool_query(create_transaction_for_endorser),
            body=body,
        )

    @returns.json
    @post("/credential-definitions/{cred_def_id}/write_record")
    def __credential_definitions_cred_def_id_write_record_post(
        self, *, cred_def_id: str
    ) -> CredentialDefinitionGetResult:
        """Internal uplink method for credential_definitions_cred_def_id_write_record_post"""

    @returns.json
    @get("/credential-definitions/created")
    def __get_created_cred_defs(
        self,
        *,
        cred_def_id: Query = None,
        issuer_did: Query = None,
        schema_id: Query = None,
        schema_issuer_did: Query = None,
        schema_name: Query = None,
        schema_version: Query = None
    ) -> CredentialDefinitionsCreatedResult:
        """Internal uplink method for get_created_cred_defs"""

    @returns.json
    @get("/credential-definitions/{cred_def_id}")
    def __get_cred_def(self, *, cred_def_id: str) -> CredentialDefinitionGetResult:
        """Internal uplink method for get_cred_def"""

    @returns.json
    @json
    @post("/credential-definitions")
    def __publish_cred_def(
        self,
        *,
        conn_id: Query = None,
        create_transaction_for_endorser: Query = None,
        body: Body(type=CredentialDefinitionSendRequest) = {}
    ) -> Union[CredentialDefinitionSendResult, TxnOrCredentialDefinitionSendResult]:
        """Internal uplink method for publish_cred_def"""
