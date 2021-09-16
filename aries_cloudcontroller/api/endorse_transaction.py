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

from aries_cloudcontroller.model.date import Date
from aries_cloudcontroller.model.endorser_info import EndorserInfo
from aries_cloudcontroller.model.transaction_jobs import TransactionJobs
from aries_cloudcontroller.model.transaction_list import TransactionList
from aries_cloudcontroller.model.transaction_record import TransactionRecord


class EndorseTransactionApi(Consumer):
    async def cancel_transaction(self, *, tran_id: str) -> TransactionRecord:
        """For Author to cancel a particular transaction request"""
        return await self.__cancel_transaction(
            tran_id=tran_id,
        )

    async def create_request(
        self,
        *,
        tran_id: str,
        endorser_write_txn: Optional[bool] = None,
        body: Optional[Date] = None
    ) -> TransactionRecord:
        """For author to send a transaction request"""
        return await self.__create_request(
            tran_id=tran_id,
            endorser_write_txn=endorser_write_txn,
            body=body,
        )

    async def endorse_transaction(self, *, tran_id: str) -> TransactionRecord:
        """For Endorser to endorse a particular transaction record"""
        return await self.__endorse_transaction(
            tran_id=tran_id,
        )

    async def get_records(self) -> TransactionList:
        """Query transactions"""
        return await self.__get_records()

    async def get_transaction(self, *, tran_id: str) -> TransactionRecord:
        """Fetch a single transaction record"""
        return await self.__get_transaction(
            tran_id=tran_id,
        )

    async def refuse_transaction(self, *, tran_id: str) -> TransactionRecord:
        """For Endorser to refuse a particular transaction record"""
        return await self.__refuse_transaction(
            tran_id=tran_id,
        )

    async def resend_transaction_request(self, *, tran_id: str) -> TransactionRecord:
        """For Author to resend a particular transaction request"""
        return await self.__resend_transaction_request(
            tran_id=tran_id,
        )

    async def set_endorser_info(
        self, *, conn_id: str, endorser_did: str, endorser_name: Optional[str] = None
    ) -> EndorserInfo:
        """Set Endorser Info"""
        return await self.__set_endorser_info(
            conn_id=conn_id,
            endorser_did=endorser_did,
            endorser_name=endorser_name,
        )

    async def set_endorser_role(
        self, *, conn_id: str, transaction_my_job: Optional[str] = None
    ) -> TransactionJobs:
        """Set transaction jobs"""
        return await self.__set_endorser_role(
            conn_id=conn_id,
            transaction_my_job=transaction_my_job,
        )

    async def write_transaction(self, *, tran_id: str) -> TransactionRecord:
        """For Author / Endorser to write an endorsed transaction to the ledger"""
        return await self.__write_transaction(
            tran_id=tran_id,
        )

    @returns.json
    @post("/transactions/{tran_id}/cancel")
    def __cancel_transaction(self, *, tran_id: str) -> TransactionRecord:
        """Internal uplink method for cancel_transaction"""

    @returns.json
    @json
    @post("/transactions/create-request")
    def __create_request(
        self,
        *,
        tran_id: Query,
        endorser_write_txn: Query = None,
        body: Body(type=Date) = {}
    ) -> TransactionRecord:
        """Internal uplink method for create_request"""

    @returns.json
    @post("/transactions/{tran_id}/endorse")
    def __endorse_transaction(self, *, tran_id: str) -> TransactionRecord:
        """Internal uplink method for endorse_transaction"""

    @returns.json
    @get("/transactions")
    def __get_records(self) -> TransactionList:
        """Internal uplink method for get_records"""

    @returns.json
    @get("/transactions/{tran_id}")
    def __get_transaction(self, *, tran_id: str) -> TransactionRecord:
        """Internal uplink method for get_transaction"""

    @returns.json
    @post("/transactions/{tran_id}/refuse")
    def __refuse_transaction(self, *, tran_id: str) -> TransactionRecord:
        """Internal uplink method for refuse_transaction"""

    @returns.json
    @post("/transaction/{tran_id}/resend")
    def __resend_transaction_request(self, *, tran_id: str) -> TransactionRecord:
        """Internal uplink method for resend_transaction_request"""

    @returns.json
    @post("/transactions/{conn_id}/set-endorser-info")
    def __set_endorser_info(
        self, *, conn_id: str, endorser_did: Query, endorser_name: Query = None
    ) -> EndorserInfo:
        """Internal uplink method for set_endorser_info"""

    @returns.json
    @post("/transactions/{conn_id}/set-endorser-role")
    def __set_endorser_role(
        self, *, conn_id: str, transaction_my_job: Query = None
    ) -> TransactionJobs:
        """Internal uplink method for set_endorser_role"""

    @returns.json
    @post("/transactions/{tran_id}/write")
    def __write_transaction(self, *, tran_id: str) -> TransactionRecord:
        """Internal uplink method for write_transaction"""
