FROM bcgovimages/aries-cloudagent:py36-1.15-0_0.5.6

ADD configuration ./configuration

#USER root
#RUN apt-get update
#RUN apt-get update && apt-get install -y gcc
#USER indy
#RUN pip3 install python3-indy
#RUN pip3 install aries-cloudagent

#ENV PATH=/home/indy/.local/bin:/home/indy/bin:/home/indy/.pyenv/shims:/home/indy/.pyenv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
#ENV LD_LIBRARY_PATH=/home/indy/.local/lib:

#ADD requirements*.txt ./
#
#RUN pip3 install --no-cache-dir -r requirements.txt -r requirements.dev.txt
#
#ADD aries_cloudagent ./aries_cloudagent
#ADD bin ./bin
#ADD README.md ./
#ADD setup.py ./
#
#RUN pip3 install --no-cache-dir -e .
#
#RUN mkdir logs && chown -R indy:indy logs && chmod -R ug+rw logs
#
#ENTRYPOINT ["/bin/bash", "-c", "aca-py \"$@\"", "--"]