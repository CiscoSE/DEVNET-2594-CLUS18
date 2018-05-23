# Overview
This stage extends the script functionality to:
- Collect metrics related to VXLAN IP routes
- Leverage code abstractions and environment variables from step-03

# Containerization Steps
Build the Docker image for this command:

    docker build -t devnet-2594/step-04:latest -t devnet-2594/step-04:1 .

# Operational Deployment
Create a Docker network to which the containers will connect:

    docker run --name nx-osv9000-1 -d --network demo0 -p 127.0.0.1:8891:8888 \
            -e "NXAPI_HOST=172.16.30.101" -e "NXAPI_PORT=80" \
            -e "NXAPI_USER=cisco" -e "NXAPI_PASS=cisco" \
            devnet-2594/step-04
    docker run --name nx-osv9000-2 -d --network demo0 -p 127.0.0.1:8892:8888 \
            -e "NXAPI_HOST=172.16.30.102" -e "NXAPI_PORT=80" \
            -e "NXAPI_USER=cisco" -e "NXAPI_PASS=cisco" \
            devnet-2594/step-04
    docker run --name nx-osv9000-3 -d --network demo0 -p 127.0.0.1:8893:8888 \
            -e "NXAPI_HOST=172.16.30.103" -e "NXAPI_PORT=80" \
            -e "NXAPI_USER=cisco" -e "NXAPI_PASS=cisco" \
            devnet-2594/step-04
    docker run --name nx-osv9000-4 -d --network demo0 -p 127.0.0.1:8894:8888 \
            -e "NXAPI_HOST=172.16.30.104" -e "NXAPI_PORT=80" \
            -e "NXAPI_USER=cisco" -e "NXAPI_PASS=cisco" \
            devnet-2594/step-04`

Deploy Prometheus container:

    docker run --name prometheus -d --network demo0 \
            -p 127.0.0.1:9090:9090 \
            -v ${PWD}/prometheus.yml:/etc/prometheus/prometheus.yml \
            quay.io/prometheus/prometheus
