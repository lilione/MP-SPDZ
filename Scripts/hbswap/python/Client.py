import asyncio
import re
import toml

from aiohttp import ClientSession
from utils import get_inverse, p

class Client:
    def __init__(self, n, t, servers):
        self.n = n
        self.t = t
        self.servers = servers

    @classmethod
    def from_toml_config(self, config_file):
        config = toml.load(config_file)

        n = config['n']
        t = config['t']
        servers = config["servers"]

        return Client(n, t, servers)

    async def send_request(self, url):
        async with ClientSession() as session:
            async with session.get(url) as resp:
                json_response = await resp.json()
                return json_response

    async def req_inputmask_shares(self, host, port, inputmask_idxes):
        url = f"http://{host}:{port}/inputmasks/{inputmask_idxes}"
        result = await self.send_request(url)
        return re.split(',', result["inputmask_shares"])

    def interpolate(self, shares):
        inputmask = 0
        for i in range(1, self.n + 1):
            tot = 1
            for j in range(1, self.n + 1):
                if i == j:
                    continue
                tot = tot * j * get_inverse(j - i) % p
            inputmask = (inputmask + shares[i - 1] * tot) % p
        return inputmask
    
    # **** call from remote client ****
    async def get_inputmasks(self, inputmask_idxes):
        tasks = []
        for server in self.servers:
            host = server["host"]
            port = server["http_port"]

            task = asyncio.ensure_future(self.req_inputmask_shares(host, port, inputmask_idxes))
            tasks.append(task)

        for task in tasks:
            await task

        inputmask_shares = []
        for task in tasks:
            inputmask_shares.append(task.result())

        inputmasks = []
        for i in range(len(tasks[0].result())):
            shares = []
            for j in range(len(self.servers)):
                shares.append(int(inputmask_shares[j][i]))
            inputmasks.append(self.interpolate(shares))
        return inputmasks