#!/usr/bin/env python3

import os
import asyncio
from aiohttp import web
import jinja2
import aiohttp_jinja2
from routes import routes
from comm_server import CommServer
from rev_server import RevServer
import shared

HOST = os.getenv("HOST") or "0.0.0.0"
HTTP_PORT = int(os.getenv("HTTP_PORT") or "8080")
COMM_PORT = int(os.getenv("COMM_PORT") or "44344")
REV_PORT = int(os.getenv("REV_PORT") or "44345")

shared.comm = CommServer()
shared.rev = RevServer()

async def background_tasks(app):
    app["comm_server"] = asyncio.create_task(shared.comm.start(HOST, COMM_PORT))
    app["rev_server"] = asyncio.create_task(shared.rev.start(HOST, REV_PORT))
    yield

def main():
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("./templates"))
    app.cleanup_ctx.append(background_tasks)
    app.add_routes(routes)
    web.run_app(app, port=HTTP_PORT)

if __name__ == '__main__':
    main()
