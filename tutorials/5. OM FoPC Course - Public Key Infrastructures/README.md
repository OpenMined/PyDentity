# OpenMined Public Key Infastructure Lesson

This set of notebooks is part of the OpenMined PKI lesson series.

To start the tutorial first install the prerequisites:

## Requirements

This project is written in Python and is displayed in jupyter notebooks.

You need to install:
1. [Docker](https://docs.docker.com/get-docker/)
2. [docker-compose](https://docs.docker.com/compose/install/)
3. The **source-to-image** (s2i) tool is also required to build the docker images used in the demo. S2I can be downloaded [here](https://github.com/openshift/source-to-image). The website gives instructions for installing on other platforms like MACOS, Linux, Windows.
Verify that **s2i** is in your PATH.  If not, then edit your PATH and add the directory where **s2i** is installed.  The **manage** script will look for the **s2i** executable on your PATH.  If it is not found you will get a message asking you to download and set it on your PATH.
    - If you are using a Mac and have Homebrew installed, the following command will install s2i: `brew install source-to-image`
    - If you are using Linux, go to the [releases](https://github.com/openshift/source-to-image/releases/latest) page and download the correct distribution for your machine. Choose either the linux-386 or the linux-amd64 links for 32 and 64-bit, respectively. Unpack the downloaded tar with `tar -xvf "Release.tar.gz"`
    - If you are not sure about your Operating System you can visit [this](https://whatsmyos.com/) and/or follow the instructions.
    - You should now see an executable called s2i. Either add the location of s2i to your PATH environment variable, or move it to a pre-existing directory in your PATH. For example, `sudo cp /path/to/s2i /usr/local/bin` will work with most setups. You can test it using `s2i version`.

Ensure that Docker is running. If it is not try `sudo dockerd` in another terminal.


# Start Up

* First copy the provided example.env files to .env files in each of the actors folders. E.g. `cp actors/datascientist/example.env actors/datascientist/.env`
* These specify the configuration parameters for the agent, including ports and API Keys.
* Then run `./manage start` (From within this tutorial folder) - This calls the `manage` bash script and spins up the docker services defined in `docker-compose.yml`
* Get Notebook Urls using `./scripts/get_URLs` (Must be from Root Repo folder)


## This tutorial has been updated to follow the [Aries-Jupyter-Playground](https://github.com/wip-abramson/aries-jupyter-playground) configuration setup. Which is why it is slightly different from the other projects in this repo.


