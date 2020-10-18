# python3 Scripts/client.py

from gmpy2 import mpz_from_old_binary
from gmpy import binary
import sys

def get_inverse(a):
    ret = 1
    b = mod - 2
    while b:
        if b % 2 == 1:
            ret = (ret * a) % mod
        b //= 2
        a = (a * a) % mod
    return ret

def format(x):
    if x >= mod / 2:
        x -= mod
    return x

def read(f, start_posn):
    f.seek(start_posn)
    _x = f.read(16)
    x = (mpz_from_old_binary(_x) * get_inverse(magic_number)) % mod
    return format(x)

def to_hex(x):
    x = (x * magic_number) % mod
    return binary(int(x))

def read_share(idx):
    x, y = [], []

    for i in range(n):
        file = f"Persistence/Transactions-P{i}.data"
        with open(file, 'rb') as f:
            x.append(i + 1)
            y.append(read(f, idx * 16))

    inputmask = 0
    for i in range(n):
        tot = 1
        for j in range(n):
            if i == j:
                continue
            tot = tot * x[j] * get_inverse(x[j] - x[i]) % mod
        inputmask = (inputmask + y[i] * tot) % mod

    return inputmask

def append_share(x):
    for i in range(n):
        file = f"Persistence/Transactions-P{i}.data"
        with open(file, 'ab') as f:
            f.write(to_hex(x))

if __name__=='__main__':
    n = 3
    mod = 170141183460469231731687303715885907969
    magic_number = -3604482
    f = 16

    amt_ETH = int(round(float(sys.argv[1]) * (2 ** f)))
    amt_TOK = int(round(float(sys.argv[2]) * (2 ** f)))

    masked_amt_ETH = amt_ETH + read_share(2)
    masked_amt_TOK = amt_TOK + read_share(3)

    append_share(masked_amt_ETH)
    append_share(masked_amt_TOK)