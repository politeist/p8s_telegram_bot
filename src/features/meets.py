import os

from telegram.ext import CallbackContext, CommandHandler
from telegram.update import Update

from loader import loader_apps


def cmd_meet(update: Update, contex: CallbackContext):
    meeting_room = os.getenv('GMEET')
    update.message.reply_text(meeting_room)


@loader_apps.handler
def meet():
    """
        /meet - Return our simple gmeet link
    """
    return CommandHandler("meet", cmd_meet)
