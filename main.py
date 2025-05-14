from telethon import TelegramClient, events
import os

# Получение данных из переменных окружения
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

# Настройки канала
channel_id = -1002251445069

# Словарь: ключ - исходная ветка, значение - список целевых веток
thread_mapping = {
    3: [19, 21],
    22: [19],
    4: [20],
    23: [20],
    24: [21],
}

# Создание клиента как бота
client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(chats=channel_id))
async def handler(event):
    thread_id = event.message.message_thread_id
    if thread_id in thread_mapping:
        for target_thread_id in thread_mapping[thread_id]:
            try:
                await client.send_message(
                    entity=channel_id,
                    message=event.message.text or '',
                    file=event.message.media,
                    message_thread_id=target_thread_id,
                    link_preview=event.message.web_preview,
                    parse_mode=None
                )
                print(f"Сообщение из ветки {thread_id} репостнуто в ветку {target_thread_id}")
            except Exception as e:
                print(f"Ошибка при репосте: {e}")

print("Бот запущен...")
client.run_until_disconnected()
