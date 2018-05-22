# Overview
Extend the standalone L2 table script to support generation and 
publishing of the metric.

# Architecture
Because we will be running this script against a NXOSv VM and 
using a container-based instance of Prometheus, the nuances
of Mac networking, VirtualBox networking, and Docker networking
necessitate converting the script to a Docker image to be run
as a container.

# Containerization Steps
Build the Docker image for this command:
``docker build -t devnet-2594/publish_l2table:latest -t devnet-2594/publish_l2table:1 .``

# Operational Deployment
Create a Docker network to which the containers will connect:
``docker network create --driver=bridge --subnet=192.168.254.0/24 --gateway=192.168.254.254 --attachable demo0``

Deploy Prometheus container:
``docker run --name prometheus -d --network demo0 \
           -p 127.0.0.1:9090:9090 \
           -v ${PWD}/prometheus.yml:/etc/prometheus/prometheus.yml \
           quay.io/prometheus/prometheus``

Deploy our publishing script:
``docker run --name collector -d --network demo0 \
           -p 127.0.0.1:8888:8888 \
           devnet-2594/publish_l2table``

# Background information
Leveraging specific Docker networking DNS entries to have script talk to host
- [https://docs.docker.com/docker-for-mac/networking/#use-cases-and-workarounds]
