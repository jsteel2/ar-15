#!/usr/bin/env python3

import os
import asyncio
from aiohttp import web
import jinja2
import aiohttp_jinja2
from routes import routes
from comm_server import CommServer
from rev_server import RevServer

HOST = os.getenv("HOST") or "127.0.0.1"
COMM_PORT = os.getenv("COMM_PORT") or 44344
REV_PORT = os.getenv("REV_PORT") or 44345

async def background_tasks(app):
    comm = CommServer()
    rev = RevServer()
    app["comm_server"] = asyncio.create_task(comm.start(HOST, COMM_PORT))
    app["rev_server"] = asyncio.create_task(rev.start(HOST, REV_PORT))
    yield

def main():
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("./templates"))
    app.cleanup_ctx.append(background_tasks)
    app.add_routes(routes)
    web.run_app(app)

if __name__ == '__main__':
    main()
