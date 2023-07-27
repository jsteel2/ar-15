#!/usr/bin/env python3

from aiohttp import web
import shared

routes = web.RouteTableDef()

@routes.get("/")
async def index(request):
    return web.Response(text="sneed")

@routes.get("/rev/{ip}/{port}")
async def rev(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    ip = request.match_info["ip"]
    port = request.match_info["port"]
    token = str(await shared.comm.clients[(ip, int(port))].msg("ls /.__EL_SNEEDIO__/rev"), "utf8") # command needs to be in background?
    shared.ws_clients[token] = ws

    try:
        async for msg in ws:
            shared.rev.clients[token][1].write(bytes(msg.data, "utf8"))
            await shared.rev.clients[token][1].drain()
    finally:
        del shared.ws_clients[token]
        return ws
