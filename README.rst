aiohttp_tools
=============

A set of little tools for aiohttp-based sites.

It contains:

- `url_for` - flask-like url reverser
- `jsonify` - flask-like json-dumper with support of datetime, and ObjectId
- `redirect` - django-like redirect
- `get_argument` - tornado-like util to get GET / POST arguments
- `static_url` - tornado-like url-wrapper to add version hast to static asset
- `flash` - simple flash messages, usage described bellow
- `get_client_ip` - client IP address
- `add_trailing_slash` - middleware for adding trailing slash to unknown url
- `fix_host` - middleware for redirect requests by IP to right domain
- `template_handler` - handler that just render template
- `url_for_processor` - context processor for using `url_for` without passing request
- `session_processor` - context_processor for `aiohttp_session`


Look at the `example` folder for working example.


Installation
------------
::
    pip install aiohttp_tools

Repository: https://github.com/imbolc/aiohttp_tools


Flash messages
--------------
.. code-block:: python

    from aiohttp_tools.flash import flash

    # you should include session middleware before flash middleware
    aiohttp_session.setup(app, ...)
    app.middlewares.append(aiohttp_tools.flash.middleware)
    context_processors.append(aiohttp_tools.flash.context_processor)

    async def handler(request):
        flash.message(request, 'Message', 'level')
        # shortcuts
        flash.info(request, 'Some message')
        flash.success(...)
        flash.warning(...)
        flash.error(...)


.. code-block:: html
    {% for message, level in get_flashed_messages() %}
        <div class="flash {{ level }}">
            {{ message }}
        </div>
    {% endfor %}
