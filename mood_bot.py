import pyodbc
import telebot
from telebot import types

# Подключение к базе данных
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=database_name;UID=username;PWD=password')
cursor = conn.cursor()

# Создание бота
bot = telebot.TeleBot('TOKEN')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    good_button = types.KeyboardButton('Хорошее')
    average_button = types.KeyboardButton('Среднее')
    bad_button = types.KeyboardButton('Плохое')
    markup.add(good_button, average_button, bad_button)
    bot.send_message(message.chat.id, 'Какое у вас сегодня настроение?', reply_markup=markup)

# Обработчик кнопок
@bot.message_handler(func=lambda message: message.text in ['Хорошее', 'Среднее', 'Плохое'])
def mood_handler(message):
    # Проверяем, была ли запись настроения от пользователя за последние 24 часа
    # query = "SELECT * FROM mood WHERE user_id = ? AND time > DATEADD(hour, -24, GETDATE())"
    # cursor.execute(query, message.chat.id)
    # row = cursor.fetchone()

    # # Если запись была, обновляем ее, иначе добавляем новую запись
    # if row:
    #     query = "UPDATE mood SET mood = ?, time = GETDATE() WHERE id = ?"
    #     cursor.execute(query, message.text, row.id
    # else:
    #     query = "INSERT INTO mood (user_id, mood, time) VALUES (?, ?, GETDATE())"
    #     cursor.execute(query, message.chat.id, message.text)

    # conn.commit()
    bot.send_message(message.chat.id, 'Ваше настроение сохранено')

# Обработчик команды /mood
@bot.message_handler(commands=['mood'])
def mood_report(message):
    query = "SELECT * FROM mood WHERE user_id = ? AND time > DATEADD(day, -7, GETDATE())"
    cursor.execute(query, message.chat.id)
    rows = cursor.fetchall()

    if rows:
        mood_report = '\n'.join(f'{row.time}: {row.mood}' for row in rows)
        bot.send_message(message.chat.id, f'Ваше настроение за последние 7 дней:\n{mood_report}')
    else:
        bot.send_message(message.chat.id, 'У вас пока нет записей о настроении')

# Запуск бота
bot.polling(none_stop= True)
