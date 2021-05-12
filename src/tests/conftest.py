import os
import sys

import pytest

from telegram.ext import CallbackContext, Dispatcher, DictPersistence
from telegram import Bot, Message, Update, User, Chat

from .settings_tests import API_TOKEN


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
print(f"Injecting project path: {BASE_PATH}/../")
# Inserting project path o pythonpath
sys.path.insert(0, f"{BASE_PATH}/../")


@pytest.fixture
def context(bot, update, dispatcher_mock):
    return CallbackContext.from_update(update, dispatcher_mock)


@pytest.fixture
def dispatcher_mock(bot):
    return Dispatcher(
        bot,
        None,
        workers=0,
        use_context=True
    )


@pytest.fixture
def message(user):
    return Message(
        message_id=1,
        from_user=user,
        date=None,
        chat=None
    )


@pytest.fixture
def user():
    return User(
        id=1,
        is_bot=False,
        first_name="Cool",
        last_name="Bot",
        username="collBot"
    )


@pytest.fixture(scope="session")
def bot():
    return Bot(token=API_TOKEN)


@pytest.fixture
def update(message):
    return Update(
        update_id=1,
        message=message)


@pytest.fixture
def context(bot, update, dispatcher_mock):
    return CallbackContext.from_update(update, dispatcher_mock)


@pytest.fixture
def chat_message(user):
    chat = Chat(
        123456789,
        "P8s",
        "group"
    )
    return Message(
        message_id=1,
        from_user=user,
        date=None,
        chat=chat,
        chat_id=chat.id
    )


@pytest.fixture
def chat_update(chat_message):
    return Update(
        update_id=2,
        _effective_chat=chat_message,
        message=chat_message
    )


@pytest.fixture
def context(bot, update, dispatcher_mock):
    return CallbackContext.from_update(update, dispatcher_mock)


@pytest.fixture
def chat_context(bot, chat_update, dispatcher_mock):
    return CallbackContext.from_update(chat_update, dispatcher_mock)