#!/bin/bash

echo "Deploying TMS v2"
echo "========================================="
echo "Prepared by Md. Rafat Hossain"
echo "Date: 14 December 2022"
echo "========================================="

echo -n "Cleaning up existing docker containers..."

docker kill $(docker ps -q --filter "name=tmsv2") >/dev/null 2>&1

docker system prune -a -f --volumes >/dev/null 2>&1

shopt -s extglob

#systemctl restart docker
#
echo "COMPLETE"

echo -n "Creating docker data directory..."

mkdir -p /aamarpay/docker_persistent/tmsv2/postgres_db >/dev/null 2>&1

echo "COMPLETE"

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

echo -n "Bringing up docker container..."

docker-compose -f "$SCRIPT_DIR/docker-compose.yml" up -d

docker system prune -a -f >/dev/null 2>&1

echo "COMPLETE"

#cp -n "$SCRIPT_DIR/env.example" "$SCRIPT_DIR/.env"

echo "Deployment completed successfully."
echo "========================================="