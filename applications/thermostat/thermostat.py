import time
import telegram
from manager.bot.security import protect_it
from manager.db_manager.manager import update_current_menu, get_current_menu
from .thermostat_manager import ThermostatBox
from .commands import *
from .settings import *


class Thermostat:
    def __init__(self):
        self.custom_keyboard = [
            [GET_DATA_FROM_TS],
            [ENABLE_TS, DISABLE_TS],
            [SET_T_MENU, SET_LIGHT_MENU],
        ]

        self.set_data_menu = [
            [TS_MENU],
        ]

        self.set_light_data_menu = [
            [ON_UV, ON_RGB, ON_RGB_UV],
            [OFF_LIGHT, GET_LIGHT_DATA],
            [SET_LIGHT_UV_MENU, SET_LIGHT_R_MENU],
            [SET_LIGHT_G_MENU, SET_LIGHT_B_MENU],
            [TS_MENU],
        ]

        self.set_intensity_menu = [
            [SET_LIGHT_MENU],
        ]

    @staticmethod
    def __get_data_from_box():
        ts = ThermostatBox()
        time.sleep(TIME_SLEEP)
        text = ts.get_data_from_box()
        return text

    @staticmethod
    def __send_data_to_box(data):
        ts = ThermostatBox()
        ts.send_data_to_box(data)
        del ts

    @staticmethod
    def __data_for_box(data_from_box):
        return [data_from_box[TS_STATE], data_from_box[SET_TEMP], data_from_box[CO2_STATE],
                data_from_box[CO2_SETTED], data_from_box[LIGHT_STATE], data_from_box[UV],
                data_from_box[R], data_from_box[G], data_from_box[B]]

    @staticmethod
    def __get_light_mode(text):
        if text[LIGHT_STATE] == '1':
            return '<b>УФ</b>'
        elif text[LIGHT_STATE] == '2':
            return '<b>RGB</b>'
        elif text[LIGHT_STATE] == '3':
            return '<b>RGB & UV</b>'
        return '<b>Вимкнено</b>'

    @protect_it
    def ts_menu(self, bot, update):
        update_current_menu(update.message.chat_id, menu=TS_MENU)
        reply_markup = telegram.ReplyKeyboardMarkup(self.custom_keyboard)
        bot.send_message(chat_id=update.message.chat_id,
                         text="Телеграм бот для керування Термостат-боксом",
                         reply_markup=reply_markup)

    @protect_it
    def get_data(self, bot, update):
        text = self.__get_data_from_box()
        light_mode = self.__get_light_mode()
        formatting_text = f"Термостат: {'On' if int(text[TS_STATE]) else 'Off'}\n" \
            f"Стан в даний момент: {('<b>Нагрівання</b>' if text[CURRENT_STATE] == '1' else '<b>Охолодження</b>') if text[CURRENT_STATE] != '0' else '<b>Вимкнено</b>'}\n" \
            f"Температура: {text[CURRENT_TEMP]}\n" \
            f"Встановлена температура.: {text[SET_TEMP]}\n" \
            f"Освітленість: {light_mode}"

        bot.send_message(chat_id=update.message.chat_id,
                         text=formatting_text, parse_mode="HTML")

    @protect_it
    def on_ts(self, bot, update):
        data_from_box = self.__get_data_from_box()
        data_from_box[TS_STATE] = "1"
        text_for_box = f"{SEND_DATA}\n" + ";".join(self.__data_for_box(data_from_box))

        self.__send_data_to_box(text_for_box)

        bot.send_message(chat_id=update.message.chat_id,
                         text="Терморегуляцію ввімкнено",
                         parse_mode="HTML")

    @protect_it
    def off_ts(self, bot, update):
        data_from_box = self.__get_data_from_box()
        data_from_box[TS_STATE] = "0"
        text_for_box = f"{SEND_DATA}\n" + ";".join(self.__data_for_box(data_from_box))

        self.__send_data_to_box(text_for_box)

        bot.send_message(chat_id=update.message.chat_id,
                         text="Терморегуляцію вимкнено",
                         parse_mode="HTML")

    @protect_it
    def set_t(self, bot, update):
        text = self.__get_data_from_box()

        update_current_menu(update.message.chat_id, menu=SET_T_MENU)

        reply_markup = telegram.ReplyKeyboardMarkup(self.set_data_menu)
        bot.send_message(chat_id=update.message.chat_id,
                         text=f"UV: Вкажіть потрібну температуру\n"
                         f"Встановлено: <b>{text[SET_TEMP]}</b>, можливе значення: <i>0-60</i>",
                         reply_markup=reply_markup,
                         parse_mode="HTML")

    @protect_it
    def set_light_menu(self, bot, update):
        update_current_menu(update.message.chat_id, menu=SET_LIGHT_MENU)
        reply_markup = telegram.ReplyKeyboardMarkup(self.set_light_data_menu)
        bot.send_message(chat_id=update.message.chat_id,
                         text="Управління освітленістю",
                         reply_markup=reply_markup)


    @protect_it
    def on_uv(self, bot, update):
        data_from_box = self.__get_data_from_box()
        data_from_box[LIGHT_STATE] = "1"
        text_for_box = f"{SEND_DATA}\n" + ";".join(self.__data_for_box(data_from_box))
        
        self.__send_data_to_box(text_for_box)

        bot.send_message(chat_id=update.message.chat_id,
                         text="Увімкнено УФ-освітлення",
                         parse_mode="HTML")

    @protect_it
    def on_rgb(self, bot, update):
        data_from_box = self.__get_data_from_box()
        data_from_box[LIGHT_STATE] = "2"
        text_for_box = f"{SEND_DATA}\n" + ";".join(self.__data_for_box(data_from_box))
        
        self.__send_data_to_box(text_for_box)
        bot.send_message(chat_id=update.message.chat_id,
                         text="Увімкнено RGB-освітлення",
                         parse_mode="HTML")

    @protect_it
    def on_rgb_uv(self, bot, update):
        data_from_box = self.__get_data_from_box()
        data_from_box[LIGHT_STATE] = "3"
        text_for_box = f"{SEND_DATA}\n" + ";".join(self.__data_for_box(data_from_box))

        self.__send_data_to_box(text_for_box)
        bot.send_message(chat_id=update.message.chat_id,
                         text="Увімкнено RGB & UV-освітлення",
                         parse_mode="HTML")

    @protect_it
    def off_light(self, bot, update):
        data_from_box = self.__get_data_from_box()
        data_from_box[LIGHT_STATE] = "0"

        text_for_box = f"{SEND_DATA}\n" + ";".join(self.__data_for_box(data_from_box))
        
        self.__send_data_to_box(text_for_box)
        bot.send_message(chat_id=update.message.chat_id,
                         text="Освітлення вимкнено",
                         parse_mode="HTML")

    @protect_it
    def get_light_data(self, bot, update):
        text = self.__get_data_from_box()
        light_data = self.__get_light_data(text)
        formatted_text = f"Стан освітленості: {light_data}" \
                         f"\n<b>UV:</b> {text[UV]}\n<b>R:</b> {text[R]}\n" \
                         f"<b>G:</b> {text[G]}\n<b>B:</b> {text[B]}"

        bot.send_message(chat_id=update.message.chat_id,
                         text=formatted_text,
                         parse_mode="HTML")

    @protect_it
    def set_uv_intensity(self, bot, update):
        text = self.__get_data_from_box()

        update_current_menu(update.message.chat_id, menu=SET_LIGHT_UV_MENU)

        reply_markup = telegram.ReplyKeyboardMarkup(self.set_intensity_menu)
        bot.send_message(chat_id=update.message.chat_id,
                         text=f"UV: Вкажіть інтенсивність УФ-освітлення\n"
                              f"Встановлено: <b>{text[UV]}</b>, можливе значення: <i>0-255</i>",
                         reply_markup=reply_markup,
                         parse_mode="HTML")

    @protect_it
    def set_r_intensity(self, bot, update):
        text = self.__get_data_from_box()

        update_current_menu(update.message.chat_id, menu=SET_LIGHT_R_MENU)

        reply_markup = telegram.ReplyKeyboardMarkup(self.set_intensity_menu)
        bot.send_message(chat_id=update.message.chat_id,
                         text=f"RGB: Вкажіть інтенсивність червоного світла \n"
                              f"Встановлено: <b>{text[R]}</b>, можливе значення: <i>0-255</i>",
                         reply_markup=reply_markup,
                         parse_mode="HTML")

    @protect_it
    def set_g_intensity(self, bot, update):
        text = self.__get_data_from_box()

        update_current_menu(update.message.chat_id, menu=SET_LIGHT_G_MENU)

        reply_markup = telegram.ReplyKeyboardMarkup(self.set_intensity_menu)
        bot.send_message(chat_id=update.message.chat_id,
                         text=f"RGB: Вкажіть інтенсивність зеленого світла\n"
                              f"Встановлено: <b>{text[G]}</b>, можливе значення: <i>0-255</i>",
                         reply_markup=reply_markup,
                         parse_mode="HTML")

    @protect_it
    def set_b_intensity(self, bot, update):
        text = self.__get_data_from_box()

        update_current_menu(update.message.chat_id, menu=SET_LIGHT_B_MENU)

        reply_markup = telegram.ReplyKeyboardMarkup(self.set_intensity_menu)
        bot.send_message(chat_id=update.message.chat_id,
                         text=f"RGB: Вкажіть інтенсивність синього світла\n"
                              f"Встановлено: <b>{text[B]}</b>, можливе значення: <i>0-255</i>",
                         reply_markup=reply_markup,
                         parse_mode="HTML")

    @protect_it
    def send_data_to_box(self, bot, update):
        data_from_box = self.__get_data_from_box()

        message = update.message.text
        current_menu = get_current_menu(update.message.chat_id)

        if current_menu == SET_LIGHT_UV_MENU:
            data_from_box[UV] = message

        elif current_menu == SET_LIGHT_R_MENU:
            data_from_box[R] = message

        elif current_menu == SET_LIGHT_G_MENU:
            data_from_box[G] = message

        elif current_menu == SET_LIGHT_B_MENU:
            data_from_box[B] = message

        elif current_menu == SET_T_MENU:
            data_from_box[SET_TEMP] = message

        text_for_box = f"{SEND_DATA}\n" + ";".join(self.__data_for_box(data_from_box))
        self.__send_data_to_box(text_for_box)

        if current_menu != SET_T_MENU:
            formatted_text = f"Інтенсивність вказаного параметра освітлення змінено на <i>{message}</i>" + \
                             f"\n<b>UV:</b> {data_from_box[UV]}\n<b>R:</b> {data_from_box[R]}\n" + \
                             f"<b>G:</b> {data_from_box[G]}\n<b>B:</b> {data_from_box[B]}"

            bot.send_message(chat_id=update.message.chat_id,
                             text=formatted_text,
                             parse_mode="HTML")

            self.set_light_menu(bot, update)
        else:
            formatted_text = f"Встановлено температуру в термостаті {message}°C"

            bot.send_message(chat_id=update.message.chat_id,
                             text=formatted_text,
                             parse_mode="HTML")

            self.ts_menu(bot, update)
