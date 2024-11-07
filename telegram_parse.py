from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from datetime import datetime
import time
import random
from dotenv import load_dotenv
import os


load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

client = TelegramClient('your_session_name', api_id, api_hash)

async def get_comments_from_post(post_url):
    load_dotenv()
    await client.connect()
    # Получение ID канала и ID поста из ссылки
    parts = post_url.split('/')
    if len(parts) >= 5 and parts[4] == 'c':
        channel_id = int(parts[5])
        post_id = int(parts[6])
    else:
        raise ValueError("Неверный формат ссылки")

    channel = await client.get_entity(InputPeerChannel(channel_id, 0))

    # Получение истории комментариев к конкретному посту
    messages = await client(GetHistoryRequest(
        peer=channel,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=100,
        add_offset=0,
        hash=0,
        min_id=post_id
    ))

    # Фильтрация комментариев, включая ответы
    comments = []
    for message in messages.messages:
        if message.reply_to_msg_id:
            comment_author = message.sender.first_name
            comment_text = message.message
            comment_time = datetime.fromtimestamp(message.date.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
            comments.append({'author': comment_author, 'text': comment_text, 'time': comment_time})

    # Вывод информации
    for comment in comments:
        print(f"Автор: {comment['author']}")
        print(f"Время: {comment['time']}")
        print(f"Комментарий: {comment['text']}")
        print("-" * 30)

    # 1. Пауза между запросами
    time.sleep(random.randint(2, 5))  # Пауза в 2-5 секунд

    # 2. Ограничение количества запросов
    if len(comments) >= 50:
        print("Достигнут лимит комментариев, завершение работы.")
        return

post_url = 'https://t.me/dva_majors/57094?single'
with client:
    client.loop.run_until_complete(get_comments_from_post(post_url))