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
    if x > mod / 2:
        x -= mod
    return x

def read(f):
    _x = f.read(16)
    x = (-mpz_from_old_binary(_x) * get_inverse(magic_number)) % mod
    return format(x)

def write(f, x):
    x = format((-x * magic_number) % mod)
    x = binary(int(x))
    f.write(x)

if __name__=='__main__':
    n = 3
    mod = 170141183460469231731687303715885907969
    magic_number = 3604482

    v = int(sys.argv[1])

    x, y = [], []

    for i in range(n):
        file = f"Persistence/Transactions-P{i}.data"
        with open(file, 'rb') as f:
            x.append(i + 1)
            y.append(read(f))

    inputmask = 0
    for i in range(n):
        tot = 1
        for j in range(n):
            if i == j:
                continue
            tot = tot * x[j] * get_inverse(x[j] - x[i]) % mod
        inputmask = (inputmask + y[i] * tot) % mod

    masked_input = v + inputmask

    for i in range(n):
        file = f"Persistence/Transactions-P{i}.data"
        with open(file, 'ab') as f:
            write(f, masked_input)

