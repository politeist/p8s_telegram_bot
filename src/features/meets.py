import os

from telegram.ext import CallbackContext, CommandHandler
from telegram.update import Update

from loader import LoaderApps


def cmd_meet(update: Update, contex: CallbackContext):
    meeting_room = os.getenv('GMEET')
    update.message.reply_text(meeting_room)


@LoaderApps.handler
def meet():
    """
        /meet - Return our simple gmeet link
    """
    return CommandHandler("meet", cmd_meet)
