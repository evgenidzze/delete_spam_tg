import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.types import MessageEntity
from dotenv import load_dotenv
from g4f.client import Client

load_dotenv()
TOKEN = os.getenv('TOKEN')

logging.basicConfig(level=logging.INFO)
client = Client()
bot = Bot(token=TOKEN)
dp = Dispatcher()
restrict_text = (
    '@' 'реєструйся', 'пишите', 'пишіть', 'роздача', 'плачу', 'в профілі', 'в профиле', 'заробіток', 'заработать',
    'регистрируйся',
    "зароб")


# @dp.message(Command('rm_old_msgs'))
# async def rm_old_sys_msg(message: types.Message):
#     for message_id in range(1, 3):
#         try:
#
#             await bot.delete_message(chat_id='-1002589587595', message_id=message_id)
#         except:
#             pass

@dp.message()
async def delete_new_system_messages(message: types.Message):
    # await gpt_check(message)
    user = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if user.status not in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR) and message.text:
        await check_entities(message)
        text = message.text.lower()
        for restrict_word in restrict_text:
            if restrict_word in text:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


async def check_entities(message):
    if message.entities:
        for entity in message.entities:
            if entity.type in ('url', 'mention'):
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                return


async def gpt_check(message):
    prompt = f"""
        Проаналізуй наступний текст і визнач, чи містить він рекламний підтекст для заробітку або переходу по посиланням. У тексті не може бути посилань. 
        Дай відповідь у форматі JSON з полями:
        - has_ad_content: true/false
        - confidence: від 0 до 1
        - explanation: коротке пояснення чому ти так вважаєш

        Текст для аналізу: 
        "{message.text}"
        """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        web_search=False
    )
    print(response.choices[0].message.content)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
