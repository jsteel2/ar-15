#!/usr/bin/env python3

from tcp_server import TCPServer
from routes import ws_clients

class RevServer(TCPServer):
    async def handle_client(self, reader, writer):
        token = None
        try:
            buf = bytearray()
            while not buf.endswith(b'END\n'):
                data = await reader.read(255)
                if len(data) == 0: raise Exception("disconnected")
                buf.extend(data)
            token = buf[:-4]
            self.clients[token] = (reader, writer)
            while True:
                data = await reader.read(255)
                if len(data) == 0: raise Exception("disconnected")
                await ws_clients[token].send_str(str(data, "utf8"))
        finally:
            if token: del self.clients[token]
            writer.close()
