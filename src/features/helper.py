from telegram.ext import CallbackContext, CommandHandler
from telegram.update import Update

from loader import LoaderApps

EXCLUDED_HANDLERS = ["quiz_response"]

def cmd_help(update: Update, contex: CallbackContext):
    helper = ['Available commands:']
    for app in LoaderApps.apps():
        if app.__name__ not in EXCLUDED_HANDLERS:
            if not app.__doc__:
                helper.append(f'/{app.__name__}')
            else:
                helper.append(app.__doc__.strip())
    update.message.reply_text('\n'.join(helper))


@LoaderApps.handler
def help():
    """
        /help - Return all handlers available
    """
    return CommandHandler("help", cmd_help)
