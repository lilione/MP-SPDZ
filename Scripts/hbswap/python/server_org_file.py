
if __name__=='__main__':
    n = 3

    for i in range(n):
        file = f"Persistence/Transactions-P{i}.data"
        pool_ETH, pool_TOK = 0, 0
        with open(file, 'rb') as f:
            f.seek(6 * 16)
            pool_ETH = f.read(16)
            pool_TOK = f.read(16)

        with open(file, 'wb') as f:
            f.write(pool_ETH + pool_TOK)