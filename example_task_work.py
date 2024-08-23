from pyrogram import Client
from decouple import config

bot = Client(name=config('LOGIN'),
             api_id=config('API_ID'),
             api_hash=config('API_HASH'),
             phone_number=config('PHONE'))

bot.start()

bot.send_message(chat_id='me', text='Отправка сообщения себе')
bot.send_message(chat_id='user_login', text='Отправка сообщения по логину другому пользователю')
bot.send_message(chat_id="+70000000", text='Отправка сообщения по номеру телефона')
bot.send_message(chat_id=122334566, text='Отправка сообщения по телеграмм айди')

bot.stop()
