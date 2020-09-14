"""
Controller for a PryVote voter.
Will be moved to pryvote dir when basic-controller is pip-installable.
"""
from uuid import uuid4

from .aries_controller import AriesAgentController


class VoterController(AriesAgentController):
    def __init__(self, webhook_host: str, webhook_port: int, admin_url: str, webhook_base: str = "") -> None:
        super().__init__(webhook_host, webhook_port, admin_url, webhook_base, connections=True, messaging=True, issuer=False)

        self._id = uuid.uuid4()
        self._vote_shares = None
        self._voting_session = None

    def update_voting_session(self, voting_session) -> None:
        self._voting_session = voting_session

    def update_vote(self, vote_value: str) -> None:
        if self._voting_session is None:
            print(f"A voting session has not been set for {self._id}")
            return

        try:
            vote_class = self._voting_session.get_vote_class(vote_value)

            onehot_votes = [0] * len(self._voting_session)
            onehot_votes[vote_class] = 1

            vote_shares = [self._encrypt_vote(binary_vote) for binary_vote in onehot_votes]

             # transpose the list to get a list of 4 vote values (the four options) for each vote share piece (the vote counters)
            self._vote_shares = list(map(list, zip(*vote_shares)))
        except KeyError:
            self._vote_shares = None

    def _encrypt_vote(self, vote: int):
        Q = self._voting_session.Q

        share_a = random.randint(-Q,Q)
        share_b = random.randint(-Q,Q)
        share_c = (vote - share_a - share_b) % Q
        return (share_a, share_b,  share_c)

    def send_vote(self, *parties) -> None:
        # TODO update to vote counter connection IDs
        if self._vote_shares is None:
            print(f"{self._id} has not set a vote")
            return

        assert len(self._vote_shares) == len(parties)

        for vote_share, party in zip(self._vote_shares, parties):
            party.receive_vote(self._id, vote_share)

        # Expire the vote session to help avoid accidental re-voting
        self._voting_session = None
