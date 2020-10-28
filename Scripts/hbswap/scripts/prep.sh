#!/usr/bin/env bash
set -e

players=3
threshold=1
port=5000

prog="malicious-shamir-party.x"

prepare() {
    make clean
    make -j tldr
    make -j 8 online
    make -j 8 $prog
    echo "MY_CFLAGS = -DINSECURE" >> CONFIG.mine
    bash Scripts/setup-online.sh $players

    mkdir Persistence
}

compile() {
    ./compile.py hbswap_init
    ./compile.py hbswap_inputmask
    ./compile.py hbswap_trade
}

run() {
    ./$prog -N $players -T $threshold -p 0 -pn $port $1 &
    ./$prog -N $players -T $threshold -p 1 -pn $port $1 &
    ./$prog -N $players -T $threshold -p 2 -pn $port $1
}

org() {
    mv 'Persistence/Transactions-P0.data' 'Scripts/hbswap/data/Pool-P0.data'
    mv 'Persistence/Transactions-P1.data' 'Scripts/hbswap/data/Pool-P1.data'
    mv 'Persistence/Transactions-P2.data' 'Scripts/hbswap/data/Pool-P2.data'
}

#prepare
#compile
kill -9 $(lsof -i:5000 -t) || true

rm ./Persistence/* || true
run hbswap_init
#mkdir Scripts/hbswap/data
org