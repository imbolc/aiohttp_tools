"""
Usage:

    from aiohttp_tools.flash import flash

    app.middlewares.append(aiohttp_tools.flash.middleware)
    context_processors.append(aiohttp_tools.flash.context_processor)

    async def handler(request):
        flash(request, ('error', 'Some error'))


    {% for message, level in get_flashed_messages() %}
    <div class="flash {{ level }}">
        {{ message }}
    </div>
    {% endfor %}
"""
from functools import partial

from aiohttp import web

from aiohttp_session import get_session


def message(request, message, level="info"):
    request.setdefault("flash_outgoing", []).append((message, level))


debug = partial(message, level="debug")
info = partial(message, level="info")
success = partial(message, level="success")
warning = partial(message, level="warning")
error = partial(message, level="error")


async def context_processor(request):
    return {"get_flashed_messages": lambda: request.pop("flash_incoming", [])}


@web.middleware
async def middleware(request, handler):
    session = await get_session(request)
    request["flash_incoming"] = session.pop("flash", [])
    response = await handler(request)
    session["flash"] = request.get("flash_incoming", []) + request.get(
        "flash_outgoing", []
    )
    return response
