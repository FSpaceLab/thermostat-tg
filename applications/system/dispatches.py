from telegram.ext import CommandHandler, RegexHandler, CallbackQueryHandler
from .commands import *
from .home import Home
from manager.bot.security import Security

security = Security()
home = Home()

dispatches = [
    CallbackQueryHandler(security.check_code, pattern="(sec_.)")
]