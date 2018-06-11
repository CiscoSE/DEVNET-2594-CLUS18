#!/bin/bash

# Stop and remove collector docker instance
docker stop collector
docker rm collector

# Stop and remove prometheus docker instance
docker stop prometheus
docker rm prometheus

