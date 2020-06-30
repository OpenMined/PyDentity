# Aries Basic Controller Python

A simple pip installable package for controlling aries agents through admin API calls.

# Install

Package only available on the test at the moment.

`python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps aries_basic_controller`


# Demo

With docker installed, run the example using ./manage start

See the demo folder for an example of how to use the aries_basic_controller in your project.

Current functionality:
* Spin up two docker images for the researcher and data owner agents
* Load the example.py file
    * Create webhook listeners for connection and basic messages
    * Establish connection between two agents
    * Send basic messages between two agents
    * Listen for webhook events


# Tutorial

```python
from aries_basic_controller import AriesAgentController


# Based on the aca-py agent you wish to control
agent_controller = AriesAgentController(WEBHOOK_HOST, WEBHOOK_PORT, WEBHOOK_BASE, ADMIN_URL)

# Spins up server to respond to any webhook events from the agent
await agent_controller.listen_webhooks()

# Controllers re-emit webhooks as events through PyPubSub
# Basic state management is handled through defaults but you can choose to pass in custom handlers
agent_controller.register_listeners(custom_handler, defaults=True)

# Create Invitation
invite = await agent_controller.connections.create_invitation(alias="Will")


```

# Contributing

This is a part of a project being developed within the [Open Mined](https://openmined.org) open source community. We welcome new contributors, either join our slack channel or just comment on an issue.