import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '6290464531:AAHyfuLMg5eMZMe348O8TxkVXQ7vhEdE1vA'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

state = {}

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    state[message.from_user.id] = {}
    await message.answer("Hi there! How are you feeling today? (happy, sad, neutral, angry, etc.)")

@dp.message_handler()
async def process_mood(message: types.Message):
    state[message.from_user.id]['mood'] = message.text
    await bot.send_message(
        chat_id=message.from_user.id, 
        text=f"Got it, you're feeling {message.text} today. Thank you!"
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
