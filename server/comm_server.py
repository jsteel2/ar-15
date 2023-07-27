#!/usr/bin/env python3

import asyncio
from tcp_server import TCPServer

class CommClient():
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.lock = asyncio.Lock()

    async def write(self, data):
        self.writer.write(data)
        await self.writer.drain()

    async def read(self):
        buf = bytearray()
        while not buf.endswith(b'END\n'):
            data = await self.reader.read(255)
            if len(data) == 0: raise Exception("disconnected")
            buf.extend(data)
        return buf[:-4]

    async def msg(self, data):
        async with self.lock:
            await asyncio.wait_for(self.write(bytes(data, "utf8") + b'\n'), 5)
            return await asyncio.wait_for(self.read(), 5)

    async def script(self, path):
        f = open(path, "r")
        data = f.read()
        f.close()
        return await self.msg(data)

    async def parse(self, script_output):
        s = script_output.split("\n")
        keys = [x.split("=", 1)[0] for x in s]
        out = [x.split("=", 1)[1] for x in s]
        return dict(zip(keys, out))

    async def run(self):
        while True:
            if await self.msg('printf "pongEND\\n"') != b'pong': break
            await asyncio.sleep(10)

class CommServer(TCPServer):
    async def handle_client(self, reader, writer):
        try:
            k = writer.get_extra_info("peername")
            client = CommClient(reader, writer)
            self.clients[k] = client
            await client.run()
        finally:
            del self.clients[k]
            writer.close()
