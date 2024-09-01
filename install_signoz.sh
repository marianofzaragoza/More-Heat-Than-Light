#!/usr/bin/env bash
#
cd /home/user

git clone -b main https://github.com/SigNoz/signoz.git && cd signoz/deploy/
docker compose -f docker/clickhouse-setup/docker-compose.yaml up -d

