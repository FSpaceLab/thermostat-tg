import telegram
from manager.bot.security import protect_it
from . import commands
from .shell_manager import ShellManager
from .answers import *

class Shell:

    def __init__(self):
        self.shell = ShellManager()
        self.custom_keyboard = [
            [commands.CURRENT_DIR, commands.SHOW_FILES],
            ["Thermostat menu"]
        ]

    @protect_it
    def shell_menu(self, bot, update):
        reply_markup = telegram.ReplyKeyboardMarkup(self.custom_keyboard)
        bot.send_message(chat_id=update.message.chat_id,
                         text="SHELL mode",
                         reply_markup=reply_markup)

    @protect_it
    def shell_ls(self, bot, update):
        text = self.shell.show_files(user_id=update.message.chat_id)
        bot.send_message(chat_id=update.message.chat_id,
                         text=text)

    @protect_it
    def shell_pwd(self, bot, update):
        text = self.shell.show_current_dir(user_id=update.message.chat_id)
        bot.send_message(chat_id=update.message.chat_id,
                         text=text)

    @protect_it
    def shell_cd(self, bot, update):
        self.shell.change_dir(user_id=update.message.chat_id, cmd=update.message.text)
        text = f"Dir changed: {self.shell.pwd(user_id=update.message.chat_id)}"
        bot.send_message(chat_id=update.message.chat_id,
                         text=text)

    @protect_it
    def shell_run(self, bot, update):
        text = self.shell.command(user_id=update.message.chat_id, cmd=update.message.text)
        bot.send_message(chat_id=update.message.chat_id,
                         text=text)

    @protect_it
    def get_file(self, bot, update):
        path_to_file = self.shell.path_to_file(user_id=update.message.chat_id, name_file=update.message.text)
        if path_to_file != IS_NOT_A_FILE:
            bot.send_document(chat_id=update.message.chat_id, document=open(path_to_file, 'rb'))
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text=f"<b>{IS_NOT_A_FILE}</b>", parse_mode='HTML')


