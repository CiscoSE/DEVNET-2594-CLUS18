#!/bin/bash

# Stop and remove collector docker instance
docker stop icam
docker rm icam

# Stop and remove prometheus docker instance
docker stop prometheus
docker rm prometheus

