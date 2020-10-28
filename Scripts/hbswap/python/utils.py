import os
import shutil

from gmpy import binary, mpz

def get_inverse(a):
    ret = 1
    b = p - 2
    while b:
        if b % 2 == 1:
            ret = (ret * a) % p
        b //= 2
        a = (a * a) % p
    return ret

def to_hex(x):
    x = mpz(x)
    x = (x * R) % p
    return binary(int(x))

p = 170141183460469231731687303715885907969
R = -3604482
inverse_R = get_inverse(R)
f = 16