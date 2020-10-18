#!/usr/bin/env bash
set -e

players=3
threshold=1
port=5000

prog="malicious-shamir-party.x"

prepare() {
    make -j 8 $prog
    #Scripts/setup-online.sh $players

    kill -9 $(lsof -i:5000 -t) || true
    rm ./Persistence/* || true
}

compile() {
    ./compile.py honeybadgerswap_init
    ./compile.py honeybadgerswap_inputmask
    ./compile.py honeybadgerswap_trade
}

run() {
    #./Scripts/mal-shamir.sh honeybadgerswap
    ./$prog -N $players -T $threshold -p 0 -pn $port $1 &
    ./$prog -N $players -T $threshold -p 1 -pn $port $1 &
    ./$prog -N $players -T $threshold -p 2 -pn $port $1
}

trade() {
    echo "-----------------------------------------------"
    run honeybadgerswap_inputmask
    echo "-----------------------------------------------"
    python3 Scripts/client.py $1 $2
    echo "-----------------------------------------------"
    run honeybadgerswap_trade
    echo "-----------------------------------------------"
    python3 Scripts/server_org_file.py
}

prepare
compile

run honeybadgerswap_init
trade 1.1 -2.5
trade -1.1 2