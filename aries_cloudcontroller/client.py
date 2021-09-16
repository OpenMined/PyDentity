from contextlib import AbstractAsyncContextManager
from typing import Dict

import uplink

from aries_cloudcontroller.api import (
    ActionMenuApi,
    BasicmessageApi,
    ConnectionApi,
    CredentialDefinitionApi,
    CredentialsApi,
    DidExchangeApi,
    EndorseTransactionApi,
    IntroductionApi,
    IssueCredentialV10Api,
    IssueCredentialV20Api,
    JsonldApi,
    LedgerApi,
    MediationApi,
    MultitenancyApi,
    OutOfBandApi,
    PresentProofV10Api,
    PresentProofV20Api,
    ResolverApi,
    RevocationApi,
    SchemaApi,
    ServerApi,
    TrustpingApi,
    WalletApi,
)


class Client(AbstractAsyncContextManager):
    action_menu: ActionMenuApi
    basicmessage: BasicmessageApi
    connection: ConnectionApi
    credential_definition: CredentialDefinitionApi
    credentials: CredentialsApi
    did_exchange: DidExchangeApi
    endorse_transaction: EndorseTransactionApi
    introduction: IntroductionApi
    issue_credential_v1_0: IssueCredentialV10Api
    issue_credential_v2_0: IssueCredentialV20Api
    jsonld: JsonldApi
    ledger: LedgerApi
    mediation: MediationApi
    multitenancy: MultitenancyApi
    out_of_band: OutOfBandApi
    present_proof_v1_0: PresentProofV10Api
    present_proof_v2_0: PresentProofV20Api
    resolver: ResolverApi
    revocation: RevocationApi
    schema: SchemaApi
    server: ServerApi
    trustping: TrustpingApi
    wallet: WalletApi

    def __init__(
        self,
        base_url: str,
        client: uplink.AiohttpClient,
        *,
        extra_service_params: Dict = {}
    ):
        self.base_url = base_url
        service_params = {
            **extra_service_params,
            "base_url": base_url,
            "client": client,
        }

        self.action_menu = ActionMenuApi(**service_params)
        self.basicmessage = BasicmessageApi(**service_params)
        self.connection = ConnectionApi(**service_params)
        self.credential_definition = CredentialDefinitionApi(**service_params)
        self.credentials = CredentialsApi(**service_params)
        self.did_exchange = DidExchangeApi(**service_params)
        self.endorse_transaction = EndorseTransactionApi(**service_params)
        self.introduction = IntroductionApi(**service_params)
        self.issue_credential_v1_0 = IssueCredentialV10Api(**service_params)
        self.issue_credential_v2_0 = IssueCredentialV20Api(**service_params)
        self.jsonld = JsonldApi(**service_params)
        self.ledger = LedgerApi(**service_params)
        self.mediation = MediationApi(**service_params)
        self.multitenancy = MultitenancyApi(**service_params)
        self.out_of_band = OutOfBandApi(**service_params)
        self.present_proof_v1_0 = PresentProofV10Api(**service_params)
        self.present_proof_v2_0 = PresentProofV20Api(**service_params)
        self.resolver = ResolverApi(**service_params)
        self.revocation = RevocationApi(**service_params)
        self.schema = SchemaApi(**service_params)
        self.server = ServerApi(**service_params)
        self.trustping = TrustpingApi(**service_params)
        self.wallet = WalletApi(**service_params)

        self.client = client

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.close()

    async def close(self):
        await self.client.close()
