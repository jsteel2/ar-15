#!/usr/bin/env python3

import os
import traceback
import asyncio
from aiohttp import web
import jinja2
import aiohttp_jinja2
from routes import routes
from comm_server import CommServer
from rev_server import RevServer
import shared
import pci

HOST = os.getenv("HOST") or "0.0.0.0"
HTTP_PORT = int(os.getenv("HTTP_PORT") or "8080")
COMM_PORT = int(os.getenv("COMM_PORT") or "44344")
REV_PORT = int(os.getenv("REV_PORT") or "44345")

shared.comm = CommServer()
shared.rev = RevServer()

async def background_tasks(app):
    await pci.init()
    app["comm_server"] = asyncio.create_task(shared.comm.start(HOST, COMM_PORT))
    app["rev_server"] = asyncio.create_task(shared.rev.start(HOST, REV_PORT))
    yield

def json_error(code, e):
    return web.json_response({"error": e.__class__.__name__, "detail": str(e)}, status=code)

async def error_middleware(app, handler):
    async def m(request):
        try:
            response = await handler(request)
            if response.status == 404: return json_error(404, Exception(response.message))
            return response
        except web.HTTPException as e:
            if e.status == 404: return json_error(404, e)
            raise
        except Exception as e:
            print(f"Request {request} has failed with exception: {traceback.format_exc()}")
            return json_error(500, e)

    return m

def main():
    app = web.Application(middlewares=[error_middleware])
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("./templates"))
    app.cleanup_ctx.append(background_tasks)
    app.add_routes(routes)
    web.run_app(app, host=HOST, port=HTTP_PORT)

if __name__ == '__main__':
    main()
