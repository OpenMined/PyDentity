# PryVote

PryVote is a SSI-driven voting project
which builds on the `aries-basic-controller`,
developed in `PyDentity`,
to implement logic for holding voting sessions
and casting votes.

The project is in early development.
We are implementing minimal examples
to demonstrate how to use PryVote.

Building something with PryVote?
Let us know!

## Examples

#### Login and parsing

This notebook, in the "Alice" folder,
demonstrates a method for validating a GitHub account.
This can be used to issue credentials
of GitHub community membership.

#### OpenMined community / voter

These notebooks
(one in "Alice", the other in "Bob")
show a simple method for self-attested votes.
They should be followed concurrently;
section numbers indicate the flow of information.


### Pre-requisites

- Docker

### How to run

Run `bash ./manage up` from this directory.
This spins up two containers, "Alice" and "Bob".
Alice acts as a vote/credential issuer,
and Bob is a voter.

Lots of information will get posted to your terminal.
Scroll up to find links to connect to the Alice and Bob agents,
or go to both localhost `8888` and `8889`
in a browser of your choice.

Quit the notebooks
and run `bash ./manage down`
to close.
