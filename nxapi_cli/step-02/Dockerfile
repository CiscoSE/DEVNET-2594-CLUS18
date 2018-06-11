FROM  fedora:latest
LABEL maintainer "Tim Miller <timmil@cisco.com>"

WORKDIR /opt

# Install python and pip
RUN     dnf install -y python-pip

# Install required Python modules
RUN     yes | pip install --upgrade requests prometheus_client 

COPY    publish_l2table.py /opt/publish_l2table.py
EXPOSE  8888
USER    nobody

CMD [ "/usr/bin/python", "/opt/publish_l2table.py" ]

