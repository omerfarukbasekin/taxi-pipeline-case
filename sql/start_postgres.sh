#!/bin/bash
set -e

docker volume create pgdata || true

docker run -d \
  --name postgres \
  -e POSTGRES_DB=... \
  -e POSTGRES_USER=... \
  -e POSTGRES_PASSWORD=... \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:15
