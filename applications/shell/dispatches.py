from telegram.ext import CommandHandler, RegexHandler, CallbackQueryHandler
from .commands import *
from .shell import Shell

sh = Shell()

dispatches = [
    RegexHandler(SHELL, sh.shell_menu),
    RegexHandler(SHOW_FILES, sh.shell_ls),
    RegexHandler(CURRENT_DIR, sh.shell_pwd),
    RegexHandler(CD_REGEX, sh.shell_cd),
    RegexHandler(COMMAND_REGEX, sh.shell_run),
    RegexHandler(GET_FILE_REGEX, sh.get_file),
]