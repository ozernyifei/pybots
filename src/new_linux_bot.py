from decouple import config 
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from asyncpg import create_pool
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
import datetime 

TELEGRAM_BOT_TOKEN=config('TELEGRAM_BOT_TOKEN')

async def get_user(telegram_id):
    pool = await create_connection()
    user = await pool.fetchrow("SELECT * FROM users WHERE telegram_id=$1", telegram_id)
    await pool.close()
    return user

# Создание бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot=bot)

# Обработка сообщений
@dp.message(Command("start"))
async def start(message: types.Message):
    pool = await create_connection()
    # Проверка, есть ли пользователь в базе данных
    user = await get_user(message.from_user.id)
    if user is None:
        # Создание нового пользователя
        await pool.execute("INSERT INTO users (telegram_id, username, first_name, last_name) VALUES ($1, $2, $3, $4)",
                            message.from_user.id, message.from_user.username, message.from_user.first_name,
                            message.from_user.last_name)
        user = await pool.fetchrow("SELECT * FROM users WHERE telegram_id=$1", message.from_user.id)
        
    # Create a basic keyboard
    start_keyboard = ReplyKeyboardMarkup()
    start_keyboard.add(
        KeyboardButton(text="Отправить настроение"),
        KeyboardButton(text="Получить настроение"),
    )

    # Send the keyboard to the user
    await message.answer(
        "Привет! Это бот настроения. Что ты хочешь сделать?",
        reply_markup=start_keyboard
    )

        # Отправка приветствия
    await message.answer(f"Привет, {user['username']}!")
    
    await pool.close()

# Обработка команд
@dp.message(Command("mood"))
async def set_mood(message: types.Message):
    pool = await create_connection()
    start_keyboard = [
        [KeyboardButton(text="Хорошее")]]
    start_keyboard.add(
        KeyboardButton(text="Среднее"),
        KeyboardButton(text="Плохое"),
        KeyboardButton(text="Вернуться обратно")
    )
    keyboard = ReplyKeyboardMarkup(type=list[list[KeyboardButton]],
                                   keyboard=start_keyboard,
                                   resize_keyboard=True 
                                   )
    

    await message.answer("Какое у тебя настроение?", reply_markup=keyboard)

    mood = message.text

    user = await get_user(message.from_user.id)
    last_mood_date = user.get("last_mood_date")
    if last_mood_date is not None:
        now = datetime.datetime.now()
        if now - last_mood_date < datetime.timedelta(days=1):
            await message.answer("Ты уже отправил свое настроение сегодня. Попробуй снова завтра.")
            return

    # Save the mood to the database
    await pool.execute(
        "INSERT INTO users_moods (user_id, mood) VALUES ($1, $2)",
        message.from_user.id,
        mood,
    )

    # Update the user's last mood date
    await pool.execute(
        "UPDATE users SET last_mood_date = NOW() WHERE telegram_id = $1",
        message.from_user.id,
    )

    # Send a confirmation message to the user
    await message.answer(f"Твое настроение обновлено на {mood}.")


    


async def create_connection():
    # Подключение к базе данных
    pool = await create_pool(user=config('pg_user'),
                             password=config('pg_pass'),
                             host=config('pg_host'),
                             port=config('pg_port'),
                             database=config('pg_db'),
                             command_timeout=60)
    return pool
async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())