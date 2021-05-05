from utils import logger

from typing import Callable, List, Optional

from telegram.ext import Handler


class Loader:
    _APPS = []

    @classmethod
    def clean(cls):
        cls._APPS = []

    @classmethod
    def apps(cls):
        _apps = []
        for app in cls._APPS:
            _apps.append(app.handler)
        return _apps

    @classmethod
    def handler(cls, app):
        app = App(handler=app)
        cls._APPS.append(app)

    @classmethod
    def setup(cls, dispatcher):
        for route in cls._APPS:
            route.instance = route.handler()
            dispatcher.add_handler(route.instance)


# Set all methods back in here
loader_apps = Loader
