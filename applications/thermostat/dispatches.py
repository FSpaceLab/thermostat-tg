from telegram.ext import CommandHandler, RegexHandler, CallbackQueryHandler
from .commands import *
from .thermostat import Thermostat

ts = Thermostat()

dispatches = [
    CommandHandler(START_COMMAND, ts.ts_menu),

    RegexHandler(TS_MENU, ts.ts_menu),

    RegexHandler(GET_DATA_FROM_TS, ts.get_data),
    RegexHandler(ENABLE_TS, ts.on_ts),
    RegexHandler(DISABLE_TS, ts.off_ts),
    RegexHandler(SET_T_MENU, ts.set_t),

    RegexHandler(SET_LIGHT_MENU, ts.set_light_menu),
    RegexHandler(ON_UV, ts.on_uv),
    RegexHandler(ON_RGB, ts.on_rgb),
    RegexHandler(GET_LIGHT_DATA, ts.get_light_data),
    RegexHandler(OFF_LIGHT, ts.off_light),
    RegexHandler(SET_LIGHT_UV_MENU, ts.set_uv_intensity),
    RegexHandler(SET_LIGHT_R_MENU, ts.set_r_intensity),
    RegexHandler(SET_LIGHT_G_MENU, ts.set_g_intensity),
    RegexHandler(SET_LIGHT_B_MENU, ts.set_b_intensity),

    RegexHandler("^[\d]+$", ts.send_data_to_box)
]
