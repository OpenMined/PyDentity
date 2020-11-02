FROM bcgovimages/aries-cloudagent:py36-1.15-0_0.5.6

ADD configuration .

USER root
RUN apt-get update
RUN apt-get update && apt-get install -y gcc
RUN pip3 install python3-indy
RUN pip3 install aries-cloudagent


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