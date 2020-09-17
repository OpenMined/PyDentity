![om-logo](https://github.com/OpenMined/design-assets/blob/master/logos/OM/horizontal-primary-trans.png)
![Tests](https://github.com/OpenMined/PyVertical/workflows/Tests/badge.svg?branch=master)
![License](https://img.shields.io/github/license/OpenMined/PyVertical)
![OpenCollective](https://img.shields.io/opencollective/all/openmined)


# PyDentity

In this repo we are creating a set of libraries to facilitate education and experimentation with the Hyperledger Aries framework for implementing secure identification and authentication procedures using Decentralised Identifiers(DIDs) and Verifiable Credentials (VCs).

Ultimately we are exploring how to create a [Distributed Trust System for Privacy Preserving Machine Learning](https://arxiv.org/abs/2006.02456) that can work with PySyft. We're using HL-Aries Agents to establish an end-end encrypted channel which will facilitate syft communications. We can then extend this with credentials and governance systems.

![Endgame](./images/endgame.png)

**This is very experimental at this stage.**

## Libraries

Each library has it's own Readme and set of Juypter Notebook tutorials documenting how it can be used.

### [aries-basic-controller](./libs/aries-basic-controller)

This is the core library in this repository. It is a simple python wrapper for the swagger api interface to an [aca-py ssi agent](https://github.com/hyperledger/aries-cloudagent-python). This is a great place to start.

### [acapy-protocol-example](./libs/acapy-protocol-example)

This library gives a very basic example of how to extend the core set of protocols that an aca-py agent understand with a custom protocol.

### [om-aries-controller](./libs/om-aries-controller)

This library shows how the basic controller can easily be extended to control an agent with custom protocols.

## Projects

### [PryVote](./projects/pryvote)

SSI voting system.
