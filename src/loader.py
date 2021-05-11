''' Class Loader '''
from dataclasses import dataclass
from typing import Callable, List, Optional

from telegram.ext import Handler

from utils import logger



@dataclass
class App:
    handler: Callable
    instance: Optional[Handler] = None


class Loader:
    _APPS: List[App] = []

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
LoaderApps = Loader
