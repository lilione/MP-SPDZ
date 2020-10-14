#!/usr/bin/env bash
set -e

BLS_PRIME=52435875175126190479447740508185965837690552500527637822603658699938581184513
players=3
threshold=1

prog="malicious-shamir-party.x"

kill -9 $(lsof -i:5000 -t) || true

#Scripts/setup-online.sh $players
#make -j 8 $prog

./compile.py uniswap

#./Scripts/mal-shamir.sh uniswap

#rm ./Persistence/* || true


./$prog -N 3 -p 0 -pn 5000 uniswap &
./$prog -N 3 -p 1 -pn 5000 uniswap &
./$prog -N 3 -p 2 -pn 5000 uniswap
