#!/usr/bin/env python3

import asyncio

class TCPServer():
    def __init__(self):
        self.clients = {}

    async def start(self, host, port):
        s = await asyncio.start_server(self.handle_client, host, port)
        async with s: await s.serve_forever()
