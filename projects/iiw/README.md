# IIW OpenMined ACA-Py, aries-basic-controller & Juypter Notebook demo


* You need [Docker](https://docs.docker.com/compose/install/)
* You need [Source 2 Image](https://github.com/openshift/source-to-image) 

### Config

In the manage file you can configure the parameters of your agent. You may want to change your agents name and api_key. Although this is only for fun so I don't suppose it really matters.

You can also edit your agents configuration flags in the startup.sh file.

Fetch the jupyter notebook token by running `docker logs iiw_iiw-notebook_1`

Navigate to the notebook - [https://localhost:8888](https://localhost:8888)