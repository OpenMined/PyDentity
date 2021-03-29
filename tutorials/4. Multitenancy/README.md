# Multitenancy Tutorial

In this tutorial you will learn how to use an ACA-Py instance in multi-tenant mode. This will include:

* Managing subwallets (create, update, delete)
* Interacting with the ACA-Py instance as a subwallet
* Establishing a mediator

**Note: This tutorial also uses a postgres db for the wallet storage of the multi-tenant agent. It is highly recommended to have a look through the docker-compose.yml file to see the additional configuration needed for this (see wallets-db service). As well as the additional ACA-Py flags used by the multitenant-agent service** 