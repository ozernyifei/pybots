import pyodbc
import telebot
import datetime
from telebot import types

server_name = 'localhost'  # Имя вашего сервера
database_name = 'MoodBotDB'  # Название вашей базы данных
username = 'botbotname'  # Ваше имя пользователя для доступа к базе данных
password = 'password'  # Ваш пароль для доступа к базе данных

# Строка подключения
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}'

# Создаем соединение
cnxn = pyodbc.connect(connection_string)

cursor = cnxn.cursor()

# Создание бота
bot = telebot.TeleBot('6290464531:AAHyfuLMg5eMZMe348O8TxkVXQ7vhEdE1vA')

# Обработчик команды /start
@bot.message_handler(commands=['start'])

def start(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
    good_button = types.KeyboardButton('Хорошее')
    average_button = types.KeyboardButton('Среднее')
    bad_button = types.KeyboardButton('Плохое')
    markup.add(good_button, average_button, bad_button)
    bot.send_message(message.chat.id, 'Какое у вас сегодня настроение?', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Хорошее', 'Среднее', 'Плохое'])
def add_mood_to_db(message):
    user_id = message.chat.id
    now = datetime.datetime.now()  # Получаем текущее время
    last_mood_time = get_last_mood_time(message.chat.id)  # Получаем время последнего добавления настроения

    # Проверяем, прошло ли более 24 часов с момента последнего добавления настроения
    if last_mood_time is None or now - last_mood_time >= datetime.timedelta(hours=24):
        # Выполняем запрос на вставку в базу данных
        cursor.execute("INSERT INTO mood (user_id, mood, time) VALUES (?, ?, ?)",
                       (user_id, message, now))
        cnxn.commit()  # Сохраняем изменения в базе данных
        return True
    else:
        return False

# Обработчик кнопок
@bot.message_handler(func=lambda message: message.text in ['Хорошее', 'Среднее', 'Плохое'])
def mood_handler(message):
    # Получаем из базы данных последнюю запись настроения пользователя
    query = "SELECT TOP 1 * FROM mood WHERE user_id = ? ORDER BY time DESC"
    cursor.execute(query, message.chat.id)
    row = cursor.fetchone()

    if row:
        # Проверяем, прошло ли уже 24 часа с момента последней записи настроения
        last_time = row.time
        time_diff = (datetime.datetime.now() - last_time).total_seconds() // 3600
        if time_diff < 24:
            # Если прошло меньше 24 часов, сообщаем пользователю, что он уже сегодня сообщил свое настроение
            bot.send_message(message.chat.id, f'Вы уже сообщили свое настроение сегодня. Следующая запись будет доступна через {24 - time_diff} часа(ов).')
        else:
            # Если прошло больше 24 часов, даем пользователю возможность обновить свое настроение
            mood_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            mood_keyboard.add(types.KeyboardButton('Хорошее'))
            mood_keyboard.add(types.KeyboardButton('Среднее'))
            mood_keyboard.add(types.KeyboardButton('Плохое'))
            bot.send_message(message.chat.id, 'Какое у вас настроение?', reply_markup=mood_keyboard)
    else:
        # Если у пользователя еще нет записей настроения, предлагаем ему сообщить свое настроение
        mood_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mood_keyboard.add(types.KeyboardButton('Хорошее'))
        mood_keyboard.add(types.KeyboardButton('Среднее'))
        mood_keyboard.add(types.KeyboardButton('Плохое'))
        bot.send_message(message.chat.id, 'Какое у вас настроение?', reply_markup=mood_keyboard)
    
def get_last_mood_time(user_id):
    cursor.execute("SELECT TOP 1 time FROM mood WHERE user_id = ? ORDER BY time DESC", (user_id))
    row = cursor.fetchone()
    if row is not None:
        return row[0]
    else:
        return None
        



# Обработчик команды /mood
@bot.message_handler(commands=['mood'])
def mood_report(message):
    user_id = message.chat.id
    query = "SELECT * FROM mood WHERE user_id = ? AND time > DATEADD(day, -7, GETDATE())"
    cursor.execute(query, user_id)
    rows = cursor.fetchall()

    if rows:
        mood_report = '\n'.join(f'{row.time}: {row.mood}' for row in rows)
        bot.send_message(user_id, f'Ваше настроение за последние 7 дней:\n{mood_report}')
    else:
        bot.send_message(user_id, 'У вас пока нет записей о настроении')

# Запуск бота
bot.polling(none_stop= True)
