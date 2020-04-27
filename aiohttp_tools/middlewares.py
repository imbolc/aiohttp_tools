import logging
from aiohttp import web


log = logging.getLogger(__name__)


async def add_trailing_slash(app, handler):
    async def middleware(request):
        try:
            response = await handler(request)
        except web.HTTPNotFound as e:
            if not request.path.endswith("/"):
                raise web.HTTPFound(request.path + "/")
            raise e
        return response

    return middleware


def fix_host(true_host):
    async def fabric(app, handler):
        async def middleware(request):
            if request.host != true_host:
                requested_url = "{}://{}{}".format(
                    request.scheme, request.host, request.path_qs
                )
                redirect_url = "{}://{}{}".format(
                    request.scheme, true_host, request.path_qs
                )
                log.warning(
                    "Redirect wrong host: %s => %s",
                    requested_url,
                    redirect_url,
                )
                return web.HTTPPermanentRedirect(redirect_url)
            return await handler(request)

        return middleware

    return fabric
