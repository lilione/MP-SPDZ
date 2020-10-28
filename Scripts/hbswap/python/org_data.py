import sys

if __name__=='__main__':
    server_id = sys.argv[1]

    file = f"Persistence/Transactions-P{server_id}.data"
    pool_ETH, pool_TOK = 0, 0
    with open(file, 'rb') as f:
        f.seek(6 * 16)
        pool_ETH = f.read(16)
        pool_TOK = f.read(16)
    file = f"Scripts/hbswap/data/Pool-P{server_id}.data"
    with open(file, 'wb') as f:
        f.write(pool_ETH + pool_TOK)