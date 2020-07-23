![om-logo](https://github.com/OpenMined/design-assets/blob/master/logos/OM/horizontal-primary-trans.png)
![Tests](https://github.com/OpenMined/PyVertical/workflows/Tests/badge.svg?branch=master)
![License](https://img.shields.io/github/license/OpenMined/PyVertical)
![OpenCollective](https://img.shields.io/opencollective/all/openmined)


# PyDentity

![Endgame](./images/endgame.png)

In this repo, we're extending a [Distributed Trust System for Privacy Preserving Machine Learning](https://arxiv.org/abs/2006.02456) to work with PySyft. We're using HL-Aries Agents to establish an end-end encrypted channel which will facilitate syft communications. We can then extend this with credentials and governance systems.

# Requirements

* Docker
* Docker Compose v1.24
* [S2i](https://computingforgeeks.com/install-source-to-image-toolkit-on-linux/)

# Structure

This repository contains a series of libraries each with their own README and demos under the libs folder:

* [aries-basic-controller](./libs/aries-basic-controller) - This is a generic python wrapper for an [aries aca-py](https://github.com/hyperledger/aries-cloudagent-python) admin-api.
* [acapy-protocol-example](./libs/acapy-protocol-example) - This is an example library showing how you can extend the core aca-py functionality by writing custom protocols and including them as a plugin to the agent.
* [om-aries-controller](./libs/om-aries-controller) - This library currently extends the basic controller functionality to handle the custom protocol.

The objective is to develop a om-aries-controller for an aca-py instance with protocols specifically designed for sending privacy preserving machine learning messages. The [demo folder](./demo) in the root directory acts as our sketch pad for demonstrating this functionality as it is developed.



# Running the demo

## Note this is incomplete: Try the demo's within the individual libraries.

From root directory run:
```
./manage up
```

Navigate to [researcher notebook](http://localhost:8889), you will find the token for this in the terminal you ran ./manage up from.

Navigate to [data notebook](http://localhost:8888), you will find the token for this in the terminal you ran ./manage up from.

Both jupyter instances should have a notebook, either researcher or data_owner. Open these up and follow the tutorial contained within the notebooks. You can view these notebooks from this repo in the demo folder.

To get the token for the juypter notebook run:

* Alice : `docker logs om-aries-controller_alice-notebook_1`
* Bob : `docker logs om-aries-controller_bob-notebook_1`
