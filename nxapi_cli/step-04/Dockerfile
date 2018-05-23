FROM  fedora:latest
LABEL maintainer "Tim Miller <timmil@cisco.com>"

WORKDIR /opt

# Install python and pip
RUN     dnf install -y python-pip

# Install required Python modules
RUN     yes | pip install --upgrade requests prometheus_client isodate

COPY    publish_vxlan.py /opt/publish_vxlan.py
COPY    connection.py /opt/connection.py
COPY    payloads.py /opt/payloads.py

EXPOSE  8888
USER    nobody

ENV  NXAPI_HOST "host.docker.internal"
ENV  NXAPI_PORT "23456"
ENV  NXAPI_USER "admin"
ENV  NXAPI_PASS "admin"

CMD [ "/usr/bin/python", "/opt/publish_vxlan.py", "--container" ]

