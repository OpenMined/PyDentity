"""
Code for managing voting sessions
"""
from typing import List, Optional

import numpy as np


class VoteSession:
    """
    Base class for voting sessions.
    """

    def __init__(self, *options, vote_title: Optional[str] = None) -> None:
        vote_values = {}
        for i, option in enumerate(options):
            vote_values[option] = i

        self._vote_values = vote_values
        self._vote_classes = {v: k for k, v in vote_values.items()}

        self._results = None
        self._vote_title = vote_title

    @property
    def ongoing(self) -> bool:
        """
        Whether or not the vote is active

        Returns:
            bool : True if no results have been calculated, otherwise False
        """
        return self._results is None

    def __len__(self) -> int:
        return len(self._vote_values)

    def get_vote_class(self, vote_value: str) -> int:
        return self._vote_values[vote_value]

    def get_vote_value(self, vote_class: int) -> str:
        return self._vote_classes[vote_class]

    def add_results(self, results) -> None:
        raise NotImplementedError("add_results must be implemented by base class")

    def calculate_winner(self):
        raise NotImplementedError("calculate_winner must be implemented by base class")

    def __str__(self) -> str:
        s = f"{self._vote_title}\n"
        s += f"Vote options are: {', '.join(self._vote_values.keys())}\n"
        s += f"Vote is {'ongoing' if self.ongoing else 'finished'}"
        return s


class SMPCVoteSession(VoteSession):
    def __init__(self, Q: int, *options, vote_title: str = "SMPC Vote") -> None:
        super().__init__(*options, vote_title=vote_title)

        self._Q = Q

    def add_results(self, results: List[int]) -> None:
        self._results = results

    def calculate_winner(self) -> str:
        if self.ongoing:
            raise RuntimeError("Vote is ongoing")
        else:
            decrypted_vote_counts = [shares % self._Q for shares in self._results]
            return self.get_vote(np.argmax(decrypted_vote_counts))
