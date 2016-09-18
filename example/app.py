#!/usr/bin/env python
import sys
from datetime import datetime
sys.path.append('../')  # noqa

from aiohttp import web
import jinja2
import aiohttp_jinja2
import aiohttp_session

from aiohttp_tools import jsonify, redirect, get_client_ip, get_argument
from aiohttp_tools import flash
from aiohttp_tools.static_url import static_url
import aiohttp_tools.middlewares
import aiohttp_tools.context_processors


@aiohttp_jinja2.template('index.html')
async def index(request):
    if request.method == 'POST':
        data = await request.post()
        message = get_argument(data, 'message')
        flash.info(request, message)
        return redirect(request, 'index')
    return {}


@jsonify
async def api(request):
    method = request.match_info['method']
    if method == 'now':
        return {'now': datetime.now()}
    elif method == 'ip':
        return {'ip': get_client_ip(request)}
    return {'error': 'unknown api method'}


app = web.Application(middlewares=[
    aiohttp_tools.middlewares.fix_host('0.0.0.0:8000'),
    aiohttp_tools.middlewares.add_trailing_slash,
])
aiohttp_session.setup(app, aiohttp_session.SimpleCookieStorage())
app.middlewares.append(aiohttp_tools.flash.middleware)

env = aiohttp_jinja2.setup(
    app,
    loader=jinja2.FileSystemLoader('./'),
    context_processors=[
        aiohttp_tools.context_processors.url_for_processor,
        aiohttp_tools.flash.context_processor,
    ],
)
env.globals['static_url'] = static_url


app.router.add_get('/', index, name='index')
app.router.add_post('/', index)
app.router.add_get('/api/{method}', api, name='api')
app.router.add_static('/', './')


if __name__ == '__main__':
    web.run_app(app, port=8000)
