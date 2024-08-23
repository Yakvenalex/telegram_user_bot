from pyrogram import Client, filters
from decouple import config
from pyrogram.types import Message
from datetime import datetime
import pytz

# Инициализация клиента
bot = Client(name=config('LOGIN'),
             api_id=config('API_ID'),
             api_hash=config('API_HASH'),
             phone_number=config('PHONE'))


def get_time_msg():
    # Получение текущего московского времени
    moscow_tz = pytz.timezone('Europe/Moscow')
    current_time = datetime.now(moscow_tz).strftime('%H:%M:%S')
    return f"Текущее московское время: {current_time}"


# Обработчик входящих сообщений
@bot.on_message(filters.text)
async def handle_message(client: Client, message: Message):
    text = message.text.lower()

    # Обработка команд /start и /help
    if text == '/start':
        await message.reply("Привет! Я ваш помощник-бот. Введите /help для получения списка команд.")
    elif text == '/help':
        await message.reply(
            "Доступные команды:\n"
            "/start - Приветственное сообщение\n"
            "/help - Список команд"
        )
    # Обработка запроса времени
    elif 'который сейчас час' in text:
        await message.reply(text=get_time_msg())
    # Пересылка сообщения в избранное
    elif "в избранное" in text:
        await client.forward_messages(
            chat_id="me",  # Идентификатор чата для "Избранных сообщений"
            from_chat_id=message.chat.id,
            message_ids=message.id
        )
        await message.reply("Сообщение переслано в избранное.")
    # Пересылка сообщения в указанный чат
    elif "перешли это в чат:" in text:
        try:
            target_chat_id = text.split("перешли это в чат:")[1].strip()
            await client.forward_messages(
                chat_id=target_chat_id,
                from_chat_id=message.chat.id,
                message_ids=message.id
            )
            await message.reply(f"Сообщение переслано в чат с ID {target_chat_id}.")
        except Exception as e:
            await message.reply(f"Ошибка при пересылке сообщения: {e}")
    # Копирование сообщения в указанный чат
    elif "скопируй это в чат:" in text:
        try:
            target_chat_id = text.split("скопируй это в чат:")[1].strip()
            await client.copy_message(
                chat_id=target_chat_id,
                from_chat_id=message.chat.id,
                message_id=message.id
            )
            await message.reply(f"Сообщение скопировано в чат с ID {target_chat_id}.")
        except Exception as e:
            await message.reply(f"Ошибка при копировании сообщения: {e}")
    # Эхо-ответ
    else:
        await message.reply(text=f'Повторяю без цитаты: {message.text}')
        await message.reply(text=f'Повторяю с цитатой: {message.text}', quote=True)


# Запуск клиента
bot.run()
