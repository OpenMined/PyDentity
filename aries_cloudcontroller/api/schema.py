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

from aries_cloudcontroller.model.schema_get_result import SchemaGetResult
from aries_cloudcontroller.model.schema_send_request import SchemaSendRequest
from aries_cloudcontroller.model.schema_send_result import SchemaSendResult
from aries_cloudcontroller.model.schemas_created_result import SchemasCreatedResult
from aries_cloudcontroller.model.txn_or_schema_send_result import TxnOrSchemaSendResult


class SchemaApi(Consumer):
    async def get_created_schemas(
        self,
        *,
        schema_id: Optional[str] = None,
        schema_issuer_did: Optional[str] = None,
        schema_name: Optional[str] = None,
        schema_version: Optional[str] = None
    ) -> SchemasCreatedResult:
        """Search for matching schema that agent originated"""
        return await self.__get_created_schemas(
            schema_id=schema_id,
            schema_issuer_did=schema_issuer_did,
            schema_name=schema_name,
            schema_version=schema_version,
        )

    async def get_schema(self, *, schema_id: str) -> SchemaGetResult:
        """Gets a schema from the ledger"""
        return await self.__get_schema(
            schema_id=schema_id,
        )

    async def publish_schema(
        self,
        *,
        conn_id: Optional[str] = None,
        create_transaction_for_endorser: Optional[bool] = None,
        body: Optional[SchemaSendRequest] = None
    ) -> Union[SchemaSendResult, TxnOrSchemaSendResult]:
        """Sends a schema to the ledger"""
        return await self.__publish_schema(
            conn_id=conn_id,
            create_transaction_for_endorser=bool_query(create_transaction_for_endorser),
            body=body,
        )

    async def write_record(self, *, schema_id: str) -> SchemaGetResult:
        """Writes a schema non-secret record to the wallet"""
        return await self.__write_record(
            schema_id=schema_id,
        )

    @returns.json
    @get("/schemas/created")
    def __get_created_schemas(
        self,
        *,
        schema_id: Query = None,
        schema_issuer_did: Query = None,
        schema_name: Query = None,
        schema_version: Query = None
    ) -> SchemasCreatedResult:
        """Internal uplink method for get_created_schemas"""

    @returns.json
    @get("/schemas/{schema_id}")
    def __get_schema(self, *, schema_id: str) -> SchemaGetResult:
        """Internal uplink method for get_schema"""

    @returns.json
    @json
    @post("/schemas")
    def __publish_schema(
        self,
        *,
        conn_id: Query = None,
        create_transaction_for_endorser: Query = None,
        body: Body(type=SchemaSendRequest) = {}
    ) -> Union[SchemaSendResult, TxnOrSchemaSendResult]:
        """Internal uplink method for publish_schema"""

    @returns.json
    @post("/schemas/{schema_id}/write_record")
    def __write_record(self, *, schema_id: str) -> SchemaGetResult:
        """Internal uplink method for write_record"""
