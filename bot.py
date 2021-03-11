from loader import bot, dp
from aiogram import executor
from aiogram.types import CallbackQuery, Message
from aiogram import Dispatcher
from aiogram.types import ContentType

import buttons

text1 = 'Похоже что твой собеседник остановил бота🙊'
text2 = '''Спасибо, надеюсь уже все хорошо🥺
Что-бы воспользоваться ботом еще раз, напиши🥰 /start'''
text3 = '''Мы нашли вам собеседника🥰
Что бы остановить диалог /stop'''
text4 = '''Извини, что то пошло не так...
Попробуй найти новго собеседника /start'''
text5 = 'Выбери что ты хочешь сделать🥰'
text6 = 'Ожидайте🙈...'


@dp.message_handler(commands=['start'], state='*')
async def start_handler(message: Message):
    state = dp.current_state()
    await state.set_state('IW')
    await state.set_data({'link': 0})

    await bot.send_message(message.chat.id, text=text5, reply_markup=buttons.main_buttons())


@dp.message_handler(commands=['stop'], state='*')
async def stop_handler(message: Message):
    state = dp.current_state()
    global_state = dp.current_state(chat=0, user=0)
    gdata = await global_state.get_data()

    uid = await state.get_data()
    uid = uid['link']

    if uid:
        ustate = dp.current_state(chat=uid, user=uid)
        data = await ustate.get_data()
        data['link'] = 0
        await ustate.set_data(data)
        await ustate.set_state('NONE')
        await bot.send_message(uid, text1)
        await bot.send_message(uid, text2)

    await state.set_data({'link': 0})
    await state.set_state('NONE')
    await bot.send_message(message.chat.id, text2)


@dp.callback_query_handler(state='IW')
async def iw_handler(callback: CallbackQuery):
    state = dp.current_state()
    sdate = await state.get_data()

    data = callback.data

    global_state = dp.current_state(chat=0, user=0)
    gdata = await global_state.get_data()

    if data == 'help_me':
        if callback.message.chat.id in gdata['helpers']:
            gdata['helpers'].remove(callback.message.chat.id)
        if len(gdata['helpers']):
            sdate['link'] = gdata['helpers'][-1]
            gdata['helpers'].pop(-1)
            try:
                await bot.send_message(sdate['link'], text=text3)
                await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                            text=text3, reply_markup=None)
                await state.set_state('CHAT')
                await dp.current_state(chat=sdate['link'], user=sdate['link']).set_state('CHAT')
                await dp.current_state(chat=sdate['link'], user=sdate['link']).set_data(
                    {'link': callback.message.chat.id})
            except:
                sdate['link'] = 0

        else:
            if callback.message.chat.id not in gdata['needers']:
                gdata['needers'].append(callback.message.chat.id)
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        text=text6, reply_markup=None)
    else:
        if callback.message.chat.id in gdata['needers']:
            gdata['needers'].remove(callback.message.chat.id)

        if len(gdata['needers']):
            sdate['link'] = gdata['needers'][-1]
            gdata['needers'].pop(-1)
            try:
                await bot.send_message(sdate['link'], text=text3)
                await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                            text=text3, reply_markup=None)
                await state.set_state('CHAT')
                await dp.current_state(chat=sdate['link'], user=sdate['link']).set_state('CHAT')
                await dp.current_state(chat=sdate['link'], user=sdate['link']).set_data(
                    {'link': callback.message.chat.id})
            except:
                sdate['link'] = 0

        else:
            if callback.message.chat.id not in gdata['helpers']:
                gdata['helpers'].append(callback.message.chat.id)
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        text=text6, reply_markup=None)

    await state.set_data(sdate)
    await global_state.set_data(gdata)


@dp.message_handler(state='CHAT', content_types=[ContentType.ANY])
async def chat_handler(message: Message):
    print(1)
    state = dp.current_state()
    uid = await state.get_data()
    uid = uid['link']

    try:
        await bot.copy_message(uid, message.chat.id, message.message_id)
    except:
        await bot.send_message(message.chat.id, text4)


async def startup(dispatcher: Dispatcher):
    state = dispatcher.current_state(chat=0, user=0)
    data = await state.get_data()
    if 'data' not in data.keys():
        data = {'helpers': list(), 'needers': list()}
        await state.set_data(data)

    print('Data:', data)

    return True


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    return True


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown, on_startup=startup)
