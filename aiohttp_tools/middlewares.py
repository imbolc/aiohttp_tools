import logging

from aiohttp import web

log = logging.getLogger(__name__)


def fix_host(true_host: str):
    @web.middleware
    async def fix_host_middleware(request, handler):
        if request.host != true_host:
            requested_url = "{}://{}{}".format(
                request.scheme, request.host, request.path_qs
            )
            redirect_url = "{}://{}{}".format(
                request.scheme, true_host, request.path_qs
            )
            log.warning(
                "Unknown domain redirection: %s => %s",
                requested_url,
                redirect_url,
            )
            raise web.HTTPPermanentRedirect(redirect_url)
        return await handler(request)

    return fix_host_middleware
