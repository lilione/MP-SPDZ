#!/usr/bin/env bash
set -e

kill -9 $(lsof -i:8545 -t) || true
rm -rf Scripts/hbswap/poa/data
bash Scripts/hbswap/scripts/chain.sh

go run Scripts/hbswap/go/deploy/deploy.go