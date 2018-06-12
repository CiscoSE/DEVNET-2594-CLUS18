# Demo scripts showcasing NXAPI functionality
The following functionality is demonstrated in this directory tree:
- step-01 : iCAM metric generation
  - basic HTTP request formation
  - NXAPI CLI JSON RPC payload creation
  - POSTing CLI and parsing output from NXOS switch

- step-02 : iCAM metric collection
  - extend script in step-01 to include code that stores metrics
    in Prometheus data objects for collection
  - Build a Docker container to run that generation script
  - Deploy a Prometheus container to collect the metrics

- step-03 : expand iCAM metrics and refactor code
  - Add a few more metrics to collect into the code
  - Restructure the script to make reusable components

- step-04 : route metrics and Grafana visualization
  - Use modified script to collect routing information from sandbox
  - Deploy Grafana container
  - Configure Grafana to leverage Prometheus
  - Configure dashboards

