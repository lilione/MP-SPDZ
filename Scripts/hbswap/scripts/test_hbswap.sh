# bash Scripts/hbswap/test_hbswap.sh

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
    ./compile.py hbswap_init
    ./compile.py hbswap_inputmask
    ./compile.py hbswap_trade
}

run() {
    #./Scripts/mal-shamir.sh hbswap
    ./$prog -N $players -T $threshold -p 0 -pn $port $1 &
    ./$prog -N $players -T $threshold -p 1 -pn $port $1 &
    ./$prog -N $players -T $threshold -p 2 -pn $port $1
}

trade() {
    echo "-----------------------------------------------"
    run hbswap_inputmask
    echo "-----------------------------------------------"
    python3 Scripts/hbswap/python/hbswap_client.py $1 $2
    echo "-----------------------------------------------"
    run hbswap_trade
    echo "-----------------------------------------------"
    python3 Scripts/hbswap/python/server_org_file.py
}

#prepare
#compile
#
#run hbswap_init
trade 1.1 -2.5
trade -1.1 2