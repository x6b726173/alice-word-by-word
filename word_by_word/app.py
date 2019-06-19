from aiohttp import web
import aiohttp_cors
from aioalice import get_new_configured_app
from settings import *
from core import dp
# регистрация методов диалога
import dialog.v1


if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)

    # фактически отключаем cors защиту
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    for route in list(app.router.routes()):
        cors.add(route)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
