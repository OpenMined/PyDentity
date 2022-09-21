<p align="center">
  <br />
  <img
    alt="Hyperledger Aries logo"
    src="https://raw.githubusercontent.com/didx-xyz/aries-cloudcontroller-python/main/assets/aries-logo.png"
    height="250px"
  />
</p>
<h1 align="center"><b>Aries Cloud Controller Python</b></h1>
<p align="center">
  <img
    alt="Pipeline Status"
    src="https://github.com/didx-xyz/aries-cloudcontroller-python/actions/workflows/python-publish.yml/badge.svg?branch=main"
  />
        <a href="https://pypi.org/project/aries-cloudcontroller/">
        <img alt="aries-cloudcontroller version" src="https://badge.fury.io/py/aries-cloudcontroller.svg"/>
      </a>
  <a
    href="https://raw.githubusercontent.com/didx-xyz/aries-cloudcontroller-python/main/LICENSE"
    ><img
      alt="License"
      src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"
  /></a>
  <a href="https://www.python.org/"
    ><img
      alt="Python"
      src="https://img.shields.io/badge/%3C%2F%3E-Python-%230074c1.svg"
  /></a>
</p>
<br />

<p align="center">
  <a href="#features">Features</a> &nbsp;|&nbsp;
  <a href="#usage">Usage</a> &nbsp;|&nbsp;
  <a href="#available-apis">Available APIs</a> &nbsp;|&nbsp;
  <a href="#contributing">Contributing</a> &nbsp;|&nbsp;
  <a href="#license">License</a> 
</p>

Aries Cloud Controller Python is a client library written in Python for interacting with an [Aries Cloud Agent Python](https://github.com/hyperledger/aries-cloudagent-python) instance. It is generated based on the OpenAPI definition provided by ACA-Py, giving a fully-typed rich API for interacting the cloud agent.

Each Cloud Controller version maps to a specific ACA-Py version, which is outlined in the table below. Although not strictly adhered to in the past, a new ACA-Py version will result in a new Minor version bump for the Cloud Controller, as there are often times breaking changes.

| Aries Cloud Controller Version | Aries Cloud Agent Python Version |
| ------------------------------ | -------------------------------- |
| 0.5.1-0.5.2                    | 0.7.3                            |
| 0.6.0                          | 0.7.4                            |

## Features

Aries Cloud Controller Python is a fully featured client for interacting with ACA-Py.

- Fully Typed wrapper around Aries Cloud Agent Python
- Supports latest ACA-Py version (0.7.4)
- Client is auto generated based on OpenAPI definitions, allowing us to keep up to date with new releases.
- Supports multi-tenant APIs and authentication
- Async API

## Usage

Aries Cloud Controller Python is published to PyPi and can be installed using pip:

```sh
pip install aries-cloudcontroller
```

### Creating a client

```python
from aries_cloudcontroller import AcaPyClient

client = AcaPyClient(
    base_url="http://localhost:8000",
    api_key="myApiKey"
)
```

**Admin insecure mode**

If you are running ACA-Py with the admin insecure flag and don't have the API key, you must set the `admin_insecure` property:

```python
client = AcaPyClient(
    base_url="http://localhost:8000",
    # Explicitly mark that no api key is used
    admin_insecure=True
)
```

**Multitenancy**

To provision the agent in the context of specific tenant of the agent, the `tenant_jwt` property must be set:

```python
client = AcaPyClient(
    base_url="http://localhost:8000",
    tenant_jwt="eyXXX"
)
```

### Interacting with the client

Once you have the client set up, you're ready to interact with it. Because the API is fully typed, the best way to know what is available is by looking at the ACA-Py swagger UI, and the available properties on the client.

For example to create and receive an invitation the following methods can be called:

```python
invitation = await client.connection.create_invitation(
    body=CreateInvitationRequest(my_label="Cloud Controller")
)

connection = await client.connection.receive_invitation(body=result.invitation)
```

## Available APIs

Currently the following top-level APIs are available in the client. Each api maps to the topics as used by the ACA-Py swagger UI.

- `action_menu`
- `basicmessage`
- `connection`
- `credential_definition`
- `credentials`
- `default`
- `did_exchange`
- `discover_features`
- `discover_features_v2_0`
- `endorse_transaction`
- `introduction`
- `issue_credential_v1_0`
- `issue_credential_v2_0`
- `jsonld`
- `ledger`
- `mediation`
- `multitenancy`
- `out_of_band`
- `present_proof_v1_0`
- `present_proof_v2_0`
- `resolver`
- `revocation`
- `schema`
- `server`
- `trustping`
- `wallet`

## Contributing

If you would like to contribute to the framework, please read [CONTRIBUTING](/CONTRIBUTING.md) guidelines. These documents will provide more information to get you started!

## License

Aries Cloud Controller Python is licensed under the [Apache License Version 2.0 (Apache-2.0)](/LICENSE).
