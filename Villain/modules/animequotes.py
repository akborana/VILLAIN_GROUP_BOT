# Made By @AKBORANA1 On Telegram & Github Id Akborana
import random

from telegram import Update
from telegram.ext import CallbackContext, run_async

import Villain.modules.animequotesstring as animequotesstring
from Villain import dispatcher
from Villain.modules.disable import DisableAbleCommandHandler


@run_async
def animequotes(update: Update, context: CallbackContext):
    update.effective_message.reply_text(random.choice(animequotesstring.ANIMEQUOTES))


ANIMEQUOTES_HANDLER = DisableAbleCommandHandler("animequotes", animequotes)

dispatcher.add_handler(ANIMEQUOTES_HANDLER)
#Modify by big bull