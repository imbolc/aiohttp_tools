from aiohttp_jinja2 import render_template


def template_handler(template, context=None):
    async def handler(request):
        return render_template(template, request, context or {})

    return handler
