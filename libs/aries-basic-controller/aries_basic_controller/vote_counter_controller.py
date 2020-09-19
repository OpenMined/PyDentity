"""
Controller for a PryVote vote counter.
Will be moved to pryvote dir when basic-controller is pip-installable.
"""
from typing import List
from uuid import uuid4, UUID

from .aries_controller import AriesAgentController
from .vote_session import VoteSession


class VoteCounterController(AriesAgentController):
    def __init__(self, voting_session: VoteSession, webhook_host: str, webhook_port: int, admin_url: str, webhook_base: str) -> None:
        # Voter counters can issue "has voted" credentials
        super().__init__(webhook_host, webhook_port, admin_url, webhook_base, connections=True, messaging=True, issuer=True)

        self._id = uuid4()
        self._voter_ids = []
        self._voting_session = voting_session
        self._vote_sum = [0] * len(self._voting_session)

    def receive_vote(self, voter_id: UUID, votes: List[int]) -> None:
        if voter_id not in self._voter_ids:
            print(f"{self._id}: Adding vote for {voter_id}")
            self._voter_ids.append(voter_id)

            for i in range(len(votes)):
                self._vote_sum[i] += votes[i]
        else:
            print(f"{self._id}: {voter_id} has already voted")
