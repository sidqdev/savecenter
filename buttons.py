from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_buttons():
    button = InlineKeyboardMarkup()
    help_me = InlineKeyboardButton(text='Мне нужна помощь', callback_data='help_me')
    i_w_help = InlineKeyboardButton(text='Я могу помочь', callback_data='i_w_help')
    button.add(help_me, i_w_help)

    return button
