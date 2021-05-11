import os
import sys
import random

from importlib import import_module

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from loader import loader_apps
from settings import TOKEN, APPS
from utils import logger


def features_discovery():
    """
        Loading features defined in settings.py with the pattern
        defined to be used, integrating dinamically helpers and loaders
    """
    for app in APPS:
        feature_module = f'features.{app}'
        try:
            import_module(feature_module)
        except Exception as e:
            logger.error(f"Error to load feature: {app}:{e}")


def start(update, context):
    """
        Basic handler commands
        function to handle the /start command
    """
    update.message.reply_text('start command received')


def error(update, context):
    """
        function to handle errors occured in the dispatcher
    """
    logger.error(context.error)
    update.message.reply_text('Fui pegar um back, talvez ja ja eu volte!')


def text(update, context):
    """
        function to handle normal text
    """
    text_received = update.message.text
    STICKERS = [
        "CAACAgEAAxkBAAECStJgmoWxfRZbQlNGWpeE3NaqEWYf8QACNwQAAnTnKwIlivXJuy2BSh8E",
        "CAACAgIAAxkBAAECStRgmoYCD8Gu47QRekNoDt5GxKDsLwACawEAAlrjihfqNIInyEgvQR8E",
        "CAACAgIAAxkBAAECStZgmoYiuofAXBpCkvA-_45wH8Vc-AACWAEAAlrjihdmuBpbgPVJqB8E",
        "CAACAgEAAxkBAAECSthgmoY7PmF5uSsaeUvY8ZlPHmYieAACTQIAAnTnKwLmJx6dp10G6B8E",
        "CAACAgEAAxkBAAECStpgmoZc2O9WCrIBuTuXHGymu_f_gAACfAADv4XHBbjt-hzAn-V2HwQ"
    ]
    if update.message.from_user.username == 'vcali' or update.message.from_user.username == 'rondineli':
        chat = update.message.chat
        context.bot.send_sticker(chat.id, random.choice(STICKERS))
        update.message.reply_text(f'🖕 vai procurar o q fazer {update.message.from_user.username}!')
        return
    update.message.reply_text(f'did you say "{text_received}" ?')


def main():
    """
        create the updater, that will automatically create
        also a dispatcher and a queue to make them dialoge
    """
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    features_discovery()
    loader_apps.setup(dispatcher)

    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(CommandHandler("help", help))
    # dispatcher.add_handler(CommandHandler("meet", meet))

    # add an handler for normal text (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text, text))

    # add an handler for errors
    dispatcher.add_error_handler(error)

    # start your shiny new bot
    updater.start_polling()

    # run the bot until Ctrl-C
    updater.idle()


if __name__ == '__main__':

    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    logger.info(f"Injecting project path: {BASE_PATH}")
    # Inserting project path o pythonpath
    sys.path.insert(0, BASE_PATH)

    main()
