import asjson
from aiohttp import web

DEFAULT = object()


def url_for(
    request, urlname, *, _external=False, _scheme=None, _query=None, **parts
):
    url = request.app.router[urlname].url_for(
        **{k: str(v) for k, v in parts.items()}
    )
    if _query:
        url = url.with_query(_query)
    if _external:
        url = "{}://{}{}".format(_scheme or request.scheme, request.host, url)
    return str(url)


def redirect(request, urlname, *, permanent=False, **kwargs):
    if urlname.startswith(("/", "http://", "https://")):
        url = urlname
    else:
        url = url_for(request, urlname, **kwargs)
    res_cls = web.HTTPMovedPermanently if permanent else web.HTTPFound
    return res_cls(url)


def get_client_ip(request):
    try:
        ips = request.headers["X-Forwarded-For"]
    except KeyError:
        ips = request.transport.get_extra_info("peername")[0]
    return ips.split(",")[0]


def get_argument(container, name, default=DEFAULT, *, cls=None):
    arg = container.get(name, default)
    if name not in container:
        if default is not DEFAULT:
            return default
        raise web.HTTPBadRequest(
            reason="Missing required argument: {}".format(name)
        )
    if cls:
        try:
            arg = cls(arg)
        except Exception:
            raise web.HTTPBadRequest(
                reason="Argument is incorrect: {}".format(name)
            )
    return arg


def jsonify(handler_or_data, *args, **kwargs):
    f = jsonify_decortor if callable(handler_or_data) else jsonify_function
    return f(handler_or_data, *args, **kwargs)


def jsonify_function(data, debug=False, **kwargs):
    text = asjson.dumps(data, debug=debug)
    kwargs["content_type"] = kwargs.get("content_type", "application/json")
    return web.Response(text=text, **kwargs)


def jsonify_decortor(handler, *args, **kwargs):
    async def wrapper(request):
        response = await handler(request)
        if isinstance(response, web.StreamResponse):
            return response
        return jsonify_function(response, *args, **kwargs)

    return wrapper
