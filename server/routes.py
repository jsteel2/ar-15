#!/usr/bin/env python3

from aiohttp import web

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
        rev.clients[token].writer.write(bytes(msg, "utf8"))
        await rev.clients[token].writer.drain()

    return ws
