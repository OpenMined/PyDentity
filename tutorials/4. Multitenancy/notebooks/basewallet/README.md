## Alice and Bob

In this tutorial Alice and Bob live on the same notebook server endpoint. That is due to the multitenancy setup.

![multitenancy](https://raw.githubusercontent.com/hyperledger/aries-cloudagent-python/main/docs/assets/multitenancyDiagram.png)

Alice and Bob now reside on the same agent and have hence the same endpoint.

In these tuorials we will create subwallets for both of them on this basewallte multitenant agent. 

We will then continue to explore features of multitenancy and mediation. From the other agent which simulates an external (from another network) entity we will explore how to reach and interact with Bob and Alice via the basewallet agent.