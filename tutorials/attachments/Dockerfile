FROM continuumio/miniconda3

ENV WORKSPACE /workspace

ARG jupyter_port
ENV env_jupyter_port=jupyter_port
# Setup workspace environment
RUN apt-get update && apt-get install -y gcc
RUN conda install jupyter notebook=5.7.8

#ADD aries-basic-controller aries-basic-controller
#
#
#RUN pip install --no-cache-dir -e aries-basic-controller



ADD libs/attachment-controller attachment-controller

#ADD setup.py ./om-controller/setup.py
#
#ADD README.md ./om-controller/README.md
#ADD requirements.txt ./om-controller/requirements.txt
#
#RUN cd om-controller

RUN pip install --no-cache-dir -e attachment-controller


WORKDIR $WORKSPACE

# Make the image start the jupyer notebook
COPY scripts/jupyter-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# ENTRYPOINT ["/entrypoint.sh", "$env_jupyter_port"]
ENTRYPOINT ["/entrypoint.sh", "8888"]