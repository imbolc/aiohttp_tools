from functools import partial

try:
    from aiohttp_session import get_session
except ImportError:
    pass

from . import url_for


async def url_for_processor(request):
    return {"url_for": partial(url_for, request)}


async def session_processor(request):
    session = await get_session(request)
    return {"session": session}
