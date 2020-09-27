![om-logo](https://github.com/OpenMined/design-assets/blob/master/logos/OM/horizontal-primary-trans.png)
![Tests](https://github.com/OpenMined/PyVertical/workflows/Tests/badge.svg?branch=master)
![License](https://img.shields.io/github/license/OpenMined/PyVertical)
![OpenCollective](https://img.shields.io/opencollective/all/openmined)


# PyDentity

In this repo we are creating a set of libraries to facilitate education and experimentation with the Hyperledger Aries framework for implementing secure identification and authentication procedures using Decentralised Identifiers(DIDs) and Verifiable Credentials (VCs).

Ultimately we are exploring how to create a [Distributed Trust System for Privacy Preserving Machine Learning](https://arxiv.org/abs/2006.02456) that can work with PySyft. We're using HL-Aries Agents to establish an end-end encrypted channel which will facilitate syft communications. We can then extend this with credentials and governance systems.

![Endgame](./images/endgame.png)

**This is very experimental at this stage.**

## Tutorials

In the tutorials folder you will find a set of series of juypter notebook tutorials walking through how to use the libraries contained within this repository. Each tutorial series can be run from it's folder using `./manage up`

### [SSI Basics with Hyperledger](./tutorials/aries-basic-controller)

This series introduces Self-Sovereign Identity and provides all the information needed to get started developing with the Hyperledger SSI stack using the aries-basic-controller library we developed to provide code examples within the notebooks.

**This is a great place to start!** 

### [Making SSI "Real"](./tutorials/aries-stagingnet)

In this series you will learn how to move your solutions from a local test network onto the publicly accessible internet by connecting to the Sovrin StagingNet.

## Libraries


### [aries-basic-controller](./libs/aries-basic-controller)

This is the core library in this repository. It is a simple python wrapper for the swagger api interface to an [aca-py ssi agent](https://github.com/hyperledger/aries-cloudagent-python). 

### [acapy-protocol-example](./libs/acapy-protocol-example)

This library gives a very basic example of how to extend the core set of protocols that an aca-py agent understand with a custom protocol.

### [om-aries-controller](./libs/om-aries-controller)

This library shows how the basic controller can easily be extended to control an agent with custom protocols.

## Projects

### [Opus](./projects/opus)

SSI Third Party Credential Onboarding.

### [PryVote](./projects/pryvote)

SSI voting system.

### [Doctors in Training](./projects/doctors-in-training)

A real life use case of SSI developed as part of an NHS INTEROpen hackathon.