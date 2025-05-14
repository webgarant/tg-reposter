from telethon import TelegramClient, events
import os

# Получение данных из переменных окружения
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# Настройки канала
channel_id = -1002251445069

# Словарь: ключ - исходная ветка, значение - целевая ветка
thread_mapping = {
    3: [19],      # Ветка 3 репостится в 19
    22: [19],     # Ветка 22 репостится в 19
    4: [20],      # Ветка 4 репостится в 20
    23: [20],     # Ветка 23 репостится в 20
    3: [21],      # Ветка 3 репостится в 21
    24: [21],     # Ветка 24 репостится в 21
}

# Создание клиента Telethon
client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage(chats=channel_id))
async def handler(event):
    # Если сообщение из одной из исходных веток
    if event.message.message_thread_id in thread_mapping:
        # Репостим в целевые ветки для данной исходной
        for target_thread_id in thread_mapping[event.message.message_thread_id]:
            try:
                await client.send_message(
                    entity=channel_id,
                    message=event.message.text or '',
                    file=event.message.media,
                    message_thread_id=target_thread_id,
                    link_preview=event.message.web_preview,
                    parse_mode=None
                )
                print(f"Сообщение из ветки {event.message.message_thread_id} репостнуто в ветку {target_thread_id}")
            except Exception as e:
                print(f"Ошибка при репосте: {e}")

client.start()
print("Бот запущен...")
client.run_until_disconnected()