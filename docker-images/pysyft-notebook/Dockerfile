FROM continuumio/miniconda3

ENV WORKSPACE /workspace

ARG jupyter_port
ENV env_jupyter_port=jupyter_port

# Setup workspace environment
RUN apt-get update && apt-get install -y gcc
RUN conda install jupyter notebook=5.7.8
RUN pip install --no-cache-dir syft[udacity,sandbox]
RUN pip install aiohttp PyPubSub asyncio
RUN pip install --index-url https://test.pypi.org/simple/ aries_basic_controller

# Create jupyter notebook workspace
RUN mkdir $WORKSPACE
WORKDIR $WORKSPACE

# Make the image start the jupyer notebook
COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh





# ENTRYPOINT ["/entrypoint.sh", "$env_jupyter_port"]
ENTRYPOINT ["/entrypoint.sh", "8888"]
