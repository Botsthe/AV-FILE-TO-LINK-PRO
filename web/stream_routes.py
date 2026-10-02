import time
import asyncio
from aiohttp import web
import re
import math
import logging
import secrets
import mimetypes
from aiohttp.http_exceptions import BadStatusLine
from web.bot import multi_clients, work_loads
from web.server.exceptions import FileNotFound, InvalidHash
from web.utils.custom_dl import ByteStreamer
from web.utils.render_template import render_page
from info import *
from utils import temp, get_readable_time
from web.utils import StartTime, __version__
import aiofiles
import jinja2
from database.users_db import db # Apni DB import

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(_):
    return web.json_response({
        "server_status": "running",
        "uptime": get_readable_time(time.time() - StartTime),
        "telegram_bot": "@" + temp.U_NAME,
        "connected_bots": len(multi_clients),
        "loads": {
            "bot" + str(i + 1): load
            for i, (_, load) in enumerate(
                sorted(work_loads.items(), key=lambda x: x[1], reverse=True)
            )
        },
        "version": __version__,
    })

# ---------------------------------------------------------------
#  PASSWORD PROTECTED REDIRECT ROUTES (Add this at the bottom)
# ---------------------------------------------------------------

# Routes Update
@routes.get(r"/p/{token}", allow_head=True)
async def protected_view(request: web.Request):
    token = request.match_info["token"]
    data = await db.get_protected_link(token)
    
    if not data:
        return web.Response(text="Link not found.", status=404)

    async with aiofiles.open("web/template/password_redirect.html", mode='r') as f:
        template_content = await f.read()
        template = jinja2.Template(template_content)

    return web.Response(
        text=template.render(
            token=token,
            title=data.get("title", "Protected Link"),           # Feature 5
            channel_link=data.get("channel_link")                # Feature 1
        ),
        content_type="text/html"
    )

@routes.post(r"/p/{token}")
async def protected_verify(request: web.Request):
    token = request.match_info["token"]
    data = await request.post()
    user_pass = data.get("password")

    link_data = await db.get_protected_link(token)
    
    if not link_data:
        return web.Response(text="Link invalid.", status=404)

    if user_pass == link_data["password"]:
        return web.HTTPFound(link_data["url"])
    else:
        # Error hone par bhi title/link wapas bhejna padega
        async with aiofiles.open("web/template/password_redirect.html", mode='r') as f:
            template_content = await f.read()
            template = jinja2.Template(template_content)
            
        return web.Response(
            text=template.render(
                token=token,
                error="âŒ Wrong Password!",
                title=link_data.get("title", "Protected Link"),
                channel_link=link_data.get("channel_link")
            ),
            content_type="text/html"
        )
        
@routes.get(r"/watch/{path:\S+}", allow_head=True)
async def watch_handler(request: web.Request): # Renamed to avoid name conflict
    try:
        path = request.match_info["path"]
        match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
        if match:
            secure_hash = match.group(1)
            id = int(match.group(2))
        else:
            id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
            secure_hash = request.rel_url.query.get("hash")
        return web.Response(
            text=await render_page(id, secure_hash), content_type="text/html"
        )
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FileNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        # FIX: Return a response instead of passing
        return web.Response(status=400, text="Connection Error")
    except Exception as e:
        logging.critical(e.with_traceback(None))
        raise web.HTTPInternalServerError(text=str(e))


@routes.get(r"/{path:\S+}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
        if match:
            secure_hash = match.group(1)
            id = int(match.group(2))
        else:
            id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
            secure_hash = request.rel_url.query.get("hash")
        return await media_streamer(request, id, secure_hash)
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FileNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        # FIX: Return a response instead of passing
        return web.Response(status=400, text="Connection Error")
    except Exception as e:
        logging.critical(e.with_traceback(None))
        raise web.HTTPInternalServerError(text=str(e))
        
class_cache = {}


async def media_streamer(request: web.Request, id: int, secure_hash: str):
    range_header = request.headers.get("Range")

    index = min(work_loads, key=work_loads.get)
    faster_client = multi_clients[index]

    if len(multi_clients) > 1:
        logging.info(f"Client {index} is now serving {request.remote}")

    if faster_client in class_cache:
        tg_connect = class_cache[faster_client]
        logging.debug(f"Using cached ByteStreamer object for client {index}")
    else:
        logging.debug(f"Creating new ByteStreamer object for client {index}")
        tg_connect = ByteStreamer(faster_client)
        class_cache[faster_client] = tg_connect
    logging.debug("before calling get_file_properties")
    file_id = await tg_connect.get_file_properties(id)
    logging.debug("after calling get_file_properties")

    if file_id.unique_id[:6] != secure_hash:
        logging.debug(f"Invalid hash for message with ID {id}")
        raise InvalidHash

    file_size = file_id.file_size

    # Parse HTTP Range safely. This supports normal and suffix ranges
    # without crashing on malformed Range headers.
    if range_header:
        try:
            http_range = request.http_range
            start = http_range.start
            stop = http_range.stop

            if start is None:
                start = 0

            # bytes=-N means the last N bytes.
            if start < 0:
                from_bytes = max(file_size + start, 0)
            else:
                from_bytes = start

            until_bytes = (stop if stop is not None else file_size) - 1
        except (ValueError, IndexError, TypeError):
            return web.Response(
                status=416,
                text="416: Range not satisfiable",
                headers={"Content-Range": f"bytes */{file_size}"},
            )
    else:
        from_bytes = 0
        until_bytes = file_size - 1

    if file_size <= 0 or from_bytes >= file_size or until_bytes < from_bytes:
        return web.Response(
            status=416,
            text="416: Range not satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"},
        )

    until_bytes = min(until_bytes, file_size - 1)

    chunk_size = 1024 * 1024
    until_bytes = min(until_bytes, file_size - 1)

    offset = from_bytes - (from_bytes % chunk_size)
    first_part_cut = from_bytes - offset
    last_part_cut = until_bytes % chunk_size + 1

    req_length = until_bytes - from_bytes + 1
    part_count = math.ceil((until_bytes + 1) / chunk_size) - math.floor(offset / chunk_size)
    body = tg_connect.yield_file(
        file_id, index, offset, first_part_cut, last_part_cut, part_count, chunk_size
    )

    mime_type = file_id.mime_type
    file_name = file_id.file_name
    disposition = "attachment"

    if mime_type:
        if not file_name:
            try:
                file_name = f"{secrets.token_hex(2)}.{mime_type.split('/')[1]}"
            except (IndexError, AttributeError):
                file_name = f"{secrets.token_hex(2)}.unknown"
    else:
        if file_name:
            mime_type = mimetypes.guess_type(file_id.file_name)[0]
            if not mime_type:
                mime_type = "application/octet-stream"
        else:
            mime_type = "application/octet-stream"
            file_name = f"{secrets.token_hex(2)}.unknown"

    response = web.StreamResponse(
        status=206 if range_header else 200,
        headers={
            "Content-Type": mime_type,
            **({"Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}"} if range_header else {}),
            "Content-Length": str(req_length),
            "Content-Disposition": f'{disposition}; filename="{file_name}"',
            "Accept-Ranges": "bytes",
        },
    )

    await response.prepare(request)

    # HEAD requests return headers without downloading the Telegram file.
    if request.method == "HEAD":
        await response.write_eof()
        return response

    try:
        async for chunk in body:
            if chunk:
                await response.write(chunk)
    except (ConnectionResetError, asyncio.CancelledError):
        logging.info("Client disconnected while streaming file %s", id)
    except Exception:
        logging.exception("Streaming failed for file %s", id)
    finally:
        try:
            await response.write_eof()
        except (ConnectionResetError, RuntimeError):
            pass

    return response
