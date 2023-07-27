#!/usr/bin/env python3

from tcp_server import TCPServer

class RevServer(TCPServer):
    async def handle_client(self, reader, writer):
        print("ugh")
