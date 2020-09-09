# PryVote

PryVote is a SSI-driven voting project
which builds on the `aries-basic-controller`,
developed in `PyDentity`,
to implement logic for holding voting sessions
and casting votes.

The project is in early development.

Building something with PryVote?
Let us know!

## Examples

#### OpenMined community / voter

These notebooks
(one in "Alice", the other in "Bob")
show a simple method for self-attested votes.
They should be followed concurrently;
section numbers indicate the flow of information.

### Pre-requisites

- Docker

### Environment

- Voter (Bob) Notebook:8889
- Bob Agent:8051
- Vote holder (Alice) Notebook:8888
- Alice Agent:8021
- Ledger Browser:9000

### How to run

Run `bash ./manage up` from this directory.
This spins up two containers, "Alice" and "Bob".
Alice acts as a vote/credential issuer,
and Bob is a voter.

Lots of information will get posted to your terminal.
Scroll up to find the tokens needed to access
the Alice and Bob notebooks.

Quit the notebooks
and run `bash ./manage down`
to close.
