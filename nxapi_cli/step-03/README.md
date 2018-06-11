# Overview
This stage extends the script functionality to:
- Add additional metrics collected
- Abstract connection code into a separate Python module
- Abstract the payload templating into separate Python module
- Add support for environment variables in order to run multiple instances, collecting metrics from multiple switch targets.

# Containerization Steps
Build the Docker image for this command:
    docker build -t devnet-2594/step-03:latest -t devnet-2594/step-03:1 .

# Operational Deployment
(If not already created in previous step) Create a Docker network to which 
the containers will connect:

    docker network create --driver=bridge --subnet=192.168.254.0/24 \
                          --gateway=192.168.254.254 --attachable demo0

Deploy the icam collector container:

    docker run --name icam -d --network demo0 -p 127.0.0.1:8888:8888 devnet-2594/step-03

Deploy Prometheus container:

    docker run --name prometheus -d --network demo0 \
               -p 127.0.0.1:9090:9090 \
               -v ${PWD}/prometheus.yml:/etc/prometheus/prometheus.yml \
               quay.io/prometheus/prometheus
